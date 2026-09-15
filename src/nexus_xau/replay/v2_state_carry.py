from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Literal, cast

import pandas as pd

from nexus_xau.data.resample import resample_ohlc
from nexus_xau.replay.v2_integration import DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED
from nexus_xau.research.minimal_v2_0700 import (
    H4_RUN_POINTS,
    H4Origin,
    _build_minimal_v2_core,
    _normalize_m1_frame,
    build_h4_origins,
    detect_pat2_full_range,
    origin_state_at,
)

CARRY_CONTRACT = "PHASE1_V2_ORIGIN_STATE_CARRY_V0.1"
V2_VERSION = "0700_MINIMAL_V2.0"
DETECTOR_BRIDGE_HOURS = 8
BRIDGE_CONTINUITY_STATUS = "EXACT_OBSERVED_M1_8H_NO_HOLES_V0.1"
HANDOFF_GAP_POLICY = "REQUIRE_CHECKPOINT_MINUTE_OBSERVED_NO_SYNTHETIC_FILL_V0.1"

COMPLETE_SEED_EVIDENCE_CONTRACT = "PHASE1_V2_COMPLETE_SEED_EVIDENCE_V0.1"
COMPLETE_SEED_ASSERTION = "ALL_ACTIVE_H4_ORIGINS_REPRESENTED_AT_CHECKPOINT"
COMPLETE_SEED_VERIFICATION_STATUS = "INDEPENDENT_EVIDENCE_CLOSED"

SEED_COMPLETE = "COMPLETE"
SEED_SYNTHETIC_COMPLETE = "SYNTHETIC_COMPLETE"
SEED_UNKNOWN_PREHISTORY = "UNKNOWN_PREHISTORY"
SeedCompleteness = Literal["COMPLETE", "SYNTHETIC_COMPLETE", "UNKNOWN_PREHISTORY"]

_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class V2StateCarryError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


@dataclass(frozen=True, slots=True)
class CarriedH4Origin:
    origin_id: str
    side: str
    pattern_known_at: pd.Timestamp
    origin_known_at: pd.Timestamp
    anchor_price: float
    consumed_points_at_checkpoint: float

    def as_origin(self) -> H4Origin:
        return H4Origin(
            origin_id=self.origin_id,
            side=self.side,
            pattern_known_at=self.pattern_known_at,
            origin_known_at=self.origin_known_at,
            anchor_price=self.anchor_price,
        )


@dataclass(frozen=True, slots=True)
class BridgeProvenance:
    source_family: str
    symbol: str
    m1_representation: str
    integration_representation_version: str
    continuity_status: str
    source_provenance_sha256: str
    bridge_sha256: str


@dataclass(frozen=True, slots=True)
class CompleteSeedEvidence:
    evidence_ref: str
    evidence_sha256: str
    assertion: str
    verification_status: str
    independence_basis: str
    checkpoint_at: pd.Timestamp
    source_family: str
    symbol: str
    m1_representation: str
    integration_representation_version: str


@dataclass(frozen=True, slots=True)
class V2OriginStateCarry:
    checkpoint_at: pd.Timestamp
    seed_completeness: SeedCompleteness
    source_family: str
    symbol: str
    m1_representation: str
    integration_representation_version: str
    active_origins: tuple[CarriedH4Origin, ...]
    bridge_m1: pd.DataFrame
    source_provenance: dict[str, object]
    bridge_provenance: BridgeProvenance
    complete_seed_evidence: CompleteSeedEvidence | None = None
    prior_checkpoint_sha256: str | None = None

def _utc(value: pd.Timestamp | str) -> pd.Timestamp:
    timestamp = pd.Timestamp(value)
    if timestamp.tz is None:
        raise ValueError("Timestamp must be timezone-aware")
    return timestamp.tz_convert("UTC")


def _require_h4_boundary(timestamp: pd.Timestamp) -> None:
    if timestamp != timestamp.floor("4h"):
        raise V2StateCarryError(
            "CARRY_BOUNDARY_UNALIGNED",
            "checkpoint_at must be an exact 4-hour UTC boundary",
        )


def _active_m1(frame: pd.DataFrame) -> pd.DataFrame:
    if "volume" not in frame.columns:
        return frame.copy()
    return frame.loc[frame["volume"] > 0].copy()


def _json_scalar(value: object) -> object:
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if hasattr(value, "item"):
        return value.item()
    if pd.isna(value):
        return None
    return str(value)


def _json_normalize(value: object) -> object:
    if isinstance(value, dict):
        return {str(key): _json_normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_normalize(item) for item in value]
    return _json_scalar(value)


def _canonical_sha256(value: object) -> str:
    canonical = json.dumps(
        _json_normalize(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def _bridge_payload(frame: pd.DataFrame) -> dict[str, object]:
    columns = [str(column) for column in frame.columns]
    rows: list[list[object]] = []
    for timestamp, row in frame.iterrows():
        rows.append(
            [
                pd.Timestamp(timestamp).isoformat(),
                *[_json_scalar(row[column]) for column in frame.columns],
            ]
        )
    return {"columns": columns, "rows": rows}


def _bridge_sha256(frame: pd.DataFrame) -> str:
    return _canonical_sha256(_bridge_payload(frame))


def _source_provenance_sha256(source_provenance: dict[str, object]) -> str:
    return _canonical_sha256(source_provenance)


def _origin_payload(origin: CarriedH4Origin) -> dict[str, object]:
    return {
        "origin_id": origin.origin_id,
        "side": origin.side,
        "pattern_known_at": origin.pattern_known_at.isoformat(),
        "origin_known_at": origin.origin_known_at.isoformat(),
        "anchor_price": origin.anchor_price,
        "consumed_points_at_checkpoint": origin.consumed_points_at_checkpoint,
    }


def _bridge_provenance_payload(provenance: BridgeProvenance) -> dict[str, object]:
    return {
        "source_family": provenance.source_family,
        "symbol": provenance.symbol,
        "m1_representation": provenance.m1_representation,
        "integration_representation_version": provenance.integration_representation_version,
        "continuity_status": provenance.continuity_status,
        "source_provenance_sha256": provenance.source_provenance_sha256,
        "bridge_sha256": provenance.bridge_sha256,
    }


def _complete_seed_evidence_payload(
    evidence: CompleteSeedEvidence | None,
) -> dict[str, object] | None:
    if evidence is None:
        return None
    return {
        "evidence_ref": evidence.evidence_ref,
        "evidence_sha256": evidence.evidence_sha256,
        "assertion": evidence.assertion,
        "verification_status": evidence.verification_status,
        "independence_basis": evidence.independence_basis,
        "checkpoint_at": evidence.checkpoint_at.isoformat(),
        "source_family": evidence.source_family,
        "symbol": evidence.symbol,
        "m1_representation": evidence.m1_representation,
        "integration_representation_version": evidence.integration_representation_version,
    }

def checkpoint_payload(checkpoint: V2OriginStateCarry) -> dict[str, object]:
    _validate_checkpoint(checkpoint)
    return {
        "contract": CARRY_CONTRACT,
        "v2_version": V2_VERSION,
        "checkpoint_at": checkpoint.checkpoint_at.isoformat(),
        "seed_completeness": checkpoint.seed_completeness,
        "source_family": checkpoint.source_family,
        "symbol": checkpoint.symbol,
        "m1_representation": checkpoint.m1_representation,
        "integration_representation_version": checkpoint.integration_representation_version,
        "active_origins": [_origin_payload(origin) for origin in checkpoint.active_origins],
        "bridge_m1": _bridge_payload(checkpoint.bridge_m1),
        "source_provenance": _json_normalize(checkpoint.source_provenance),
        "bridge_provenance": _bridge_provenance_payload(checkpoint.bridge_provenance),
        "complete_seed_evidence": _complete_seed_evidence_payload(
            checkpoint.complete_seed_evidence
        ),
        "prior_checkpoint_sha256": checkpoint.prior_checkpoint_sha256,
    }


def checkpoint_sha256(checkpoint: V2OriginStateCarry) -> str:
    return _canonical_sha256(checkpoint_payload(checkpoint))


def checkpoint_document(checkpoint: V2OriginStateCarry) -> dict[str, object]:
    payload = checkpoint_payload(checkpoint)
    return {**payload, "checkpoint_sha256": _canonical_sha256(payload)}


def _bridge_from_payload(payload: dict[str, object]) -> pd.DataFrame:
    raw = payload["bridge_m1"]
    if not isinstance(raw, dict):
        raise V2StateCarryError("CARRY_SCHEMA_INVALID", "bridge_m1 must be an object")
    columns = [str(value) for value in raw.get("columns", [])]
    rows = raw.get("rows", [])
    if not isinstance(rows, list):
        raise V2StateCarryError("CARRY_SCHEMA_INVALID", "bridge_m1.rows must be a list")
    index: list[pd.Timestamp] = []
    values: list[list[object]] = []
    for row in rows:
        if not isinstance(row, list) or len(row) != len(columns) + 1:
            raise V2StateCarryError("CARRY_SCHEMA_INVALID", "invalid bridge row")
        index.append(_utc(str(row[0])))
        values.append(list(row[1:]))
    return pd.DataFrame(values, columns=columns, index=pd.DatetimeIndex(index))


def _bridge_provenance_from_payload(payload: dict[str, object]) -> BridgeProvenance:
    raw = payload.get("bridge_provenance")
    if not isinstance(raw, dict):
        raise V2StateCarryError(
            "CARRY_SCHEMA_INVALID",
            "bridge_provenance must be an object",
        )
    return BridgeProvenance(
        source_family=str(raw["source_family"]),
        symbol=str(raw["symbol"]),
        m1_representation=str(raw["m1_representation"]),
        integration_representation_version=str(raw["integration_representation_version"]),
        continuity_status=str(raw["continuity_status"]),
        source_provenance_sha256=str(raw["source_provenance_sha256"]),
        bridge_sha256=str(raw["bridge_sha256"]),
    )


def _complete_seed_evidence_from_payload(
    payload: dict[str, object],
) -> CompleteSeedEvidence | None:
    raw = payload.get("complete_seed_evidence")
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise V2StateCarryError(
            "CARRY_SCHEMA_INVALID",
            "complete_seed_evidence must be an object",
        )
    return CompleteSeedEvidence(
        evidence_ref=str(raw["evidence_ref"]),
        evidence_sha256=str(raw["evidence_sha256"]),
        assertion=str(raw["assertion"]),
        verification_status=str(raw["verification_status"]),
        independence_basis=str(raw["independence_basis"]),
        checkpoint_at=_utc(str(raw["checkpoint_at"])),
        source_family=str(raw["source_family"]),
        symbol=str(raw["symbol"]),
        m1_representation=str(raw["m1_representation"]),
        integration_representation_version=str(raw["integration_representation_version"]),
    )

def checkpoint_from_document(document: dict[str, object]) -> V2OriginStateCarry:
    if document.get("contract") != CARRY_CONTRACT:
        raise V2StateCarryError("CARRY_CONTRACT_MISMATCH", "unexpected carry contract")
    if document.get("v2_version") != V2_VERSION:
        raise V2StateCarryError("CARRY_V2_VERSION_MISMATCH", "unexpected V2 version")
    origins_raw = document.get("active_origins", [])
    if not isinstance(origins_raw, list):
        raise V2StateCarryError("CARRY_SCHEMA_INVALID", "active_origins must be a list")
    origins = tuple(
        CarriedH4Origin(
            origin_id=str(item["origin_id"]),
            side=str(item["side"]),
            pattern_known_at=_utc(str(item["pattern_known_at"])),
            origin_known_at=_utc(str(item["origin_known_at"])),
            anchor_price=float(item["anchor_price"]),
            consumed_points_at_checkpoint=float(item["consumed_points_at_checkpoint"]),
        )
        for item in origins_raw
    )
    checkpoint = V2OriginStateCarry(
        checkpoint_at=_utc(str(document["checkpoint_at"])),
        seed_completeness=cast(SeedCompleteness, str(document["seed_completeness"])),
        source_family=str(document["source_family"]),
        symbol=str(document["symbol"]),
        m1_representation=str(document["m1_representation"]),
        integration_representation_version=str(
            document["integration_representation_version"]
        ),
        active_origins=origins,
        bridge_m1=_bridge_from_payload(document),
        source_provenance=dict(document.get("source_provenance", {})),
        bridge_provenance=_bridge_provenance_from_payload(document),
        complete_seed_evidence=_complete_seed_evidence_from_payload(document),
        prior_checkpoint_sha256=(
            str(document["prior_checkpoint_sha256"])
            if document.get("prior_checkpoint_sha256") is not None
            else None
        ),
    )
    _validate_checkpoint(checkpoint)
    observed_digest = str(document.get("checkpoint_sha256", ""))
    if observed_digest != checkpoint_sha256(checkpoint):
        raise V2StateCarryError("CARRY_DIGEST_MISMATCH", "checkpoint payload was mutated")
    return checkpoint


def _expected_bridge_index(checkpoint_at: pd.Timestamp) -> pd.DatetimeIndex:
    start = checkpoint_at - timedelta(hours=DETECTOR_BRIDGE_HOURS)
    return pd.date_range(
        start,
        checkpoint_at - timedelta(minutes=1),
        freq="1min",
        tz="UTC",
    )


def _validate_bridge(checkpoint: V2OriginStateCarry) -> None:
    bridge = _normalize_m1_frame(checkpoint.bridge_m1)
    expected_index = _expected_bridge_index(checkpoint.checkpoint_at)
    if not bridge.index.equals(expected_index):
        raise V2StateCarryError(
            "CARRY_BRIDGE_CONTINUITY_GAP",
            "bridge must contain the exact observed one-minute grid for the declared eight hours",
        )
    provenance = checkpoint.bridge_provenance
    identity = (
        provenance.source_family,
        provenance.symbol,
        provenance.m1_representation,
        provenance.integration_representation_version,
    )
    expected_identity = (
        checkpoint.source_family,
        checkpoint.symbol,
        checkpoint.m1_representation,
        checkpoint.integration_representation_version,
    )
    if identity != expected_identity:
        raise V2StateCarryError(
            "CARRY_BRIDGE_PROVENANCE_MISMATCH",
            "bridge provenance identity differs from checkpoint source identity",
        )
    if provenance.continuity_status != BRIDGE_CONTINUITY_STATUS:
        raise V2StateCarryError(
            "CARRY_BRIDGE_PROVENANCE_MISMATCH",
            "bridge continuity status is not the frozen carry status",
        )
    if provenance.source_provenance_sha256 != _source_provenance_sha256(
        checkpoint.source_provenance
    ):
        raise V2StateCarryError(
            "CARRY_BRIDGE_PROVENANCE_MISMATCH",
            "bridge source provenance digest does not match checkpoint provenance",
        )
    if provenance.bridge_sha256 != _bridge_sha256(bridge):
        raise V2StateCarryError(
            "CARRY_BRIDGE_DIGEST_MISMATCH",
            "bridge payload digest does not match bridge provenance",
        )


def _validate_complete_seed_evidence(checkpoint: V2OriginStateCarry) -> None:
    evidence = checkpoint.complete_seed_evidence
    if checkpoint.seed_completeness != SEED_COMPLETE:
        if evidence is not None:
            raise V2StateCarryError(
                "CARRY_COMPLETE_EVIDENCE_UNEXPECTED",
                "complete-seed evidence is only valid for COMPLETE checkpoints",
            )
        return
    if evidence is None:
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_REQUIRED",
            "COMPLETE checkpoint requires independent complete-seed evidence",
        )
    if evidence.assertion != COMPLETE_SEED_ASSERTION:
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_INVALID",
            "complete-seed evidence assertion is not recognized",
        )
    if evidence.verification_status != COMPLETE_SEED_VERIFICATION_STATUS:
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_INVALID",
            "complete-seed evidence is not independently closed",
        )
    if not evidence.independence_basis.strip():
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_INVALID",
            "complete-seed evidence lacks an independence basis",
        )
    if not _SHA256_RE.fullmatch(evidence.evidence_sha256):
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_INVALID",
            "complete-seed evidence SHA-256 is invalid",
        )
    evidence_identity = (
        evidence.checkpoint_at,
        evidence.source_family,
        evidence.symbol,
        evidence.m1_representation,
        evidence.integration_representation_version,
    )
    checkpoint_identity = (
        checkpoint.checkpoint_at,
        checkpoint.source_family,
        checkpoint.symbol,
        checkpoint.m1_representation,
        checkpoint.integration_representation_version,
    )
    if evidence_identity != checkpoint_identity:
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_IDENTITY_MISMATCH",
            "complete-seed evidence does not bind to this checkpoint identity",
        )
    evidence_path = Path(evidence.evidence_ref)
    if not evidence_path.is_file():
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_FILE_UNAVAILABLE",
            "complete-seed evidence file is unavailable",
        )
    actual_sha256 = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    if actual_sha256 != evidence.evidence_sha256:
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_DIGEST_MISMATCH",
            "complete-seed evidence file no longer matches its recorded digest",
        )


def _validate_checkpoint(checkpoint: V2OriginStateCarry) -> None:
    _require_h4_boundary(checkpoint.checkpoint_at)
    if checkpoint.seed_completeness not in {
        SEED_COMPLETE,
        SEED_SYNTHETIC_COMPLETE,
        SEED_UNKNOWN_PREHISTORY,
    }:
        raise V2StateCarryError("CARRY_SCHEMA_INVALID", "unsupported seed completeness")
    if not checkpoint.integration_representation_version.strip():
        raise V2StateCarryError(
            "CARRY_SCHEMA_INVALID",
            "integration representation version is required",
        )
    if (
        checkpoint.seed_completeness == SEED_SYNTHETIC_COMPLETE
        and not checkpoint.source_family.startswith("SYNTHETIC")
    ):
        raise V2StateCarryError(
            "CARRY_SYNTHETIC_SOURCE_REQUIRED",
            "SYNTHETIC_COMPLETE is restricted to synthetic source families",
        )
    _validate_bridge(checkpoint)
    _validate_complete_seed_evidence(checkpoint)
    ids = [origin.origin_id for origin in checkpoint.active_origins]
    if len(set(ids)) != len(ids):
        raise V2StateCarryError("CARRY_SCHEMA_INVALID", "duplicate carried origin_id")
    for origin in checkpoint.active_origins:
        if origin.side not in {"BUY", "SELL"}:
            raise V2StateCarryError("CARRY_SCHEMA_INVALID", "invalid carried origin side")
        if origin.consumed_points_at_checkpoint < 0:
            raise V2StateCarryError("CARRY_SCHEMA_INVALID", "negative consumed points")
        if origin.consumed_points_at_checkpoint >= H4_RUN_POINTS:
            raise V2StateCarryError("CARRY_SCHEMA_INVALID", "terminal origin cannot be active")


def load_complete_seed_evidence(path: str | Path) -> CompleteSeedEvidence:
    evidence_path = Path(path).resolve()
    raw = evidence_path.read_bytes()
    payload = json.loads(raw.decode("utf-8"))
    if not isinstance(payload, dict):
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_INVALID",
            "complete-seed evidence document must be an object",
        )
    if payload.get("contract") != COMPLETE_SEED_EVIDENCE_CONTRACT:
        raise V2StateCarryError(
            "CARRY_COMPLETE_EVIDENCE_INVALID",
            "unexpected complete-seed evidence contract",
        )
    evidence = CompleteSeedEvidence(
        evidence_ref=str(evidence_path),
        evidence_sha256=hashlib.sha256(raw).hexdigest(),
        assertion=str(payload.get("assertion", "")),
        verification_status=str(payload.get("verification_status", "")),
        independence_basis=str(payload.get("independence_basis", "")),
        checkpoint_at=_utc(str(payload["checkpoint_at"])),
        source_family=str(payload["source_family"]),
        symbol=str(payload["symbol"]),
        m1_representation=str(payload["m1_representation"]),
        integration_representation_version=str(
            payload["integration_representation_version"]
        ),
    )
    return evidence


def _build_checkpoint(
    *,
    m1: pd.DataFrame,
    checkpoint_at: pd.Timestamp | str,
    seed_completeness: SeedCompleteness,
    source_family: str,
    symbol: str,
    m1_representation: str,
    integration_representation_version: str,
    source_provenance: dict[str, object],
    complete_seed_evidence: CompleteSeedEvidence | None,
    prior_checkpoint_sha256: str | None,
) -> V2OriginStateCarry:
    checkpoint_at = _utc(checkpoint_at)
    _require_h4_boundary(checkpoint_at)
    frame = _normalize_m1_frame(m1)
    active = _active_m1(frame)
    bridge_start = checkpoint_at - timedelta(hours=DETECTOR_BRIDGE_HOURS)
    bridge = active.loc[(active.index >= bridge_start) & (active.index < checkpoint_at)].copy()
    h4 = resample_ohlc(active.loc[active.index < checkpoint_at], "H4")
    origins = build_h4_origins(h4, detect_pat2_full_range(h4, "H4"))
    carried: list[CarriedH4Origin] = []
    for origin in origins:
        if origin.origin_known_at > checkpoint_at:
            continue
        state, consumed, _, _ = origin_state_at(
            active_m1=active, origin=origin, at=checkpoint_at
        )
        if state != "ACTIVE":
            continue
        carried.append(
            CarriedH4Origin(
                origin_id=origin.origin_id,
                side=origin.side,
                pattern_known_at=origin.pattern_known_at,
                origin_known_at=origin.origin_known_at,
                anchor_price=origin.anchor_price,
                consumed_points_at_checkpoint=consumed,
            )
        )
    bridge_provenance = BridgeProvenance(
        source_family=source_family,
        symbol=symbol,
        m1_representation=m1_representation,
        integration_representation_version=integration_representation_version,
        continuity_status=BRIDGE_CONTINUITY_STATUS,
        source_provenance_sha256=_source_provenance_sha256(source_provenance),
        bridge_sha256=_bridge_sha256(bridge),
    )
    checkpoint = V2OriginStateCarry(
        checkpoint_at=checkpoint_at,
        seed_completeness=seed_completeness,
        source_family=source_family,
        symbol=symbol,
        m1_representation=m1_representation,
        integration_representation_version=integration_representation_version,
        active_origins=tuple(carried),
        bridge_m1=bridge,
        source_provenance=dict(source_provenance),
        bridge_provenance=bridge_provenance,
        complete_seed_evidence=complete_seed_evidence,
        prior_checkpoint_sha256=prior_checkpoint_sha256,
    )
    _validate_checkpoint(checkpoint)
    return checkpoint

def create_checkpoint(
    *,
    m1: pd.DataFrame,
    checkpoint_at: pd.Timestamp | str,
    seed_completeness: SeedCompleteness,
    source_family: str,
    symbol: str,
    m1_representation: str,
    integration_representation_version: str,
    source_provenance: dict[str, object],
    prior_checkpoint_sha256: str | None = None,
) -> V2OriginStateCarry:
    if seed_completeness == SEED_COMPLETE:
        raise V2StateCarryError(
            "CARRY_COMPLETE_REQUIRES_EVIDENCE_API",
            "COMPLETE checkpoints must be created with create_complete_checkpoint",
        )
    if seed_completeness not in {SEED_SYNTHETIC_COMPLETE, SEED_UNKNOWN_PREHISTORY}:
        raise V2StateCarryError("CARRY_SCHEMA_INVALID", "unsupported seed completeness")
    return _build_checkpoint(
        m1=m1,
        checkpoint_at=checkpoint_at,
        seed_completeness=seed_completeness,
        source_family=source_family,
        symbol=symbol,
        m1_representation=m1_representation,
        integration_representation_version=integration_representation_version,
        source_provenance=source_provenance,
        complete_seed_evidence=None,
        prior_checkpoint_sha256=prior_checkpoint_sha256,
    )


def create_complete_checkpoint(
    *,
    m1: pd.DataFrame,
    checkpoint_at: pd.Timestamp | str,
    source_family: str,
    symbol: str,
    m1_representation: str,
    integration_representation_version: str,
    source_provenance: dict[str, object],
    complete_seed_evidence: CompleteSeedEvidence,
    prior_checkpoint_sha256: str | None = None,
) -> V2OriginStateCarry:
    return _build_checkpoint(
        m1=m1,
        checkpoint_at=checkpoint_at,
        seed_completeness=SEED_COMPLETE,
        source_family=source_family,
        symbol=symbol,
        m1_representation=m1_representation,
        integration_representation_version=integration_representation_version,
        source_provenance=source_provenance,
        complete_seed_evidence=complete_seed_evidence,
        prior_checkpoint_sha256=prior_checkpoint_sha256,
    )


def run_continuation(
    *,
    checkpoint: V2OriginStateCarry,
    continuation_m1: pd.DataFrame,
    source_family: str,
    symbol: str,
    m1_representation: str,
    integration_representation_version: str,
    handoff_gap_policy: str,
    allow_synthetic_complete: bool = False,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, object]]:
    _validate_checkpoint(checkpoint)
    if checkpoint.source_family != source_family:
        raise V2StateCarryError("CARRY_SOURCE_FAMILY_MISMATCH", "source family changed")
    if checkpoint.symbol != symbol:
        raise V2StateCarryError("CARRY_SYMBOL_MISMATCH", "symbol changed")
    if checkpoint.m1_representation != m1_representation:
        raise V2StateCarryError("CARRY_REPRESENTATION_MISMATCH", "M1 representation changed")
    if checkpoint.integration_representation_version != integration_representation_version:
        raise V2StateCarryError(
            "CARRY_INTEGRATION_VERSION_MISMATCH",
            "integration representation version changed",
        )
    if handoff_gap_policy != HANDOFF_GAP_POLICY:
        raise V2StateCarryError(
            "CARRY_HANDOFF_POLICY_MISMATCH",
            "continuation must use the frozen no-fabrication handoff policy",
        )
    if checkpoint.seed_completeness == SEED_UNKNOWN_PREHISTORY:
        raise V2StateCarryError(
            DATA_EXCLUDED_ORIGIN_HISTORY_UNSEEDED,
            "UNKNOWN_PREHISTORY cannot promote through forward continuation",
        )
    if checkpoint.seed_completeness == SEED_SYNTHETIC_COMPLETE and not allow_synthetic_complete:
        raise V2StateCarryError(
            "CARRY_SYNTHETIC_ONLY",
            "SYNTHETIC_COMPLETE is limited to controlled parity fixtures",
        )

    continuation = _active_m1(_normalize_m1_frame(continuation_m1))
    if continuation.empty:
        raise V2StateCarryError(
            "CARRY_HANDOFF_GAP",
            "continuation contains no observed M1 at checkpoint handoff",
        )
    if bool((continuation.index < checkpoint.checkpoint_at).any()):
        raise V2StateCarryError(
            "CARRY_CONTINUATION_OVERLAP",
            "continuation M1 must begin at or after checkpoint_at",
        )
    if continuation.index[0] != checkpoint.checkpoint_at:
        raise V2StateCarryError(
            "CARRY_HANDOFF_GAP",
            "first observed continuation M1 must equal checkpoint_at; no fill is permitted",
        )
    if continuation.index.duplicated().any():
        raise V2StateCarryError(
            "CARRY_CONTINUATION_OVERLAP",
            "continuation contains duplicate M1 timestamps",
        )

    combined = pd.concat([checkpoint.bridge_m1, continuation]).sort_index(kind="stable")
    if combined.index.duplicated().any():
        raise V2StateCarryError("CARRY_CONTINUATION_OVERLAP", "duplicate handoff timestamps")
    initial_origins = [origin.as_origin() for origin in checkpoint.active_origins]
    consumed_floors = {
        origin.origin_id: origin.consumed_points_at_checkpoint
        for origin in checkpoint.active_origins
    }
    days, origins, events, report = _build_minimal_v2_core(
        active_m1=combined,
        source_descriptor=f"CARRY:{source_family}:{symbol}",
        source_metadata_descriptor=CARRY_CONTRACT,
        source_sha256=checkpoint_sha256(checkpoint),
        initial_origins=initial_origins,
        consumed_floor_by_origin=consumed_floors,
        output_start=checkpoint.checkpoint_at,
        detected_origin_after=checkpoint.checkpoint_at,
    )
    report = dict(report)
    report["carry_contract"] = CARRY_CONTRACT
    report["checkpoint_sha256"] = checkpoint_sha256(checkpoint)
    report["seed_completeness"] = checkpoint.seed_completeness
    report["detector_bridge_hours"] = DETECTOR_BRIDGE_HOURS
    report["handoff_gap_policy"] = HANDOFF_GAP_POLICY
    report["bridge_continuity_status"] = checkpoint.bridge_provenance.continuity_status
    return days, origins, events, report

def write_checkpoint_json(checkpoint: V2OriginStateCarry, path: str | Path) -> str:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    document = checkpoint_document(checkpoint)
    serialized = json.dumps(document, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    temporary = target.with_suffix(target.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        handle.write(serialized)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, target)
    return str(document["checkpoint_sha256"])


def read_checkpoint_json(path: str | Path) -> V2OriginStateCarry:
    document = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise V2StateCarryError("CARRY_SCHEMA_INVALID", "checkpoint document must be an object")
    return checkpoint_from_document(document)