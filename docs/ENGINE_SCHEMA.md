# Engine Schema / State Model

This is a proposed research schema. Fields may exist before the rule that populates them is fully solved.

## 1. Market metadata

```yaml
MarketContext:
  symbol: XAUUSD
  broker: Exness
  server: string
  account_type: string
  timezone: string
  digits: int
  point_size: float
  tick_size: float
  tick_value: float
  chart_price_source: Bid|Ask|Mid
```

No point-distance calculation should run without explicit `point_size`.

---

## 2. Frame object

```yaml
Frame:
  frame_id: string
  frame_type: MAE_PLA_STAT|POR_CHON_ATH|DAY|SIDEWAY|SUPPORT|RESISTANCE|OTHER
  timeframe: M30|H1|H4|D1|W1
  price: float
  zone_low: float|null
  zone_high: float|null
  created_at: datetime
  source_candle_ids: [string]
  evidence_level: A|B|C|D
  confidence: float|null
  active: bool
  invalidation_reason: string|null
```

---

## 3. PA / PAT event

```yaml
PAEvent:
  pa_id: string
  direction: BUY|SELL
  pat_type: PAT1|PAT2|PAT3|UNKNOWN
  timeframe: string
  candle_ids: [string]
  location_frame_id: string|null
  near_frame_distance_points: float|null
  pattern_complete_at: datetime|null
  invalidated_at: datetime|null
  invalidation_reason: string|null
  body_collection_required: bool|null
  evidence_level: A|B|C|D
```

Pattern geometry fields should be added only after primary rules are confirmed.

---

## 4. SIG object

```yaml
SIGEvent:
  sig_id: string
  direction: BUY|SELL
  timeframe: H1|H4|D1|W1|OTHER
  pa_id: string
  sig_start_time: datetime
  sig_confirm_time: datetime|null
  anchor_candle_id: string|null
  anchor_price: float|null
  anchor_kind: POST_SIG_WICK
  normal_run_points: float|null
  target_1x_price: float|null
  target_2x_price: float|null
  completed_1x_at: datetime|null
  completed_2x_at: datetime|null
  extreme_price: float|null
  extreme_at: datetime|null
  status: PENDING|ACTIVE|TP_COMPLETE|OVERRUN|BROKEN|RETRACING|DONE
  evidence_level: A|B|C|D
```

For the directly-confirmed PA BUY PAT2 example, the anchor candle is candle #3. Do not globally encode that for other PATs yet.

---

## 5. Body collection object

```yaml
BodyCollectionZone:
  zone_id: string
  source_timeframe: H4|H1|M30|OTHER
  source_candle_ids: [string]
  structure_label: string|null
  zone_low: float|null
  zone_high: float|null
  direction: BUY|SELL|null
  status: IDENTIFIED|TOUCHED|COLLECTING|COMPLETE|INVALID
  completed_at: datetime|null
  reused: bool
  evidence_level: A|B|C|D
```

Exact geometry is intentionally unresolved.

---

## 6. Retracement object

```yaml
RetracementEvent:
  retrace_id: string
  parent_sig_id: string
  retrace_type: HALF|SWING|UNKNOWN
  direction_of_parent_run: BUY|SELL
  start_price: float
  extreme_price: float
  midpoint_price: float
  opposite_pa_present: bool|null
  opposite_pa_id: string|null
  reference_created_at: datetime
  midpoint_touched: bool|null
  status: REFERENCE_ONLY|ACTIVE|INVALID|COMPLETE
  evidence_level: A|B|C|D
```

Current confirmed arithmetic:

```text
midpoint_price = (start_price + extreme_price) / 2
```

Classification hypothesis supported by direct relative explanation:

```text
if overrun and opposite PA drives pullback:
    type = HALF
    start = post-SIG wick
elif overrun and no opposite PA:
    type = SWING
    start = qualifying candle wick
```

The `qualifying candle` rule is unresolved.

---

## 7. Multi-timeframe context

```yaml
TFContext:
  timestamp: datetime
  m5_direction: BUY|SELL|NEUTRAL|UNKNOWN
  m15_direction: BUY|SELL|NEUTRAL|UNKNOWN
  m30_direction: BUY|SELL|NEUTRAL|UNKNOWN
  h1_sig_id: string|null
  h4_sig_id: string|null
  d1_sig_id: string|null
  w1_sig_id: string|null
  relationship_status: ALIGNED|CONFLICT|PARTIAL|UNKNOWN
```

The algorithm that determines each lower-TF direction remains unresolved.

---

## 8. Trade setup object

```yaml
TradeSetup:
  setup_id: string
  direction: BUY|SELL
  frame_id: string|null
  pa_id: string|null
  sig_id: string|null
  body_zone_id: string|null
  retrace_id: string|null
  distance_to_frame_points: float|null
  lower_tf_confirmed: bool|null
  entry_trigger: string|null
  entry_price: float|null
  sl_reference_price: float|null
  sl_price: float|null
  tp_reference_price: float|null
  tp_price: float|null
  status: WATCH|READY|TRIGGERED|SKIPPED|INVALID|CLOSED
  skip_reason: string|null
  evidence_level: A|B|C|D
```

Execution must stay disabled while entry/SL rules remain unresolved.

---

## 9. Proposed state machine

```text
UNKNOWN
  ↓ frame/cycle identified
SIDEWAY
  ↓ valid PA/SIG at valid location + sideway completion/break rule (UNRESOLVED)
SIG_ACTIVE
  ↓ run from SIG anchor
RUNNING
  ↓ normal run completed
TP_COMPLETE
  ├─→ if run continues: OVERRUN
  └─→ if rest begins: RETRACING

OVERRUN
  ├─→ opposite PA drives retrace: HALF_RETRACE
  └─→ no opposite PA: SWING_RETRACE

HALF_RETRACE / SWING_RETRACE
  ↓ completion / new setup condition (UNRESOLVED)
SIDEWAY or NEW_SIG
```

---

## 10. Replay/backtest event record

Every replay decision should persist:

```yaml
DecisionRecord:
  timestamp: datetime
  visible_data_until: datetime
  detected_frames: [string]
  detected_pa: [string]
  active_sigs: [string]
  cycle_state: string
  candidate_setups: [string]
  action: NO_TRADE|WATCH|ENTER|EXIT|INVALIDATE
  rule_ids_fired: [string]
  evidence_levels: [A|B|C|D]
  future_data_used: false
```

The engine should reject a production backtest if a trade depends on a Level C/D rule unless the experiment explicitly enables hypothesis testing.