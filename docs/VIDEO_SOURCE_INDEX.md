# VIDEO SOURCE INDEX

สถานะ: Working source inventory สำหรับการ reverse-engineer ระบบแม่ปลาปากกาเขียว

หลักการใช้งาน:
- Source label จากผู้ใช้/ญาติ แยกจาก title ที่ตรวจได้จาก YouTube
- ถ้า title/transcript ยังดึงไม่ได้ ให้สถานะ UNVERIFIED และห้ามสรุปกฎจากชื่อไฟล์/บริบทเอง
- Transcript แบบ timestamp ทุก ~8 วินาที ให้ถือเป็นวัตถุดิบหลักสำหรับ Rule Extraction เมื่อผู้ใช้ส่งมา

## Source list from chat (2026-09-01)

| Video ID | URL | Title / Label | Status | Research use |
|---|---|---|---|---|
| oCcG3dUjrgw | https://youtu.be/oCcG3dUjrgw | ผู้ใช้ส่งเดิม; เปิดไม่ได้ในฝั่งญาติ | REPLACED | เก็บไว้เพื่อ trace history; ใช้ jBEM-vWYj_o แทนตามข้อความญาติ |
| jBEM-vWYj_o | https://youtu.be/jBEM-vWYj_o | EP.3 แนวรับ - แนวต้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว | VERIFIED TITLE | สำคัญต่อ support/resistance, body-collection reference zone, left-side candle references |
| ESHDuiVPJow | https://youtu.be/ESHDuiVPJow | EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว | VERIFIED TITLE | Trend vs Frame vs SIG priority |
| UV5NijhjfJ8 | https://youtu.be/UV5NijhjfJ8 | EP.4 เบรก M5 เงินล้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว; ญาติระบุ “อันนี้เป็น การเข้าออเดอร์” | VERIFIED TITLE + USER LABEL | Highest priority for exact M5 break, entry trigger, <=200pt proximity, SL/confirmation |
| a9hPolrjNwU | https://youtu.be/a9hPolrjNwU | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| 16KoS7d-koI | https://youtu.be/16KoS7d-koI | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| vcdN51_OrPE | https://youtu.be/vcdN51_OrPE | EP.พิเศษ ขยี้ให้แหลก #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว; ญาติระบุ “อันนี้สรุป ทั้งหมด” | VERIFIED TITLE + USER LABEL | High-value recap; ใช้ cross-check terminology และ rule conflicts |
| h9gwEq52AWQ | https://youtu.be/h9gwEq52AWQ | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| 1E_PYPor1qQ | https://youtu.be/1E_PYPor1qQ | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| 1QZ8elWm1fM | https://youtu.be/1QZ8elWm1fM | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| CzsnaRh8egw | https://youtu.be/CzsnaRh8egw | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| im3ebGY12j4 | https://youtu.be/im3ebGY12j4 | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| NfdtSc4_A5I | https://youtu.be/NfdtSc4_A5I | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| gdBy24O5DQU | https://youtu.be/gdBy24O5DQU | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| -CZ5laDyzjs | https://youtu.be/-CZ5laDyzjs | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |
| Zila-zxvNx0 | https://youtu.be/Zila-zxvNx0 | ยังไม่ยืนยันชื่อ | UNVERIFIED | ต้องดึง title/transcript ก่อน |

## Immediate gap noted in chat

ญาติ/ผู้ใช้มีคำถามว่า “PAT1 อันไหนนะครับ” แต่จาก metadata ที่ตรวจได้ตอนนี้ยังระบุไม่ได้ว่า video ID ใดในชุดด้านบนเป็นบท PAT1 โดยตรง จึงห้ามเดา ต้อง resolve จาก title/transcript ของรายการ UNVERIFIED หรือคำยืนยันจากญาติ

## Priority transcript extraction order

1. UV5NijhjfJ8 — EP.4 เบรก M5 เงินล้าน / การเข้าออเดอร์
2. vcdN51_OrPE — EP.พิเศษ ขยี้ให้แหลก / สรุปทั้งหมด
3. ESHDuiVPJow — EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig
4. jBEM-vWYj_o — EP.3 แนวรับ-แนวต้าน
5. Resolve PAT1/PAT2/PAT3 source among remaining videos
6. Sideway full lesson
7. Half-retrace / swing-retrace / Fibonacci full lesson

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
