# Crypto / NFT / points due-diligence — อ่านได้ทั้งคนและ agent

ตรวจเองบนเชน+API ไม่เชื่อข้อความบนเว็บ · ภาษาไทย · ทุกตัวเลขมีคำสั่ง re-verify ได้ (`tools/verify.sh`)

- 8 โปรเจกต์ · snapshot หลัก: `2026-09-30` · schema `v1.0`
- เริ่มอ่านจาก: `llms.txt` (agent) หรือตารางด้านล่าง (คน)
- แก้ข้อมูล: แก้ `tools/data_*.py` → `python3 tools/build.py` (ไฟล์อื่นทั้งหมดถูก generate) 

## การจัดอันดับ (interest = ความน่าสนใจ, credibility = ความน่าเชื่อถือ)

| # | โปรเจกต์ | interest | credibility | สถานะ | เข้าได้ตั้งแต่ | เพดานงบ | หนึ่งบรรทัด |
|--:|---|--:|--:|---|--:|--:|---|
| 1 | [Renaiss](data/projects/renaiss.md) | 8.5 | 8.0 | live (open beta) | $28 | $1,000 | RWA ตัวจริงที่ตรวจสอบได้บนเชน: การ์ดสแล็บจริง 11,197 ใบเป็น NFT บน BSC, สัญญา verified, อัปเกรดต้องผ่าน Timelock, ord… |
| 2 | [NetNet Capital Management ($NET)](data/projects/netnet.md) | 7.5 | 7.0 | live | $500 | $5,000 | Reserve fund สไตล์ OlympusDAO v1 บน Robinhood Chain ที่โปร่งใสเกินมาตรฐานโครงการนี้: มี prospectus ฉบับจริงบอกสูตร RF… |
| 3 | [Pull.Fun (+ $TAKO)](data/projects/pullfun.md) | 6.5 | 4.5 | live (store | $10 | $500 | ร้านเปิดpack การ์ดสแล็บจริงที่ serious ด้าน UX — odds เปิดเผย, fair commit-reveal (off-chain), KYC, Stripe, ToS มีเนื… |
| 4 | [TRACE](data/projects/trace.md) | 4.5 | 4.0 | live collection | $50 | $200 | NFT collection ที่ on-chain มีจริงแต่ proxy ไม่ตรงกับที่เว็บแสดง; floor 0.0108 ETH, volume 7 วัน 59.39 ETH; โปรเจกต์ก… |
| 5 | [Clickihood](data/projects/clickihood.md) | 4.0 | 3.0 | mint เสร็จ | $0 | $50 | Free mint 9,999 ที่ metadata ยัง unfrozen และ contract ไม่มีเงิน (0 ETH) — on-chain โปร่งใสดี (holder 711, top-10 29.… |
| 6 | [HYPEST](data/projects/hypest.md) | 3.5 | 3.0 | leaderboard เปิด | $0 | $0 | ระบบ leaderboard 400 ใบแบบ non-transferable (ตรวจสอบได้) ที่โฆษณา pool $HYPE 690 ล้านเหรียญที่ยัง 'ไม่เปิดใช้งาน' — โ… |
| 7 | [Agnt](data/projects/agnt.md) | 3.0 | 2.5 | mint 2,530/10,000 | $0 | $0 | Mint ที่วิ่งไปเพียง 25.3% ของ supply (2,530/10,000) และความเข้มข้นการถือ 63% ในกลุ่มบน + ปุ่ม claim ยังปิด (claimsOpe… |
| 8 | [MemeBitcoin](data/projects/memebitcoin.md) | 1.0 | 0.5 | ไม่แนะนำทุกกรณี | $0 | $0 | Lottery/Math-based scheme ที่ probability ชัยชนะจริงต่ำจนกลายเป็นศูนย์: ที่ผู้เล่น 60,000 คน โอกาสชนะต่อวัน ~3.7e-39 … |

## ผลตอบแทนคาดการณ์ตามงบ (USD, ค่าคาดหวังหลังหัก house edge/fee แล้ว — ไม่ใช่คำการันตี)

| งบ | Renaiss | NetNet Capital Management ($NET) | Pull.Fun (+ $TAKO) | TRACE | Clickihood | HYPEST | Agnt | MemeBitcoin |
|---:|---:|---:|---:|---:|---:|---:|---:|---:
| $0 | +0 | +0 | -1 | +0 | +0 | +0 | +0 | +0 |
| $100 | -6 | -10 | -12 | -5 | -10 | -100 | -40 | -100 |
| $500 | -18 | -49 | -53 | -20 | -40 | +0 | -200 | -500 |
| $1,000 | -60 | -98 | -106 | -200 | -300 | +0 | -400 | -1,000 |
| $5,000 | -60 | -488 | -530 | -1,200 | +0 | +0 | -2,000 | -5,000 |
| $10,000 | -1,500 | -975 | -530 | +0 | +0 | +0 | -4,000 | -10,000 |

> อ่านตารางนี้ว่า: ถ้ามีเงิน X ควรไปลงตรงไหน และ **ผลที่คาดหวังเป็น USD** คือเท่าไร; ตัวเลขเชิงลบหมายความว่า ค่าเฉลี่ยของผู้เล่นเสียเท่านั้นเท่านี้ ไม่ใช่ "อาจจะเสีย"

## หลักการให้คะแนน credibility (rubric)

| องค์ประกอบ | น้ำหนัก |
|---|--:|
| ตรวจสอบ on-chain ได้จริง | 25 |
| การ custody เงิน/ของ + หลักฐานสต็อก | 20 |
| ปริมาณการใช้งานจริง (ไม่ใช่ตัวเลข PR) | 20 |
| นิติบุคคล + การเปิดเผยใน ToS | 15 |
| โครงสร้าง tokenomics / house edge เปิดเผย | 10 |
| ทีม + ผู้สนับสนุน (ยืนยันจากแหล่งอิสระ) | 10 |

คะแนนที่แสดงเป็น 0–10 (ถ่วงน้ำหนักแล้ว ×10) — ดูวิธีคิดเต็ม ๆ ที่ `docs/methodology.md`

## สิ่งที่ไม่ตรวจให้ (ขอบเขต)

- สัญญาว่าเป็นกำไร / ให้คำแนะนำการลงทุนรายบุคคล — นี่คือข้อมูลตัดสินใจ ไม่ใช่คำแนะนำ
- ตัวเลขที่แพลตฟอร์มไม่เปิดให้วัด (จำนวน holder จริงบน chain ที่ RPC ถูกปิดกั้น, สต็อกในคลัง vault) — ดู `unverified[]` ของแต่ละไฟล์

## โครงสร้างไฟล์

```
llms.txt                     ทางเข้าของ agent
AGENTS.md                    กติกาการอ่าน/อัปเดต
data/index.json              สแกนเร็ว: slug, rank, scores, verdict, path
data/scorecard.csv           หนึ่งแถวต่อโปรเจกต์ (เปิดใน Excel ได้)
data/schema.json             JSON Schema — บังคับให้มีครบ 10 ฟิลด์
data/projects/<slug>.json    บันทึกเต็ม (ทุกฟิลด์ที่ agent ต้องใช้)
data/projects/<slug>.md      บันทึกเดียวกันฉบับคนอ่าน
docs/methodology.md          rubric + นิยาม house edge + เกณฑ์ตัดคะแนน
docs/pitfalls.md             กับดัก/ข้อผิดพลาดที่เคยเกิด (รวมสิ่งที่ผมเคยแก้)
docs/evidence.md             คำสั่ง + endpoint + contract ที่ใช้พิสูจน์ทีละข้อ
tools/data_*.py              แหล่งข้อมูลจริง (แก้ที่นี่)
tools/build.py               ตัว render ทั้งหมดใน repo
tools/verify.sh              re-verify live ก่อนอ้างตัวเลข
tools/push-github.sh         สร้าง repo + push (ต้องใส่ GITHUB_TOKEN เอง)
```

## หมายเหตุความซื่อสัตย์

ทุกไฟล์มี `unverified[]` ของตัวเอง; `needs_recheck: true` = หลักฐานชุดนั้นไม่ครบถ้วนโดยเจตนา (โปรเจกต์ที่ตรวจไว้รอบแรก และ raw artifacts ไม่ถูกเก็บไว้) — ห้ามใช้อ้างอิงภายนอกถ้ายังไม่ re-derive
