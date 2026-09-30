# AGENTS.md — วิธีใช้ repo นี้

repo นี้คือ *ฐานข้อมูลผลการตรวจสอบ* ไม่ใช่ blog post. อ่านเป็น JSON/CSV ได้ทันที และทุกความเชื่อมีคำสั่งพิสูจน์แนบไว้

## ถ้าจะอ่านอย่างเดียว
1. `data/index.json` → เลือก slug
2. `data/projects/<slug>.json` → ใช้ 10 ฟิลด์ภาคบังคับ (schema: `data/schema.json`)
3. ต้องย่อให้มนุษย์อ่าน → ใช้ `verdict_short`, `capital_rule`, `returns[]`

## กติกาบังคับ (hard rules)
- **อย่า quote ตัวเลขโดยไม่รัน** `bash tools/verify.sh` — ตัวเลข usage/ราคา/balance เปลี่ยนรายวัน; `stale_risk` บอกไว้ต่อ record
- **`unverified[]` คือเส้นแดง**: ห้ามเปลี่ยนสิ่งที่ยังวัดไม่ได้ให้เป็นข้อสรุปเชิงบวก หรือบอกว่า "ไม่มีข้อมูล = น่าจะโอเค"
- **คำเคลมของแพลตฟอร์ม ≠ หลักฐาน**: `trust_evidence[]` มีเฉพาะสิ่งที่วัดเอง (RPC/merkle/source/ตลาด) เท่านั้น
- `needs_recheck: true` → หลักฐานไม่ครบ (round แรกไม่ได้ persist raw) → re-derive ก่อนอ้างหรือก่อนแนะนำเงิน
- คำแนะนำเรื่องเงินต้องมาจาก `cost_of_entry_usd`, `returns[]`, `max_sane_budget_usd`, `capital_rule` — ห้ามคิดตัวเลขใหม่เอง
- ทุก record ต้องมี `unverified[]` และ `watch[]` ไม่เช่นนั้น build จะ fail

## ถ้าจะเขียน/อัปเดต
1. แก้ dict ใน `tools/data_renaiss.py` | `tools/data_netnet_pullfun.py` | `tools/data_older.py` (+ `tools/data_meta.py` สำหรับ field 7/งบ/วันตรวจ)
2. `python3 tools/build.py` — จะ validate ให้ (ครบ 10 ฟิลด์, score 0-10, `returns[]` เรียงตามงบ, `unverified` ไม่ว่าง)
3. commit ทั้ง source และ generated files (repo นี้ตั้งใจให้ generate output ถูก commit ไว้เพื่อ agent ที่อ่านโดยไม่ต้องรัน Python)

### รูปแบบ record ที่ต้องคงไว้
```json
{
  "name": "...", "links": { "x": "https://x.com/...", "site": "..." },
  "score": { "interest": 8.5, "trust": 8.0 },
  "field2_interest": "เหตุผลว่าทำไมได้คะแนนนี้",
  "trust_evidence": ["on-chain: ...", "source: ...", "market: ..."],
  "model": "สถาปัตยกรรม 3 ชั้น ...",
  "how_to_play": ["ตรวจก่อน ...", "เข้า ...", "ออก ..."],
  "risks": ["..."],
  "value_for_money": "จ่าย X ได้ Y",
  "house_edge": [{ "machine": "...", "price_usd": 28, "ev_usd": 31.0, "ev_over_price": "+10.7%", "instant_flip_net_pct": -5.9 }],
  "opportunity": "...",
  "returns": [{ "budget_usd": 100, "note": "...", "expected_usd": -6.0 }],
  "max_sane_budget_usd": 1000, "capital_rule": "...",
  "history": ["2026-06-18: ..."],
  "technical": { "onchain": [{ "item": "...", "addr": "0x...", "finding": "..." }], "api_endpoints": [] },
  "verdict_short": "...",
  "unverified": ["..."], "watch": ["..."], "sources": ["..."],
  "stale_risk": "medium", "needs_recheck": false
}
```

## สกอร์ = rubric (docs/methodology.md)
on-chain verifiability 25 + custody/funds proof 20 + real usage 20 + legal entity 15 + tokenomics/house edge 10 + team/backing 10 → ×10 เป็นสเกล 0-10

## เวลาจะเพิ่มโปรเจกต์ใหม่ (checklist ที่ใช้จริงกับ 8 ตัวนี้)
1. X profile: follower/tweets/join date/verified badge — นับ account ที่เกี่ยวข้องด้วย
2. โดเมน: RDAP/whois (`.fun`/`.capital` มักไม่ตอบ → ให้บันทึกว่า "ตรวจไม่ได้")
3. raw HTML + JS bundle: grep หา `0x[0-9a-f]{40}`, `contract`, `merkle`, `ethers|viem|wagmi` → ถ้า 0 = Web2 store
4. API: อ่าน `/openapi.json` ก่อนเดา path (path ที่เดาเอง 404 เกือบหมด)
5. On-chain: `totalSupply/ownerOf/balanceOf/paused/admin/code` + custody split + stablecoin balance ใน contract
6. Fairness: merkle root ต่อ set, `cardCount × allCardDrawnSetCount` = lifetime pulls (pull-history API ถูก capped)
7. ตลาด: CoinGecko/DexScreener (price/vol/liq/FDV) — liq/MC < 10% = ห้ามถือยาว
8. ToS/Privacy: entity + เขตอำนาจศาล + arbitration/KYC/geo-block
9. เงิน: คำนวณ EV ต่อหน่วย, haircut, round-trip cost, slippage ตามขนาด order จริง
10. เขียน `unverified[]` ให้ตรงข้ามกับ `trust_evidence[]` — สิ่งที่ยืนยันไม่ได้ต้องถูกเขียนไว้

## verify & push
- `bash tools/verify.sh` — re-check live (ต้องต่อเน็ตได้)
- `bash tools/push-github.sh yourname/crypto-due-diligence` — สร้าง repo + push (ใช้ `GITHUB_TOKEN`; repo นี้ไม่มีสิทธิ์ของใครฝังอยู่)
