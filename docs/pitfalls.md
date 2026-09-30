# Pitfalls — กับดักที่เจอจริงระหว่างตรวจ 8 โปรเจกต์

อ่านก่อนเริ่มตรวจโปรเจกต์ใหม่ ทุกข้อยามาจากการพลาดจริง (ของผมเองรวมอยู่ด้วย) ไม่ใช่ทฤษฎี

## A. กับดักด้านเครื่องมือ (เทคนิค)
| # | กับดัก | ทางแก้ที่ใช้ได้ผล |
|--:|---|---|
| 1 | `fetch_page` บน SPA (React/Next) ได้ HTML เปล่าหรือ skeleton | `curl` raw HTML/JS bundle แล้ว grep; payload RSC ต้อง `.replace('\\"','"')` ก่อน regex |
| 2 | เดา path API | อ่าน `/openapi.json` ก่อน — path ที่เดาเอง 404 เกือบทั้งหมด (`/v1/fair/packs/{uuid}/sets`, `/v0/fair/packs/{slug}/sets`, `/v1/fair/active-sets/{root}` พังหมด; ที่ใช้ได้คือ `/v0/fair/packs/{onChainPackId}/sets`) |
| 3 | พารามิเตอร์ paging ถูกมองข้าม | `/v0/marketplace?pageSize=1` ไม่ย่อ (ได้ 10 เสมอ) → ใช้ `pagination.total` + `limit` |
| 4 | ประวัติ pull ถูก capped (~500-2,000 รายการ) | lifetime pulls = `allCardDrawnSetCount × cardCount`; **ห้าม** สรุปจากหน้า history ว่าเป็นของทั้งชีพ |
| 5 | `eth_getLogs` บน public RPC | `bsc-rpc.publicnode.com` ตอบ **403** แม้ช่วง 20k blocks → วัด holder set / Transfer-rate ไม่ได้ ให้เขียนว่า "ตรวจไม่ได้" |
| 6 | ไม่มี archive node (เช่น chain 4663) | rarity/Holder snapshot ย้อนหลังทำไม่ได้ → enumerate state ปัจจุบันเท่านั้น |
| 7 | `api.bscscan.com` / Blockscout `api/v2` | Cloudflare challenge ถ้าไม่มี key → holder concentration มักวัดไม่ได้ |
| 8 | อ่านราคา token จาก `getReserves()` | พังกับ **rebase token** (NetNet) → ใช้ `totalSupply` แล้วหาร 1e18 / อ่าน backing จาก vault ตรง ๆ |
| 9 | dynamic string (`name()`, `symbol()`) | ต้อง decode offset+length (ABI head/tail) ไม่ใช่ `.hex()→ascii` ตรง ๆ |
| 10 | encodings ของ API ไม่ standard | USDT เป็น string 18-dec; tier/FMV/buyback เป็น **cents**; บาง count ×1e6 → ดู type ใน openapi ก่อนหาร |
| 11 | Sourcify | `full/partial_match/56/<addr>/metadata.json` 404 ครบทั้ง 11 address ของ Renaiss → ใช้ v2 endpoint + selector probing แทน |
| 12 | RDAP/whois | `.fun`, `.capital` เงียบ ⇒ "อายุโดเมน" มักตรวจไม่ได้ (ให้บันทึกว่าตรวจไม่ได้ ไม่ใช่ "โดเมนใหม่") |
| 13 | fxtwitter `/status` | 404 → อ่าน profile อย่างเดียว (`https://api.fxtwitter.com/<handle>`) เอา timeline ไม่ได้ |
| 14 | ไฟล์ชั่วคราวใน sandbox | `/tmp` ถูกเคลียร์ทุก session — ต้อง curl ใหม่ก่อน grep เสมอ (repo นี้จึง generate ใหม่ได้เสมอ) |
| 15 | `json.loads` กับ JS ที่มี single quotes | ใช้ regex ตัด fragment แทนการ parse ทั้งก้อน |

## B. กับดักด้านความหมาย (ที่ทำให้สรุปผิด)
1. **"สัญญา custody" ≠ "มีเงินจริง"** — ต้อง `balanceOf` stablecoin ใน contract (Renaiss USDT ~$60k) และนับใบใน registry
2. **`paused()=0` ไม่ใช่ "ปลอดภัย"** มันแค่ยังไม่ถูกปิด — ดูว่า `admin()` เป็น timelock หรือ EOA
3. **verified badge บน X ไม่ใช่การยืนยันองค์กร** — เช็ก `subscriptions.blue` / verified type
4. **ตัวเลขบนหน้าเว็บเป็น self-price** — Renaiss FMV อัปเดต 2026-08-27 (ช้า ~1 เดือน) ⇒ haircut จริงอาจเกิน 15%
5. **`vaultLocation`** มีค่า `platform` 50/50 ในข้อมูลที่สุ่ม ⇒ คำว่า "independent vault" ยังไม่มีหลักฐานรายตัว
6. **airdrop speculation ต้องแยกจากข้อเท็จจริง** — SBT 0x7d1b.../Rewarder 0xaAb4... มีจริง แต่ไม่มีประกาศ ⇒ ห้ามตีความเป็น "airtime"
7. **EV บวก ≠ กำไร** — ต้องคูณ haircut/fee และวัด exit depth ก่อนใส่เงินก้อนใหญ่
8. **liq/MC < 10% = ราคาเป็นภาพลวงตา** ($TAKO liq $64,412 ต่อ MC $445,256)
9. **PR ตัวเลขสูงต้องหากับอิสระ** — ">260,000 users / >$20M turnover" ไม่มีแหล่งยืนยัน; คำนวณจาก set counts ได้ ~$5.6M เฉพาะเครื่องที่วัดได้
10. **related-party**: Logoman เป็นทั้ง angel investor และ co-author ของ Eden Pack — ความสัมพันธ์แบบนี้ต้องเขียนไว้ ไม่ใช่เงียบ

## C. ข้อผิดพลาดของผมเองที่ถูกแก้ระหว่างทาง (เก็บไว้ให้ agent รู้ว่าอะไรเคยผิด)
| เคยรายงาน | แก้เป็น | บทเรียน |
|---|---|---|
| Clickihood "~3,600 holders" | **711** | นับ holder จาก UI/dashboard ไม่ได้ ต้อง iterate `ownerOf` จริง |
| "NetNet ไม่มีฟังก์ชัน withdraw()" | มี (อ่าน contract ผิดตัว) | ตรวจ address ให้ตรง impl/proxy ก่อนเคลม absense |
| "คอลัมน์ 8 = level" (TRACE) | ไม่ใช่ | schema ของตารางบนเว็บ ≠ semantic ที่เดา |
| "depth $277k, 209×" | **$1.31M, ≈44×** | อ่านผิดหน่วย/dex depth ไม่ใช่ pool จริง |
| "$TAKO ไม่มี price history" | มี (CoinGecko OHLCV) | ให้เช็กหลาย endpoint ก่อนบอกว่า "ไม่มีข้อมูล" |
| pull.fun = "on-chain fair" | เป็น **DB-backed store** (0 contract ใน bundle 3.27 MB) | คำว่า "fair" ใน UI ≠ on-chain verification |

## D. เกณฑ์ปฏิเสธ (fast-fail)
เข้าแล้วไม่ต้องตรวจต่อเมื่อ: (1) ไม่มี contract แต่ขาย "proof" (2) ไม่มี escrow ที่ `balanceOf` ได้ (3) โอกาสชนะคำนวณแล้ว ~0 (MemeBitcoin: ~3.7e-39/วัน ที่ 60k คน)
(4) mint ปิด + ไม่มี utility + holder < 1,000 (5) ToS ไม่มี entity ระบุ

## E. ข้อผิดพลาดที่จับได้ในการประกอบ repo นี้ (live 2026-09-30)
1. **Invoice-est price จาก memory: address '0x552e…Gc96' มี 'G' อยู่ ซึ่งไม่ใช่ hex** — ตรวจสอบ `[len==42 แล git checkoutNn hex char oversó]` ทุกครั้งหลัง copy paste
2. **CoinGecko slug ≠ token**: id=tako เป็นเหรียญ Ethereum (supply 420.69B) ไม่ใช่ $TAKO ของ pull.fun — ห้าม bind ด้วยชื่อ/id เสมอให้ bind ด้วย chain + address
3. **Memory นานี้โยง chain ผิด**: netnet ที่จำไว้เป็น Base จริงๆ เป็น Robinhood Chain (4663) — เอกสารที่ genrrate จาก memory ต้อง re-verify ทุกข้อ
4. **`pa[]` comparison ผิด (`[:42]`)**: อย่าตัด `.results` ของ eth_call แบบครึ่งวินาที — getAddress ของคุณเอง ให้เอา last 40 ของ 64 char ที่ unpack แล้ว
5. **API shape ระวัง `.data` vs top-level**: `/v2/marketplace/config` คืน `{chainId, platformFeeBps, contracts:{...}}` ทีละตัวท็อป (ไม่ใช่อ่อน `.data`; สำหรับบาง endpoint อื่นใช่ — เช็กขวา/ซ้ายทีละตัว)
6. **`/v0/fair/packs` ระวัง**: field ที่เป็น usage raster คือ `allCardDrawnSetCount` (บางใต้ `currentSetId`) — ต่อ endpoint ที่ดีกว่าเพื่อนร่วม
7. **`/health` ของ backend**: ตรวจซ้ำซ้อนของไฟลสญาณไวรัส — เกี่ยนใจไม่ใช่ระบบที่อยู่ข้างล่าง แม้ว่าเขาประกาศใช้ URL ที่ out proxy ไว้

