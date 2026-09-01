# VIDEO SOURCE INDEX

สถานะ: Working source inventory สำหรับการ reverse-engineer ระบบแม่ปลาปากกาเขียว

หลักการใช้งาน:
- Source label จากผู้ใช้/ญาติ แยกจาก title ที่ตรวจได้จาก YouTube
- ถ้า title/transcript ยังดึงไม่ได้ ให้สถานะ UNVERIFIED และห้ามสรุปกฎจากชื่อไฟล์/บริบทเอง
- Transcript แบบ timestamp ทุก ~8 วินาที ให้ถือเป็นวัตถุดิบหลักสำหรับ Rule Extraction เมื่อผู้ใช้ส่งมา

## Source list from chat (2026-09-01)

| Video ID | URL | Title / Label | Status | Research use |
|---|---|---|---|---|
| NwMl2cUMb-A | https://youtu.be/NwMl2cUMb-A | ผู้ใช้ส่งซ้ำหลังจากมี primary slide PA; บริบทก่อนหน้าผูกคลิปนี้กับพื้นฐานระบบ/PA แต่ title จาก YouTube ยังดึงไม่ได้ในรอบปัจจุบัน | USER-SUPPLIED; TITLE/TRANSCRIPT NOT FETCHED | **P0 source candidate for PA/PAT exact qualification.** ใช้เทียบกับสไลด์ที่ยืนยัน PAT1, PAT2, PAT3 v1/v2/v3 และ anchor #2/#3/#4; ต้องดึง transcript ก่อนเลื่อน OHLC thresholds เป็น FACT |
| oCcG3dUjrgw | https://youtu.be/oCcG3dUjrgw | ผู้ใช้ส่งเดิม; เปิดไม่ได้ในฝั่งญาติ | REPLACED | เก็บไว้เพื่อ trace history; ใช้ jBEM-vWYj_o แทนตามข้อความญาติ |
| jBEM-vWYj_o | https://youtu.be/jBEM-vWYj_o | EP.3 แนวรับ - แนวต้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว | VERIFIED TITLE | สำคัญต่อ support/resistance, body-collection reference zone, left-side candle references |
| ESHDuiVPJow | https://youtu.be/ESHDuiVPJow | EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว | VERIFIED TITLE | Trend vs Frame vs SIG priority |
| UV5NijhjfJ8 | https://youtu.be/UV5NijhjfJ8 | EP.4 เบรก M5 เงินล้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว; ญาติระบุ “อันนี้เป็น การเข้าออเดอร์” | VERIFIED TITLE + USER LABEL | Highest priority for exact M5 break, entry trigger, <=200pt proximity, SL/confirmation |
| a9hPolrjNwU | https://youtu.be/a9hPolrjNwU | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| 16KoS7d-koI | https://youtu.be/16KoS7d-koI | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| vcdN51_OrPE | https://youtu.be/vcdN51_OrPE | EP.พิเศษ ขยี้ให้แหลก #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว; ญาติระบุ “อันนี้สรุป ทั้งหมด” | VERIFIED TITLE + USER LABEL | High-value recap; ใช้ cross-check terminology และ rule conflicts |
| h9gwEq52AWQ | https://youtu.be/h9gwEq52AWQ | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| 1E_PYPor1qQ | https://youtu.be/1E_PYPor1qQ | ผู้ใช้ระบุโดยตรงว่า P1 / PAT1 | USER-CONFIRMED LABEL; TITLE UNVERIFIED | Primary source candidate for PAT1 candle-by-candle extraction; ต้องดึง transcript ทุก ~8 วินาทีเพื่อสร้าง deterministic OHLC rule |
| 1QZ8elWm1fM | https://youtu.be/1QZ8elWm1fM | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| CzsnaRh8egw | https://youtu.be/CzsnaRh8egw | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| im3ebGY12j4 | https://youtu.be/im3ebGY12j4 | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| NfdtSc4_A5I | https://youtu.be/NfdtSc4_A5I | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| gdBy24O5DQU | https://youtu.be/gdBy24O5DQU | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| -CZ5laDyzjs | https://youtu.be/-CZ5laDyzjs | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| Zila-zxvNx0 | https://youtu.be/Zila-zxvNx0 | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |

## PAT source resolution

- Pattern taxonomy จาก primary slide ปัจจุบัน: `PAT1`, `PAT2`, `PAT3 variant 1`, `PAT3 variant 2`, `PAT3 variant 3`; ยังไม่มีหลักฐานต้นทางให้สร้าง PAT4/PAT5 แยก
- Generic post-SIG reference index จาก primary slide: PAT1=#2, PAT2=#3, PAT3=#4
- PAT1 dedicated source: `1E_PYPor1qQ` — ผู้ใช้ยืนยันว่า “P1”
- PA/PAT foundational source candidate: `NwMl2cUMb-A` — ผู้ใช้ส่งโดยตรง; ใช้ค้น exact qualification/threshold/invalidation เมื่อมี transcript

## Priority transcript extraction order

1. NwMl2cUMb-A — PA/PAT foundations; P0 เพราะอาจปิด exact qualification ของหลาย PAT พร้อมกัน
2. 1E_PYPor1qQ — PAT1 dedicated source
3. UV5NijhjfJ8 — EP.4 เบรก M5 เงินล้าน / การเข้าออเดอร์
4. vcdN51_OrPE — EP.พิเศษ ขยี้ให้แหลก / สรุปทั้งหมด
5. ESHDuiVPJow — EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig
6. jBEM-vWYj_o — EP.3 แนวรับ-แนวต้าน
7. Sideway full lesson
8. Half-retrace / swing-retrace / Fibonacci full lesson

## PA/PAT extraction checklist

เมื่อได้ transcript ของ `NwMl2cUMb-A` หรือ `1E_PYPor1qQ` ให้หาเฉพาะกฎที่แปลงเป็นโค้ดได้:
- PAT1 Buy/Sell: exact wick/body/location rule
- PAT2 Buy/Sell: exact candle 1/2 relation, body percentage if any, close threshold
- PAT3 variants 1–3: exact distinction and candle-3 completion rule
- body ratio / wick ratio / required colors
- must occur at support/resistance/frame/TP-complete context แบบใด
- pattern completion candle and closed-candle requirement
- invalidation / fake-PA examples
- post-SIG reference candle #2/#3/#4: exact wick side and minimum geometry
- body collection after PAT
- lower-TF M1/M5 confirmation
- entry / SL reference
- negative examples: หน้าตาคล้าย PAT แต่ใช้ไม่ได้

## Transcript rule-extraction format

For each ~8-second segment:
- Video ID / title
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

Do not promote instructor performance claims or anecdotal win-rate statements into strategy rules without independent evidence.
