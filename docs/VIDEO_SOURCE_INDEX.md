# VIDEO SOURCE INDEX

สถานะ: Working source inventory สำหรับการ reverse-engineer ระบบแม่ปลาปากกาเขียว

หลักการใช้งาน:
- Source label จากผู้ใช้/ญาติ แยกจาก title ที่ตรวจได้จาก YouTube
- ถ้า title/transcript ยังดึงไม่ได้ ให้สถานะ UNVERIFIED และห้ามสรุปกฎจากชื่อไฟล์/บริบทเอง
- Transcript แบบ timestamp ทุก ~8 วินาที ให้ถือเป็นวัตถุดิบหลักสำหรับ Rule Extraction เมื่อผู้ใช้ส่งมา

## Source list from chat (2026-09-01)

| Video ID | URL | Title / Label | Status | Research use |
|---|---|---|---|---|
| NwMl2cUMb-A | https://youtu.be/NwMl2cUMb-A | ผู้ใช้ส่งซ้ำหลังจากมี primary slide PA; บริบทผูกกับพื้นฐานระบบ/PA | USER-SUPPLIED; transcript ถูกใช้ใน PA/PAT forensic รอบก่อน | PA/PAT qualification / anchor / invalidation cross-check |
| oCcG3dUjrgw | https://youtu.be/oCcG3dUjrgw | ผู้ใช้ส่งเดิม; เปิดไม่ได้ในฝั่งญาติ | REPLACED | เก็บไว้ trace history; ใช้ jBEM-vWYj_o แทนตามข้อความญาติ |
| jBEM-vWYj_o | https://youtu.be/jBEM-vWYj_o | EP.3 แนวรับ - แนวต้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว | VERIFIED TITLE | support/resistance, body-collection reference zones |
| ESHDuiVPJow | https://youtu.be/ESHDuiVPJow | EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว | VERIFIED TITLE | Trend vs Frame vs SIG priority |
| UV5NijhjfJ8 | https://youtu.be/UV5NijhjfJ8 | EP.4 เบรก M5 เงินล้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว; ญาติระบุ “อันนี้เป็น การเข้าออเดอร์” | VERIFIED TITLE + USER LABEL | M5 brake / entry cross-check; ยังมีค่าเพื่อเทียบกับ transcript 16KoS7d-koI |
| a9hPolrjNwU | https://youtu.be/a9hPolrjNwU | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| 16KoS7d-koI | https://youtu.be/16KoS7d-koI | **Primary transcript supplied: บทขยี้จุดเข้า M1/M5 / เบรก M5**; transcript พูดคำว่า “เบรก M5 เงินล้าน” และสอน 5-step candle-force / retest / ยืนกรอบ | **PRIMARY TIMESTAMP TRANSCRIPT AVAILABLE (0:00–~1:53:52); exact public title not independently verified** | **P0 discovery largely closed for M5 brake / entry / frame-standing.** Forensic: `docs/M5_BRAKE_TRANSCRIPT_FORENSICS_2026-09-01.md` |
| vcdN51_OrPE | https://youtu.be/vcdN51_OrPE | EP.พิเศษ ขยี้ให้แหลก #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว; ญาติระบุ “อันนี้สรุป ทั้งหมด” | VERIFIED TITLE + USER LABEL | High-value recap; cross-check terminology/rule conflicts |
| h9gwEq52AWQ | https://youtu.be/h9gwEq52AWQ | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| 1E_PYPor1qQ | https://youtu.be/1E_PYPor1qQ | ผู้ใช้ระบุโดยตรงว่า P1 / PAT1 | USER-CONFIRMED LABEL; TITLE UNVERIFIED | PAT1 dedicated geometry source candidate |
| 1QZ8elWm1fM | https://youtu.be/1QZ8elWm1fM | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| CzsnaRh8egw | https://youtu.be/CzsnaRh8egw | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| im3ebGY12j4 | https://youtu.be/im3ebGY12j4 | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| NfdtSc4_A5I | https://youtu.be/NfdtSc4_A5I | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| gdBy24O5DQU | https://youtu.be/gdBy24O5DQU | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| -CZ5laDyzjs | https://youtu.be/-CZ5laDyzjs | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| Zila-zxvNx0 | https://youtu.be/Zila-zxvNx0 | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |

## PAT source resolution

- Strongest current taxonomy: `PAT1`, `PAT2`, `PAT3 variant 1`, `PAT3 variant 2`, `PAT3 variant 3`; no primary support for separate PAT4/PAT5 families.
- Post-SIG reference index: PAT1=#2, PAT2=#3, PAT3=#4.
- PAT1 dedicated source: `1E_PYPor1qQ` — user-confirmed P1 label.
- PA/PAT foundational evidence has been materially extracted from supplied transcript + primary slide; remaining problem is exact quantitative geometry.

## M5 / entry source resolution

Primary transcript `16KoS7d-koI` now directly supports:

- zone first, then brake/pattern search;
- M1 and M5 same abstract pattern logic;
- five logical stages: `ใหญ่ยาว → อ่อนแรง → Reject → เปลี่ยนสี → Retest`;
- stages 2/3/4 may combine in one candle;
- first brake is higher-risk; phase-2/retest entry is preferred;
- structural retest definition;
- frame-standing count begins at first frame touch and commonly uses 4–10 candles;
- body-standing primary, wick-on-line secondary;
- local structure confirmation (higher-low/lower-high / prior high-low destruction);
- overlap / false first brake / reevaluation;
- frame-brake entry is distinct from SIG entry;
- M5 is safer/less noisy than M1; M1 uses trendline/structure refinement.

See `docs/M5_BRAKE_TRANSCRIPT_FORENSICS_2026-09-01.md` and `docs/ANALYST_GAP_REVIEW_M5_BRAKE_2026-09-01.md`.

## Priority transcript extraction order — updated

1. PAT3 detailed geometry / close-up candle lesson.
2. Dedicated Sideway frame construction/completion lesson.
3. Half-retrace / swing-retrace / Fibonacci full lesson.
4. Multi-timeframe authority/conflict lesson.
5. `vcdN51_OrPE` recap for conflict checking.
6. `UV5NijhjfJ8` M5 lesson as cross-check against the now-extracted 16Ko transcript.
7. Remaining unverified IDs: identify title/transcript before assigning system rules.

## Transcript rule-extraction format

For each ~8-second segment:
- Video ID / source label
- Timestamp start-end
- Exact system term used
- Rule candidate
- Input timeframe / context
- Trigger / condition
- Output / action
- Example vs general rule
- Invalidation / exception
- Confidence: CONFIRMED / PARTIAL / INFERENCE / UNKNOWN
- Conflict with prior rulebook if any

Do not promote instructor performance claims, win-rate claims, or anecdotal probabilities into strategy statistics without independent backtest evidence.
