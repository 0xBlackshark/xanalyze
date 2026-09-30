# Methodology — วิธีได้มาซึ่งคะแนนและตัวเลข

## ลำดับการเชื่อ (evidence hierarchy)
1. **ที่อ่านได้จาก chain โดยตรง** — `totalSupply`, `ownerOf`, `balanceOf`, `code`, `admin()`, `paused()`, tx logs
2. **ที่อ่านได้จาก API/ source ที่ publish เอง** — `openapi.json`, merkle/set counters, listing counts, JS bundle (grep)
3. **ตลาด/ ราคา** — CoinGecko, DexScreener, เทรดจริงบน orderbook
4. **เอกสาร** — ToS/Privacy (นิติบุคคล, เขตอำนาจศาล, KYC, geo-block)
5. **คำเคลมของโปรเจกต์** (X posts, PR, ตัวเลขบนเว็บ) — **ใช้ตั้งสมมติฐานเท่านั้น ห้ามใช้เป็นหลักฐาน**
6. KOL / thread แชร์กัน — ไม่มีน้ำหนัก เว้นแต่ชี้ให้เช็กข้อ 1-4

กฎเหล็ก: ข้อใดอยู่ระดับ 5 และไม่มีใครตรวจข้าม (cross-check) ได้ → ต้องไปอยู่ใน `unverified[]` ของ record เสมอ

## rubric ของ credibility (0-10)
| องค์ประกอบ | น้ำหนักเต็ม | ดูอะไร | ตัดคะแนนเมื่อ |
|---|--:|---|---|
| On-chain verifiability | 25 | contract verified? คำเคลมหลัก map เป็น function/field ที่เรียกได้? | 0 contract (Web2 store), proxy ไม่ match, docs ล้าสมัย |
| Custody + funds proof | 20 | เงิน/ของอยู่ที่ไหน, มี stablecoin balance จริง, มี attestation อิสระ, burn-on-redeem | vault ไม่ระบุชื่อ, escrow ไม่มียอด, mint ปิดแต่ยังคุม supply คนเดียว |
| Real usage | 20 | ตัวเลขที่ counting ได้ (set id, pulls, listings→deals, TVL, holders) | ใช้ follower / PR "users" แทน volume จริง |
| Legal entity + disclosure | 15 | ชื่อบริษัท + จดทะเบียนที่ไหน, ToS, geo/KYC, arbitration | ไม่ระบุ entity, ไม่มี ToS, no refund |
| Tokenomics + house edge | 10 | EV ต่อหน่วยเปิดเผย, fee, haircut, unlock/vesting | EV ซ่อน, tax สองทาง, team wallet ไม่ lock |
| Team + backing | 10 | ผู้ลงทุนที่ verify จากแหล่งอิสระ, provenance ของ founder | อ้าง VC โดยไม่มีข่าว, ทีมไม่เปิดเผย |

`score.interest` = "ควรมีใครสละเวลา/เงินทุนกับสิ่งนี้ไหม" (ให้ credit กับความหายากของ setup) — จึงต่างจาก credibility โดยตั้งใจ
ตัวอย่างที่เห็นชัด: `pullfun` product interest 6.5 / token interest 2.0; `renaiss` interest 8.5 แต่ "ไม่มีอะไรให้ซื้อ"

## วิธีคำนวณตัวเลขที่ปรากฏใน record
- **EV ต่อ pack** = Σ (ความน่าจะเป็นชั้น × ฐานราคาที่ buyback รับ) เทียบกับราคาขาย
- **instant flip net** = `EV × (1 − haircut) / price − 1` ⇒ Renaiss $28: `31.00 × 0.85 / 28 − 1 = -5.9%` (haircut 15% ของฐาน buyback)
- **round-trip (token)** = `(1 − buy tax) × (1 − sell tax) − 1` ⇒ NetNet `0.95 × 0.95 − 1 = -9.75%` ก่อนบวก slippage; pull.fun instant flip ≈ `-spread + ค่าธรรมเนียมระบบ`
- **premium** = `price / backing_per_unit` (NetNet: 472.55 / 173.97 = 2.716)
- **lifetime pulls** (เมื่อ pull-history API ถูก capped) = `allCardDrawnSetCount × cardCount`
- **GMV ประมาณการ** = Σ pulls × price
- **liq/MC ratio** = pool liquidity ÷ market cap — เกณฑ์: < 10% = ห้ามถือยาว, < 20% = เทรดสั้นเท่านั้น
- **concentration** = ยอดถือของ top-10 ÷ supply (ต้องมี on-chain ranking ไม่ใช่ dashboard เว็บ)
- **exit depth** = ดีลจริงในช่วงเวลา (Renaiss: 30 sells = $5,667/6 วัน ⇒ ~5 ดีล/วัน ⇒ เพดานงบรายตัว)

## money framing (ทุก record ต้องตอบได้)
1. `cost_of_entry_usd` = ขั้นต่ำที่ "ทดสอบระบบจริง" โดยไม่หลอกตัวเอง
2. `returns[]` = ค่าคาดหวัง (USD) ที่งบ 0/100/500/1,000/5,000/10,000 — ระบุ *เหตุผล* ของตัวเลขใน `note`
3. `max_sane_budget_usd` = เพดานที่สภาพคล่อง/size ตลาดรับได้
4. `capital_rule` = trigger + stop (เช่น NetNet: เข้าเมื่อ premium<1.1, ออกเมื่อ depth<$600k)
5. ถ้าไม่มี setup ที่ EV เป็นบวก ให้ตอบตรง ๆ ว่า "อย่าเข้า" (ดู `memebitcoin`)

## เกณฑ์จัดอันดับข้ามโปรเจกต์
เรียงตาม `score.interest` แล้ว tie-break ด้วย credibility; หมายเหตุ: อันดับ = "ความน่าสนใจเมื่อเทียบกับสิ่งที่ตรวจด้วยกันชุดนี้" ไม่ใช่คำแนะนำการลงทุน

## ความไม่แน่นอน
- ทุก record มี `stale_risk` (ระดับ) + `stale_risk_note` (อะไรเน่าเร็ว)
- `needs_recheck: true` = หลักฐานชุดนั้นไม่ครบ (ส่วนมากเพราะ round แรกไม่ได้ persist raw artifacts)
- ไม่มีตัวเลขไหนควรอ้างนอก repo นี้โดยไม่รัน `bash tools/verify.sh` ก่อน
