# Transcript Evidence Register

Status: active research
Updated: 2026-09-01

Purpose: เก็บหลักฐานจากข้อความถอดเสียงวิดีโอแบบ timestamp โดยแยกคำพูดต้นทางออกจาก inference และ rule candidate เพื่อใช้สร้างกฎ deterministic สำหรับ Backtest/Detector/Replay Engine

## Source T1 — คลาส “เก็บบอดี้” (transcript แบบ timestamp)

### Confirmed source-derived observations

1. Candle-close rule
- 17:21–18:43: ผู้สอนย้ำว่า หากใช้ TF ใด ต้องรอให้แท่งของ TF นั้นจบก่อน เช่น M1 ต้องจบ 1 นาที, M5 ต้องจบ 5 นาที, M15 ต้องจบ 15 นาที และห้ามคาดเดารูปทรงก่อนแท่งปิด
- Rule candidate: `evaluate_signal_only_on_closed_bar = true`
- Confidence: HIGH (direct transcript)

2. ซอก–ไส้–คู่ เป็นองค์ประกอบหลักของ “เก็บบอดี้”
- 19:41–20:16: ผู้สอนระบุคีย์สำคัญ 3 อย่างคือ “ซอก / ไส้ / คู่” และบอกว่าสามอย่างรวมกันกลายเป็นแนวรับหรือแนวต้านในโซน
- 20:33–22:43: “ซอก” ถูกอธิบายว่าเป็นรอยต่อ/ข้อต่อระหว่างราคาปิดกับราคาเปิดของแท่งสีเดียวกัน ซึ่งเป็นราคาเดียวกัน และอาจทำหน้าที่เป็นแนวรับ/แนวต้านเมื่อกราฟสลับฝั่ง
- 23:49–25:33: “ไส้” คือ wick ของแท่งเทียน เกิดจากการดันราคาแล้วถูกย้อนกลับ; ความยาวขึ้นกับหน้างานและต้องรอแท่งจบก่อนจึงรู้
- Rule candidates: สร้าง object `BodyCollectionZone` จาก anchors ประเภท `notch`, `wick`, `pair`
- Confidence: HIGH สำหรับนิยามเชิงภาษาจาก transcript; LOW/MEDIUM สำหรับสูตร OHLC exact เพราะ “คู่” ยังต้องสกัดละเอียดเพิ่ม

3. Multi-timeframe use of body-collection structures
- 25:01–25:24: ซอก–ไส้–คู่ใช้ได้ทุก TF; ถ้าใช้ H4 ก็หาเก็บบอดี้ H4, ใช้ Day ก็หาใน Day, ใช้ M5 ก็หาใน M5
- 59:27–59:52: ตัวอย่าง M5 เกิด PA Sell หลังราคามาถึง “ระยะคาดการณ์” ที่ตีจากซอก–ไส้–คู่ของ H4 และหากหา H4 ไม่เจอ ให้ย่อยไปดูอีก 1 TF
- Rule candidate: `anchor_tf = requested_context_tf`; if no valid H4 anchor, inspect one lower TF (exact lower-TF mapping still UNKNOWN)
- Confidence: HIGH for workflow; MEDIUM for deterministic fallback mapping

4. PA + forecast zone interaction
- 59:27–59:52: M5 เกิด PA Sell หลังราคามาถึงระยะคาดการณ์ที่สร้างจากซอก–ไส้–คู่ H4
- 1:25:27–1:25:36: ถ้ามี PA ผู้สอนกล่าวว่าจะตี “โซนเก็บบอดี้”; ถ้าไม่มี/อีกบริบทหนึ่งสามารถตีแนวรับไว้รอได้
- Rule candidate: PA ไม่ควรถูกประเมินโดดเดี่ยวจากตำแหน่ง; ต้องมี context zone/anchor
- Confidence: MEDIUM-HIGH (direct example, but exact PA morphology not yet extracted)

5. Example of lower-TF confirmation
- 1:21:08–1:21:58: ผู้สอนอธิบาย H4 เป็น PA; H1 มีแท่งที่ Sell ไม่ลงเพราะอยู่แนวรับ; การย้อนของแท่งถัดไปถูก M5 confirm ว่า “ไม่ทำ High สูงขึ้น” แล้วราคาจึงเลือกลง
- Rule candidate (not yet canonical): lower-TF confirmation may include failure to create a higher high in a bearish setup
- Confidence: MEDIUM because this is an example, not yet confirmed as universal rule

6. Support/resistance lines are selective, not every fixed interval
- 1:22:23–1:23:39: ผู้สอนบอกว่าเดิมเคยตีเส้นทุก 500 จุด แต่ภายหลังเลือกตีเฉพาะแนวรับ/ต้านสำคัญ เพราะตีมากทำให้สับสน; กล่าวถึงการใช้กรอบกว้าง 1,000 จุดในภาวะวอลุ่มแรง
- Rule implication: ห้าม hard-code “ทุก 500 จุด = กรอบสำคัญ” เป็นกฎระบบ
- Confidence: HIGH

7. Training/backtest principle
- 1:57:34–1:57:58: ผู้สอนย้ำว่าไม่ควรเชื่อทันที ต้องนำไป Backtest และจดพฤติกรรมเมื่อราคาเข้าโซน
- Implication: rule candidates ที่ยังไม่ deterministic ต้องถูกเก็บเป็น hypothesis และทดสอบกับ labelled examples
- Confidence: HIGH

8. Next class explicitly named
- 1:58:08–1:58:49: ผู้สอนระบุว่าคลาสถัดไปคือ “พักครึ่ง พักสวิง” และจะสอนตี Fibonacci รวมถึง retracement / extension และความหมายของค่าแต่ละค่า
- Research priority: ต้องหา transcript ของคลาสถัดไป เพราะเป็นหลักฐานต้นทางตรงสำหรับช่องว่าง Fibonacci/pพักครึ่ง/พักสวิง
- Confidence: HIGH

## Important conflict corrections

- ยังไม่มีหลักฐานจาก T1 ที่รองรับนิยาม PAT1/PAT2/PAT3 แบบจำนวนแท่งหรือ body ratio ที่เคยถูกเสนอในบทสรุปก่อนหน้า
- ยังไม่มีหลักฐานจาก T1 ว่า PAT1 = single-bar hammer/shooting-star
- ยังไม่มีหลักฐานจาก T1 ว่า PAT1/2/3 = ไส้หลัง SIG อยู่แท่งที่ 2/3/4
- ดังนั้นนิยาม PAT เหล่านี้ต้องคงสถานะ HYPOTHESIS/UNVERIFIED จนกว่าจะพบ transcript ตรง

## Open keyword targets

Priority A:
- ช่องแม่ปลา (exact term / ASR variants)
- เพาะ (exact term / ตรวจว่าเป็นคำจริงหรือ ASR ของ PA/PAT)
- PA / พีเอ / P-A
- PAT1 / PAT2 / PAT3 / PAT4 / PAT5
- SIG / ซิก / signal
- ไส้หลัง SIG
- พักครึ่ง / พักสวิง
- Fibonacci / ฟิโบ / retracement / extension

Priority B:
- เก็บบอดี้
- ซอก / ไส้ / คู่
- ยืน / หลุด / พัง / เบรก
- กรอบ / โซน / รับ / ต้าน
- confirm / ไม่ทำ High / ไม่ทำ Low

## Current deterministic rules safe enough to prototype

```text
R-T1-001: Evaluate candle-derived signals only after the selected timeframe candle has closed.
Status: CONFIRMED

R-T1-002: Body-collection context is built from candle structures called ซอก / ไส้ / คู่ and is used as support/resistance zone context.
Status: CONFIRMED concept; exact OHLC construction UNKNOWN

R-T1-003: PA examples must be interpreted with location/context; at least one direct example shows M5 PA Sell at a forecast level derived from H4 ซอก–ไส้–คู่.
Status: CONFIRMED example; universal rule not yet proven

R-T1-004: Do not treat every fixed 500-point interval as an important frame/line.
Status: CONFIRMED
```

## Next evidence target

Locate the transcript/video immediately following this class, explicitly announced at 1:58:08 onward as the “พักครึ่ง / พักสวิง / Fibonacci / retracement / extension” lesson, then extract every relevant timestamp into this register before formalizing any Fibonacci rule.
