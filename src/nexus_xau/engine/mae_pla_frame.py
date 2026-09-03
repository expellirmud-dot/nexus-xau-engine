from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class MaePlaFrameCandidate:
    reference_price: float
    upper_price: float
    lower_price: float
    reference_distance: float


@dataclass(frozen=True, slots=True)
class MaePlaFrameCandidateSet:
    open_0700_price: float
    project_point_size: float
    half_width_points: float
    statistical_step_price: float
    candidates: tuple[MaePlaFrameCandidate, ...]
    timing_mapping_resolved: bool = False
    snap_tie_resolved: bool = False


def _nearest_statistical_references(price: float, *, step_price: float) -> tuple[float, ...]:
    if step_price <= 0:
        raise ValueError("step_price must be positive")

    lower = math.floor(price / step_price) * step_price
    upper = math.ceil(price / step_price) * step_price
    if math.isclose(lower, upper, rel_tol=0.0, abs_tol=1e-12):
        return (lower,)

    lower_distance = abs(price - lower)
    upper_distance = abs(upper - price)
    if math.isclose(lower_distance, upper_distance, rel_tol=0.0, abs_tol=1e-12):
        return (lower, upper)
    if lower_distance < upper_distance:
        return (lower,)
    return (upper,)


def build_mae_pla_frame_candidates(
    open_0700_price: float,
    *,
    project_point_size: float = 0.01,
    half_width_points: float = 500.0,
    statistical_step_price: float = 5.0,
) -> MaePlaFrameCandidateSet:
    """Build source-backed Mae Pla price candidates without guessing time/tie rules.

    Primary image evidence materially supports:
    - use the H4/opening-price context around 07:00;
    - select a nearby statistical level ending in 0 or 5;
    - upper/lower frame = reference +/- 500 project points.

    Exact timezone mapping and tie behavior are unresolved. This builder receives
    the 07:00-context price externally and returns both equally-near statistical
    references on a tie rather than choosing one silently.
    """

    if project_point_size <= 0:
        raise ValueError("project_point_size must be positive")
    if half_width_points <= 0:
        raise ValueError("half_width_points must be positive")

    half_width_price = project_point_size * half_width_points
    references = _nearest_statistical_references(
        open_0700_price,
        step_price=statistical_step_price,
    )
    candidates = tuple(
        MaePlaFrameCandidate(
            reference_price=reference,
            upper_price=reference + half_width_price,
            lower_price=reference - half_width_price,
            reference_distance=abs(open_0700_price - reference),
        )
        for reference in references
    )

    return MaePlaFrameCandidateSet(
        open_0700_price=open_0700_price,
        project_point_size=project_point_size,
        half_width_points=half_width_points,
        statistical_step_price=statistical_step_price,
        candidates=candidates,
        timing_mapping_resolved=False,
        snap_tie_resolved=len(candidates) == 1,
    )
