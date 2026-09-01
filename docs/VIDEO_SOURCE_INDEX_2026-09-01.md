# NEXUS XAU Engine — Video Source Index (2026-09-01 batch)

Purpose: preserve the exact source set supplied by the project owner and separate user labels from later transcript-derived rules.

## Evidence status legend
- USER-LABEL: description supplied directly by the project owner/chat source.
- WEB-METADATA: title verified from YouTube page metadata.
- TRANSCRIPT-PENDING: timestamp transcript extraction not yet completed.
- UNAVAILABLE: source could not currently be fetched by available retriever.

## Source set
1. `oCcG3dUjrgw` — https://youtu.be/oCcG3dUjrgw?si=hOUZgbIPDlAfZ2iZ
   - WEB-METADATA: EP.5 วิชาเก็บบอดี้ #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว
   - Chat note: 🍌 reported opening problem with this link; jBEM-vWYj_o was suggested as a replacement.
2. `jBEM-vWYj_o` — https://youtu.be/jBEM-vWYj_o?si=7TDHWagDnOYTAh12
   - USER-LABEL: “ใช้อันนี้แทนน่าจะได้”
   - WEB-METADATA: EP.3 แนวรับ - แนวต้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว
3. `ESHDuiVPJow` — https://youtu.be/ESHDuiVPJow?si=Z2cCGdSaYtoIluEa
   - WEB-METADATA: EP.2 เทรน ชนะ กรอบ กรอบ ชนะ Sig #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว
4. `UV5NijhjfJ8` — https://youtu.be/UV5NijhjfJ8?si=oTgzMrfUjtdRnFTr
   - USER-LABEL: “อันนี้เป็น การเข้าออเดอร์”
   - WEB-METADATA: EP.4 เบรก M5 เงินล้าน #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว
   - Priority: HIGH for deterministic entry/confirmation rules.
5. `a9hPolrjNwU` — https://youtu.be/a9hPolrjNwU?si=fOdklmfeHgspcJH0 — metadata/transcript pending.
6. `16KoS7d-koI` — https://youtu.be/16KoS7d-koI?si=kDoItAAg8aoDPaqP — metadata/transcript pending.
7. `vcdN51_OrPE` — https://youtu.be/vcdN51_OrPE?si=C6M1LUdSNTsa3673
   - USER-LABEL: “อันนี้สรุป ทั้งหมด”
   - WEB-METADATA: EP.พิเศษ ขยี้ให้แหลก #SmatTrderToSuccess #ระบบแม่ปลาปากกาเขียว
   - Priority: HIGHEST for terminology/system map, then verify against dedicated lessons.
8. `h9gwEq52AWQ` — https://youtu.be/h9gwEq52AWQ?si=wLLEMO54bPmCLh7O — pending.
9. `1E_PYPor1qQ` — https://youtu.be/1E_PYPor1qQ?si=G0DjGfKPMj15V9oE — pending.
10. `1QZ8elWm1fM` — https://youtu.be/1QZ8elWm1fM?si=UqQ1aiPlXQJN5Ocl — pending.
11. `CzsnaRh8egw` — https://youtu.be/CzsnaRh8egw?si=-FtNA3XzKscNORi7 — pending.
12. `im3ebGY12j4` — https://youtu.be/im3ebGY12j4?si=VmiphuRru0AX0W-2 — pending.
13. `NfdtSc4_A5I` — https://youtu.be/NfdtSc4_A5I?si=JApRbmEgjYvx5ef7 — pending.
14. `gdBy24O5DQU` — https://youtu.be/gdBy24O5DQU?si=G8gLG4ZcID-KS_x1 — pending.
15. `-CZ5laDyzjs` — https://youtu.be/-CZ5laDyzjs?si=ufeHz92jq41krorq — pending.
16. `Zila-zxvNx0` — https://youtu.be/Zila-zxvNx0?si=qtsOPS_4zuZayxJw — pending.

## Chat-context clue
At 22:57: `PAT1 อันไหนนะคับ` followed by `!!`. The supplied excerpt does not contain the actual answer. This supports that PAT1 was expected to map to one of the shared materials, but the exact video is UNKNOWN. Do not guess the mapping.

## Transcript-forensics order
1. `vcdN51_OrPE` — summary/all-system map.
2. `UV5NijhjfJ8` — entry order / M5 break.
3. `ESHDuiVPJow` — trend/frame/SIG hierarchy.
4. `jBEM-vWYj_o` — support/resistance/frame construction.
5. `oCcG3dUjrgw` — body collection and match against existing transcript evidence.
6. Remaining videos: identify topic, then target PAT1/PAT2/PAT3, พักครึ่ง, พักสวิง, Fibonacci, ช่องแม่ปลา, เพาะ, invalidation, SL/TP.

## Mandatory extraction schema
`video_id | title | timestamp_start | timestamp_end | exact_term | transcript_excerpt | visual_context_if_known | timeframe | direction | construct | condition | invalidation | evidence_type | confidence | notes`

## Rule discipline
- Exact teacher wording + timestamp = primary evidence.
- Visual context required where speech refers to the chart.
- Summary video identifies relationships but does not override dedicated lesson evidence.
- Never assume `เพาะ = PA` or `ช่องแม่ปลา = กรอบแม่` without direct evidence.
- PAT1/2/3 remain UNKNOWN until timestamp-level source evidence is recovered.
