# Phase 1 Exness XAUUSDm Tick Archive Sample Validation — 2026-09-14

Status: EXTERNAL HISTORICAL BID/ASK ROUTE SAMPLE VALIDATED / PROVENANCE BOUNDARY OPEN / NO OUTCOME SCORING

## Purpose

Validate a real historical Bid/Ask tick route for Phase 1 before constructing any synthetic spread or execution-cost model.

This checkpoint uses September 2022, an already-inspected discovery-era period. It does not access or score protected holdout outcomes.

## Evidence classification

### Source statements — Exness

Exness public Tick History states that:

- historical tick data is drawn from Exness real-time pricing;
- downloaded reports contain all ticks for the selected instrument/period, including Bid and Ask;
- suffix `m` denotes Standard accounts, with `XAUUSDm` given as the example.

Source:
- https://www.exness.com/tick-history/

Exness Help Center additionally states that:

- tick history is available as CSV inside ZIP files;
- the schema is `"Exness","Symbol","Timestamp","Bid","Ask"`;
- older periods are exposed as monthly or annual downloads;
- Standard / Standard Cent / Pro tick history is drawn from MetaTrader 4 Real 1;
- the user cannot choose the source trading server;
- prices across servers may differ slightly because of latency/time deviations.

Source:
- https://get.exness.help/hc/en-us/articles/360021547851-How-to-use-tick-history

Interpretation:

The Exness archive is a strong broker-family historical pricing reference, but the source statement itself does **not** establish exact identity with the Project's current Exness Demo / Standard-demo / MT5 runtime.

## Runtime discovery — archive endpoint

A machine-side archive endpoint was discovered from a secondary technical reference and then probed directly:

`https://ticks.ex2archive.com/ticks/`

Runtime observations on 2026-09-14:

- HTTP access succeeded from the Owner machine;
- the root listing contains `XAUUSDm`;
- `XAUUSDm` exposes year directories 2015 through 2026;
- `XAUUSDm/2022/` exposes months 01 through 12 plus `Exness_XAUUSDm_2022.zip`;
- the 2022 annual ZIP listing reports 256,694,870 bytes;
- `XAUUSDm/2022/09/` exposes `Exness_XAUUSDm_2022_09.zip`;
- the September ZIP listing reports 22,115,588 bytes.

Important provenance boundary:

The endpoint is Exness-branded and the retrieved data matches Exness's documented CSV schema, but this checkpoint did not runtime-prove that the current Exness website UI itself resolves downloads to this exact endpoint because the browser path was stopped by a Cloudflare human-verification challenge.

Therefore classify the endpoint as:

`EXNESS_BRANDED_ARCHIVE_ENDPOINT_RUNTIME_VALIDATED_FIRST_PARTY_LINKAGE_NOT_RUNTIME_PROVEN`

Do not silently upgrade that classification.

## Downloaded sample

Requested object:

`https://ticks.ex2archive.com/ticks/XAUUSDm/2022/09/Exness_XAUUSDm_2022_09.zip`

Local path, gitignored:

`data/raw/exness_tick_history/samples/Exness_XAUUSDm_2022_09.zip`

Observed:

- ZIP bytes: 22,115,588
- SHA-256: `42cb9465597f9ec6a330a93dbd093ad319d0afd51b8186a4824c0c7e21f3a828`
- ZIP integrity test: PASS
- member: `Exness_XAUUSDm_2022_09.csv`
- uncompressed CSV bytes: 151,615,162
- header: `Exness, Symbol, Timestamp, Bid, Ask`

## Full-month streaming validation

All CSV rows were scanned; this is not a small-row sample check.

Observed rows:

- total ticks: 2,377,326
- first tick: 2022-09-01 00:00:00.202Z
  - Bid 1708.919
  - Ask 1709.119
- last tick: 2022-09-30 20:57:55.790Z
  - Bid 1660.963
  - Ask 1661.163
- distinct UTC calendar dates represented: 26

Data-quality counters:

- symbol mismatch: 0
- provider/source-field mismatch: 0
- Ask < Bid: 0
- non-finite Bid/Ask: 0
- timestamp regression: 0
- consecutive equal timestamp: 0
- consecutive exact duplicate row: 0

These checks do **not** prove every expected market tick is present. They establish internal consistency of this downloaded month.

## Observed spread distribution — September 2022 only

Derived as `Ask - Bid` over every row:

- minimum: approximately 0.200
- mean: approximately 0.213872
- median / p50: 0.200
- p95: 0.200
- p99: 0.600
- maximum: approximately 1.077
- distinct spread values after rounding to 1e-6: 217

Classification:

`OBSERVED_SAMPLE_DISTRIBUTION`

This is **not**:

- a universal Exness spread;
- a replay constant;
- a threshold;
- a target;
- proof of future spread behavior.

## What is now known

### KNOWN NOW

- A working machine-accessible archive route exists for `XAUUSDm`.
- The live directory listing exposes `XAUUSDm` years 2015–2026.
- One full monthly file was downloaded and structurally validated.
- The file contains millisecond UTC timestamps plus Bid and Ask.
- The sample provides directly observed historical spread rather than a fabricated constant.

### NOT YET ESTABLISHED

- complete month-by-month/year-by-year coverage continuity across 2015–2026;
- whether every expected tick is present inside each archive;
- exact first-party linkage between the current Exness website download UI and `ticks.ex2archive.com`;
- exact equivalence between archive pricing and the current Exness Demo / MT5 server;
- historical slippage/fill behavior;
- commissions or other account-level transaction economics;
- stop-fill convention and replay fill convention;
- universal spread model.

## Effect on the prior acquisition probe

The earlier checkpoint
`docs/PHASE1_EXECUTION_DATA_ACQUISITION_PROBE_2026-09-14.md`
correctly preserved two failures at the time:

- MT5 terminal authorization failed during that earlier probe;
- direct raw Dukascopy tick access failed over the local network.

Those observations remain historical facts.

Later evidence supersedes only the old operational conclusion that no local real Bid/Ask acquisition route had yet been closed.

Current replacement conclusion:

`EXTERNAL_XAUUSDM_BID_ASK_ROUTE_SAMPLE_VALIDATED_MULTIYEAR_COVERAGE_MAPPING_PENDING`

## Next bounded technical steps

1. Build/reuse a restart-safe Exness archive coverage mapper before any multi-year bulk download.
2. Map available XAUUSDm year/month objects and file metadata without assuming continuity.
3. Validate representative files and preserve hashes/provenance.
4. Cross-validate an already-inspected overlapping 2026 interval against the current MT5 XAUUSDm tick route.
5. Keep archive feed identity separate from the current MT5 runtime identity.
6. Only after observed coverage is understood, decide whether any residual synthetic execution model is necessary.
7. Freeze replay fill/stop/cost conventions before outcome scoring.

Automatic order sending remains disabled.

Protected holdout scoring remains disabled.
