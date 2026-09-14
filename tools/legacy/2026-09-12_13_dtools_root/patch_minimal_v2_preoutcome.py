from pathlib import Path

p=Path(r"D:\nexus-xau-engine-repo\src\nexus_xau\research\minimal_v2_0700.py")
s=p.read_text(encoding="utf-8")

old='''def origin_state_at(
    *,
    active_m1: pd.DataFrame,
    origin: H4Origin,
    at: pd.Timestamp,
) -> tuple[str, float, float, pd.Timestamp | None]:
    consumed = favorable_consumed_points(
        active_m1=active_m1,
        side=origin.side,
        anchor=origin.anchor_price,
        start=origin.origin_known_at,
        end=at,
    )
    touch = first_point_check_touch(
        active_m1=active_m1,
        anchor=origin.anchor_price,
        start=origin.origin_known_at,
        end=at,
    )
    if consumed >= H4_RUN_POINTS:
        return "RUN_COMPLETE", consumed, max(0.0, H4_RUN_POINTS - consumed), touch
    if touch is not None:
        return "POINT_CHECK_DESTROYED", consumed, H4_RUN_POINTS - consumed, touch
    return "ACTIVE", consumed, H4_RUN_POINTS - consumed, None
'''
new='''def origin_state_at(
    *,
    active_m1: pd.DataFrame,
    origin: H4Origin,
    at: pd.Timestamp,
) -> tuple[str, float, float, pd.Timestamp | None]:
    path = active_m1.loc[
        (active_m1.index >= origin.origin_known_at) & (active_m1.index < at)
    ]
    target_price = (
        origin.anchor_price + H4_RUN_POINTS * PROJECT_POINT_SIZE
        if origin.side == "BUY"
        else origin.anchor_price - H4_RUN_POINTS * PROJECT_POINT_SIZE
    )
    hit = boundary_hit(
        path=path,
        side=origin.side,
        target_price=target_price,
        point_check_price=origin.anchor_price,
    )
    consumed = favorable_consumed_points(
        active_m1=active_m1,
        side=origin.side,
        anchor=origin.anchor_price,
        start=origin.origin_known_at,
        end=at,
    )
    remaining = max(0.0, H4_RUN_POINTS - consumed)

    if hit.first_hit == "TARGET_FIRST":
        return "RUN_COMPLETE", consumed, remaining, hit.point_check_at
    if hit.first_hit == "POINT_CHECK_FIRST":
        return "POINT_CHECK_DESTROYED", consumed, remaining, hit.point_check_at
    if hit.first_hit == "AMBIGUOUS_SAME_BAR":
        return "AMBIGUOUS_TERMINAL_SAME_BAR", consumed, remaining, hit.point_check_at
    return "ACTIVE", consumed, remaining, None
'''
if old not in s:
    raise SystemExit("origin_state block not found")
s=s.replace(old,new)

marker='''def _target_price_from_confirmation(
    *, side: str, confirmation_close: float, remaining_points: float
) -> float:
'''
helper='''def action_state_for_candidate(
    *, same_side_origin_count: int, opposite_side_origin_count: int
) -> str:
    if same_side_origin_count > 1 or opposite_side_origin_count > 0:
        return "PASS_CONFLICT_UNRESOLVED"
    return "PASS_SOURCE_GEOMETRY_UNRESOLVED"


'''
if helper not in s:
    s=s.replace(marker,helper+marker)

old='''            if same_side_count > 1:
                action_state = "PASS_CONFLICT_UNRESOLVED"
            elif opposite_count > 0:
                action_state = "PASS_CONFLICT_UNRESOLVED"
            else:
                action_state = "PASS_SOURCE_GEOMETRY_UNRESOLVED"
'''
new='''            action_state = action_state_for_candidate(
                same_side_origin_count=same_side_count,
                opposite_side_origin_count=opposite_count,
            )
'''
if old not in s:
    raise SystemExit("action block not found")
s=s.replace(old,new)

# Treat ambiguous terminal before confirmation as fail-closed unknown rather than accidentally active.
old='''            if pre_state == "RUN_COMPLETE":
                base["candidate_state"] = "PASS_RUN_COMPLETED_BEFORE_CONFIRMATION"
                base["action_state"] = "PASS_RUN_COMPLETED_BEFORE_CONFIRMATION"
                terminal_reasons.append("PASS_RUN_COMPLETED_BEFORE_CONFIRMATION")
                event_rows.append(base)
                continue

            consumed_confirmation = favorable_consumed_points(
'''
new='''            if pre_state == "RUN_COMPLETE":
                base["candidate_state"] = "PASS_RUN_COMPLETED_BEFORE_CONFIRMATION"
                base["action_state"] = "PASS_RUN_COMPLETED_BEFORE_CONFIRMATION"
                terminal_reasons.append("PASS_RUN_COMPLETED_BEFORE_CONFIRMATION")
                event_rows.append(base)
                continue
            if pre_state == "AMBIGUOUS_TERMINAL_SAME_BAR":
                base["candidate_state"] = "PASS_UNKNOWN_STATE"
                base["action_state"] = "PASS_UNKNOWN_STATE"
                terminal_reasons.append("PASS_UNKNOWN_STATE")
                event_rows.append(base)
                continue

            consumed_confirmation = favorable_consumed_points(
'''
if old not in s:
    raise SystemExit("pre-state block not found")
s=s.replace(old,new)

p.write_text(s,encoding="utf-8")
print("patched",p)
