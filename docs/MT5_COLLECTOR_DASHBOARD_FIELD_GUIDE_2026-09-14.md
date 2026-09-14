# MT5 Collector Dashboard Field Guide — 2026-09-14

Status: USER STUDY GUIDE
Scope: MT5 forward data collection / observability
Trading authority: NONE
Mode: READ-ONLY DATA / ORDER SEND DISABLED

## หลักสำคัญ

ค่าบน dashboard มี 2 กลุ่ม:

1. **Infrastructure / data-quality** — บอกว่าโปรแกรมและข้อมูลทำงานถูกต้องไหม
2. **Market observation** — ข้อมูลตลาดที่อาจนำไปศึกษาความสัมพันธ์ต่อได้

ไม่มีค่าใดในหน้านี้เป็น BUY/SELL signal โดยอัตโนมัติ

## READ_ONLY_DATA_ORDER_SEND_DISABLED

ประเภท: Safety state

หมายถึง collector อ่านข้อมูล MT5 และเขียนไฟล์/ฐานข้อมูลได้ แต่ไม่ส่ง แก้ หรือปิด Order

ใช้ยืนยันว่า process นี้เป็น data layer ไม่ใช่ execution layer

## Collector

ค่าที่พบได้:
- STARTING
- BACKFILLING
- RUNNING
- STOPPED
- BLOCKED
- ERROR

RUNNING = กำลังทำงาน
BACKFILLING = กำลังดึงช่วงที่ขาดหลัง restart
STOPPED = หยุดอย่างปกติ
BLOCKED = ตั้งใจไม่ทำต่อ เช่น source identity เปลี่ยน
ERROR = acquisition/runtime error

ประเภท: Infrastructure state
ไม่ใช่ signal ซื้อขาย

## Symbol

ตัวอย่าง: XAUUSDm

เป็นชื่อ symbol จริงของ broker/MT5 route นี้
suffix เช่น m เป็น broker-specific

อย่าถือว่า XAUUSDm จาก feed นี้เท่ากับ XAUUSD จากทุก broker ในเรื่อง execution evidence

## Bid / Ask

ประเภท: Direct market observation

Bid = quote ฝั่งที่เกี่ยวกับการขายเข้าสู่ตลาด
Ask = quote ฝั่งที่เกี่ยวกับการซื้อจากตลาด

collector เก็บ raw Bid/Ask ticks จริง ส่วน dashboard แสดงคู่ล่าสุด

มีคุณค่าต่อ research สูง แต่ไม่ใช่ standalone signal

## Spread

คำนวณ:

Spread = Ask - Bid

ประเภท: Derived market observation

อาจใช้ศึกษาความสัมพันธ์ เช่น:
- spread ขยาย/หดเมื่อ setup บางชนิดเกิดไหม
- ต่างกันตามเวลา/regime หรือไม่
- spread เปลี่ยนก่อนหรือหลัง quote movement
- execution condition แย่ลงในช่วงไหน

ยังไม่มี universal spread threshold

## Latest tick UTC

เวลาของ tick ล่าสุดที่ถูก commit

ประเภท: Market-data timestamp

ใช้ align กับ:
- 07:00 Asia/Bangkok
- OHLC
- source event
- confirmation
- replay chronology

ไม่ใช่ signal

## Tick age

คำนวณคร่าว ๆ:

เวลาปัจจุบัน - latest tick timestamp

ประเภท: Data freshness metric

ถ้าสูง อาจเกิดจาก:
- ไม่มี tick ใหม่
- session/market inactivity
- feed/MT5 ช้า
- collector หยุด
- pipeline delay

ดังนั้น Tick age สูงไม่ได้พิสูจน์ว่าระบบเสียทันที

## Ticks in DB

จำนวน raw tick rows ทั้งหมดใน:

data/raw/mt5/XAUUSDm_ticks.sqlite3

ไม่ใช่จำนวน trades, signals หรือ candles

ใช้ดูว่าหลักฐาน broker-specific สะสมไปเท่าไร

## This session

จำนวน tick rows ที่ commit ตั้งแต่ process รอบปัจจุบันเริ่ม

restart แล้วค่านี้เริ่มนับใหม่
แต่ Ticks in DB สะสมต่อ

ใช้วิเคราะห์ activity / recovery ของ collector

## Gaps

ตัวอย่าง:

{}

หมายถึง clean database ปัจจุบันไม่มี explicit gap/error records

สำคัญ:
ช่วงที่ MT5 คืน 0 ticks ไม่ถูกเรียก gap อัตโนมัติ เพราะอาจเป็น session/holiday/no-event

สถานะที่ contract รองรับ เช่น:
- RECOVERED
- PENDING_SESSION_CONTEXT
- UNRECOVERABLE_CURRENT_ROUTE
- API_ERROR

## Last commit UTC

เวลาที่ software commit data/state ลง SQLite สำเร็จล่าสุด

ต่างจาก Latest tick UTC:

- Latest tick = เวลาของ market observation
- Last commit = เวลาที่โปรแกรม persist สำเร็จ

ใช้ตรวจ pipeline delay

## Source

ค่าที่เห็นเป็น hash เช่น:

2017aa577e132c4e...

เป็น provenance identity จากข้อมูล non-secret เช่น:
- broker/company
- server
- trade mode
- currency
- symbol
- digits
- point
- contract size

ใช้กันการเอาข้อมูลจาก feed คนละแหล่งมาปนกันแบบเงียบ ๆ

ไม่เก็บ password/token ใน identity นี้

## Last error

NONE = ไม่มี error ปัจจุบัน

ถ้ามี error ต้องตรวจช่วงข้อมูลที่เกี่ยวข้องก่อนนำไปใช้ research/replay

## ค่าไหนอาจนำไปศึกษาตรรกะ BUY/SELL ต่อได้?

**ไม่ควรใช้เป็น signal:**
- Collector
- Tick age
- Ticks in DB
- This session
- Gaps
- Last commit
- Source
- Last error
- READ_ONLY state

กลุ่มนี้บอกคุณภาพของ evidence pipeline

**Market inputs ที่ศึกษาได้:**
- Bid
- Ask
- Spread
- ลำดับเวลา tick
- ความถี่/ความเร็วของ quote changes

ตัวแปร derived ที่อาจศึกษาในอนาคต:
- spread distribution ตามเวลา/regime
- quote-change velocity
- tick activity rate
- short-window movement magnitude
- spread expansion/contraction
- micro-volatility
- lag/lead กับปัจจัย Phase 1 เดิม

ทั้งหมดนี้เป็น research candidates ไม่ใช่ canonical signal

## วิธีศึกษาความสัมพันธ์

ใช้แนวทาง Project:

setup/state เปลี่ยน
→ Bid/Ask เปลี่ยนไหม
→ Spread เปลี่ยนไหม
→ activity/velocity เปลี่ยนไหม
→ พร้อมกันหรือล่าช้า
→ direction/magnitude เป็นอย่างไร
→ condition ไหน relation หาย
→ falsify ได้อย่างไร

representation ต้อง freeze ก่อนดู protected outcome

ห้ามสร้าง threshold ย้อนหลังจากผลที่ดูดี

## ข้อจำกัด

Raw Bid/Ask quote ticks ไม่ได้พิสูจน์ว่าใครเป็น buyer/seller ที่แท้จริงใน market

ปัจจุบัน XAUUSDm route นี้ยังไม่มี proven full order book

ดังนั้น quote movement = observation evidence
ไม่ใช่ proof ของ hidden buying/selling intent

## Safety boundary

collector/dashboard = evidence system

แยกจาก:
- BUY/SELL decision generation
- sizing
- execution
- automatic trading

ถ้าอนาคต research รองรับ decision representation ให้สร้างเป็น layer ใหม่แยกจาก collector
