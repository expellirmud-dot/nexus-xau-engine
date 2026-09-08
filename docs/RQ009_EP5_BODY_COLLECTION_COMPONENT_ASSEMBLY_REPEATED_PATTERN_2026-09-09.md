# RQ-009 — EP.5 Body Collection Component Assembly Repeated Pattern

Date: 2026-09-09
Source: original YouTube EP.5 `oCcG3dUjrgw` rendered Show transcript + synchronized original-video visual evidence
Status: PARTIAL_SOURCE_VISUAL_CLOSURE — ALL_COMPONENTS_REQUIRED / TWO_REFERENCES_REPEATED / UNIVERSAL_THREE_TO_TWO_REDUCTION_UNRESOLVED

## Research question

When EP.5 requires `ซอก + ไส้ + คู่` but teaches two forecast references/zones, does the source define a deterministic universal rule that reduces three component prices into two projected references?

This checkpoint is source-first. Historical trade outcomes are not used to choose a component mapping, equality tolerance, candidate winner, or zone boundary.

## Source facts

### Worked PA Sell example — ~49:44–51:27

The instructor starts the Body Collection placement and identifies all three ingredients in sequence:

- ~49:44–49:55: first placement has `ซอก`; the instructor points to the red-candle junction.
- ~49:55–50:04: `ไส้` is identified.
- ~50:04–50:12: `คู่` is identified, followed by the statement that all three are present/complete (`3 อัน ... ครบถ้วนไม่มีขาด`).
- ~50:12–50:20: the resulting construction is taught as forecast reference/zone `1` and `2`.
- ~50:42–51:18: price may react at reference 1, reference 2, or between them; the zone is explicitly a forecast area and not a dead/fixed price.
- ~51:27: zone arrival still requires PA confirmation.

Prior synchronized visual closure for this same worked example shows `ซอก` and `คู่` on the same upper reference around `3563.59`, while a distinct wick-derived reference is around `3560.31`. In this shown case the three named structural ingredients therefore collapse naturally to two unique reference levels because at least two ingredients share a level.

### Independent M30 example — ~1:01–1:03

The instructor searches farther back after the initially visible M30 structure has only a wick, then explicitly identifies `ซอก`, `ไส้`, and `คู่` and says the set is complete. The instructor then marks `1` and `2` and describes the later reaction as reaching the forecast Body Collection area.

This independently repeats the sequence:

`find complete ซอก+ไส้+คู่ structure -> mark two forecast references 1/2`.

The transcript does not state an OHLC transformation that maps three distinct component prices to those two references.

### Q&A — ~1:06:35–1:07:15

A direct question asks whether the wick merely indicates the distance between zones. The instructor answers no and repeats that it must all be drawn/marked (`มันต้องตีทั้งหมดเลยค่ะ`). Immediately afterward the source again describes two forecast lines/references.

Safe implication: `ไส้` is not merely an auxiliary spacing measurement. The components are structural inputs that must be considered in the taught construction.

### BUY/SELL mirror examples — ~1:12:35–1:14:09

- ~1:12:35–1:12:52: a PA Buy PAT3 example is marked with two Body Collection forecast points/references `1` and `2`.
- ~1:12:57–1:13:16: a PA Sell PAT2 example is also marked with two points/references; synchronized video shows the two horizontal projected lines and the instructor identifies wick/nook structure.
- ~1:13:47–1:14:09: another worked construction explicitly states that it has `ซอก`, `ไส้`, and `คู่`, then calls the result a zone.

This confirms that the two-reference construction is repeated on both BUY and SELL sides rather than being unique to the first PA Sell example.

## Visual observations

### M30 ~1:02

The synchronized chart contains two horizontal reference lines around the selected historical structure while the instructor annotates the source candles. The image supports the existence of two projected levels, but the visible annotations are not sufficient to derive a universal one-to-one component mapping for every `ซอก/ไส้/คู่` combination.

### BUY ~1:12:45–1:12:52

The original-video frame visibly labels two projected points, `1` and `2`, around the PA Buy PAT3 structure. This is direct BUY-side visual support for the two-reference topology.

### SELL ~1:13:05–1:13:41

The original-video frame visibly labels two projected points, `1` and `2`, around the PA Sell PAT2 structure. The instructor then annotates a wick and nook around the historical structure. This is direct SELL-side visual support for the same topology, but it still does not expose a universal formula for a hypothetical case where all three component prices are distinct.

## Source-backed closure

The repeated EP.5 pattern can now be stated safely as:

1. `ซอก + ไส้ + คู่` are required structural ingredients in the taught Body Collection construction.
2. `ไส้` is not merely a spacing helper; the source explicitly says the construction must mark/consider all of it.
3. The current teaching repeatedly outputs two forecast references/levels (`1`, `2`) on PA Sell, PA Buy, and M30 examples.
4. One synchronized worked PA Sell example demonstrates a natural collapse to two unique levels because `ซอก` and `คู่` share one reference while the wick supplies the other.
5. The source reviewed so far does **not** define a universal deterministic `three component prices -> two reference prices` reduction rule for a case in which `ซอก`, `ไส้`, and `คู่` would all resolve to three distinct normalized prices.

## Analyst-derived representation — permitted only as partial research structure

A safe detector representation is therefore:

- enumerate source-compatible `ซอก`, `ไส้`, and `คู่` component candidates;
- preserve their normalized reference prices and provenance separately;
- preserve all valid candidate clusters rather than forcing a winner;
- if a source-reviewed cluster naturally contains only two unique reference levels because component levels coincide, represent those two levels as the shown-form forecast pair;
- if three distinct component levels remain, classify the assembly as `UNRESOLVED_THREE_TO_TWO` rather than inventing a merge/rank rule.

This representation is an analyst research structure. It is **not** a claim that the instructor explicitly taught a generic unique-price-collapse algorithm.

## What remains unknown

- Universal `ซอก/ไส้/คู่ -> reference 1/reference 2` mapping when all three component prices differ.
- Universal wick-selection rule across all BUY/SELL variants.
- Broker-feed equality/tolerance needed to decide whether two component prices are "the same" machine-wise.
- Same-timeframe multi-cluster winner priority.
- Exact OHLC transition that retires a touched zone as completed/used.
- Exact broker fill price after lower-timeframe confirmation.

## Decision

Result: `PARTIAL_SOURCE_VISUAL_CLOSURE`.

The source is now strong enough to freeze `ALL_COMPONENTS_REQUIRED` and `TWO_FORECAST_REFERENCES_REPEATED`, including a demonstrated natural two-level collapse in one worked example. It is not strong enough to freeze a universal three-to-two reduction formula. Therefore `UNIVERSAL_ZONE_ASSEMBLY` remains open and must not be selected from backtest performance.

Raw transcript/screenshots remain local under `youtube/_evidence/oCcG3dUjrgw/` and are not committed.
