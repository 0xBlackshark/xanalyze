# Evidence — คำสั่งที่ใช้พิสูจน์ทีละข้อ (read-only, reproduce ได้)

ทุกคำสั่งเป็น **read-only** (eth_call / GET). ถ้าค่าต่างจากที่ repo บันทึก ให้แก้ `tools/data_*.py` + `tools/verify.py:EXPECTED` แล้วรัน `python3 tools/build.py`
ทางลัด: `bash tools/verify.sh` รันชุดสำคัญทั้งหมด (schema + build check + live checks)

```bash
export BSC_RPC=https://bsc-rpc.publicnode.com
export ROBINHOOD_RPC=https://rpc.mainnet.chain.robinhood.com
```

## Renaiss (BNB Smart Chain, chainId 56)
```bash
call(){ curl -s --max-time 20 -X POST "$BSC_RPC" -H 'content-type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"eth_call\",\"params\":[{\"to\":\"$1\",\"data\":\"$2\"},\"latest\"]}"; echo; }

# 1) registry live
call 0xF8646A3Ca093e97Bb404c3b25e675C0394DD5b30 0x18160ddd   # totalSupply() -> 0x…2bbd = 11,197 @2026-09-30
call 0xF8646A3Ca093e97Bb404c3b25e675C0394DD5b30 0x06fdde03   # name() -> "Renaiss"
call 0xF8646A3Ca093e97Bb404c3b25e675C0394DD5b30 0x95d89b41   # symbol() -> "RENAISS"
call 0xF8646A3Ca093e97Bb404c3b25e675C0394DD5b30 0x5c975abb   # paused() -> 0
# 2) ใครอัปเกรดได้ (เช็กที่สำคัญที่สุด)
call 0xF8646A3Ca093e97Bb404c3b25e675C0394DD5b30 0xf851a440   # admin() -> 0xB4cc2a69B5E461Dbc76fEf668891D0E1E3b5C80a (TimelockController)
# 3) custody split: 11,197 ใบนั่งที่ไหน
#    (padding: เอา address ไปแปะหลัง 0x70a08231 ให้ครบ 64 hex)
call 0xF8646A3Ca093e97Bb404c3b25e675C0394DD5b30 \
  "0x70a08231$(printf '%064x' 0x14b662fc59f87ec004c2c25e0a2a49c9f858ef8c)"   # CollectibleInventory -> 5,012 @ตรวจ
# 4) เงินจริงรองรับ buyback (USDT 0x55d3…7955, 18 dec)
USDT=0x55d398326f99059fF775485246999027B3197955
for c in 0xD4d18607D6111C5FA2f93a4A5B2c0e28f1563F9F 0x48fbb6eaa5f8ba3068562b7518b970b32ca7fa8e 0x9c84bd30a694cb2b0b3cc3810d621973bd3dab9d; do
  python3 - "$USDT" "$BSC_RPC" "$c" <<'PY'
import json,sys,urllib.request
usdt,rpc,c = sys.argv[1:4]
body=json.dumps({"jsonrpc":"2.0","id":1,"method":"eth_call","params":[{"to":usdt,"data":"0x70a08231"+c[2:].rjust(64,'0')},"latest"]}).encode()
r=json.loads(urllib.request.urlopen(urllib.request.Request(rpc,data=body,headers={"content-type":"application/json"})).read())
print(c, "usdt =", int(r['result'],16)/1e18)
PY
done
# 5) source of truth
curl -s "https://sourcify.dev/server/v2/contract/56/0xF8646A3Ca093e97Bb404c3b25e675C0394DD5b30" | head -c 600
curl -s "https://sourcify.dev/server/v2/contract/56/0xAE3e7268EF5A062946216A44f58A8F685fFD11d0" | head -c 600
```
API (ไม่ต้องใช้ key):
```bash
curl -s https://api.renaiss.xyz/openapi.json | jq '.paths | keys | length'          # 134
curl -s https://api.renaiss.xyz/v2/marketplace/config | jq '.platformFeeBps'        # 200 (top-level, ไม่ใช่ .data!)
curl -s "https://api.renaiss.xyz/v2/marketplace?limit=1" | jq '.pagination'          # total listings
curl -s https://api.renaiss.xyz/v0/fair/packs | jq '[.packs[]|{name,allCardDrawnSetCount}]'
curl -s https://api.renaiss.xyz/v0/gacha-v3/packs | jq '[.data.cardPacks[]?|{name,priceUsd}]'
# fairness/ownership รายใบ: เลือก id จากหน้าเว็บ (เช่น link รูปมี PSA141467279 → psacard.com/cert ค้นเอา)
# แล้วเรียก ownerOf(tokenId) เทียบกับ ownerAddress ที่เว็บแสดง (เราทำสุ่ม 12 ใบ = ตรง 12/12)
```
- PSA grading cert: ลิงก์รูปการ์ดมีเลข cert ใน URL เช่น `PSA141467279` → `psacard.com/cert/141467279`
- known-bad: `eth_getLogs` (403), `getDelay()/getRoleMemberCount()` บน Timelock (0x), Sourcify v1 metadata path (404)

## NetNet (Robinhood Chain, chainId 4663)
```bash
callr(){ curl -s --max-time 25 -X POST "$ROBINHOOD_RPC" -H 'content-type: application/json' \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"eth_call\",\"params\":[{\"to\":\"$1\",\"data\":\"$2\"},\"latest\"]}"; echo; }
NET=0xca9c78dd337a67f6e0077f65f5e9218719d30edf     # 9 decimals (อ่านจริง)
T=0x04822Ea321A0DEE6F40656172F29312104855d66        # Treasury sole minter
USDG=0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168    # 6 decimals

callr $NET 0x06fdde03   # name() -> "NetNet"
callr $NET 0x95d89b41   # symbol() -> "NET"
callr $NET 0x313ce567   # decimals() -> 9
callr $NET 0x18160ddd   # totalSupply() -> 123,035.12 (rebase, เปลี่ยนทุก epoch)
callr $NET 0x61d027b3   # treasury() -> 0x04822E…66
callr $T   0x1521843e   # backingPerToken() -> 173.4643 (18dec scaled)
callr $USDG "0x70a08231$(printf '%064x' 0x04822ea321a0dee6f40656172f29312104855d66)"   # USDG in Treasury
# Treasury ไม่ได้เก็บเงินหมดที่ตัวเอง: ส่วนใหญ่อยู่ที่ Morpho vault (Steakhouse USDG)
M=0xBeEff033F34C046626B8D0A041844C5d1A5409dd
callr $M "0x70a08231$(printf '%064x' 0x04822ea321a0dee6f40656172f29312104855d66)"      # shares
callr $M "0x07a2d13a$(printf '%064x' <shares_int>)"                                     # convertToAssets
# team multisig (1-of-1 ตามที่ prospectus ยอมรับเอง)
callr 0x3Bb7A23316f82C0e984fA2E784846d8928a35f42 0xe75235b8   # getThreshold() -> 1
callr 0x3Bb7A23316f82C0e984fA2E784846d8928a35f42 0xa0e67e2b   # getOwners() -> [0xe7e86751…]
```
- ⚠️ **ห้ามอ่านราคา NET จาก `getReserves()`** — NET เป็น rebase (9 dec); ใช้ price จาก CoinGecko id=netnet หรือ aggregator ที่ normalize อยู่แล้ว
- สูตร prospectus: RFV = liquidUSDG × 1.0 + morphoPosition × (1−2%) + rfvOfPOL; rfvOfPOL = 2·sqrt(x·y) × treasuryLpShare ⇒ ตัวเลขที่ยืนยัน on-chain ได้
- canonical channels: https://docs.netnet.capital/official-channels — IF A CHANNEL IS NOT ON THIS PAGE, IT IS NOT OURS

## Pull.Fun (ไม่มีเกมบนเชน) + $TAKO (Robinhood Chain)
```bash
# 1) พิสูจน์ว่าไม่มี smart contract: grep ทั้ง JS bundle (ต้อง curl ใหม่ทุก session — /tmp ไม่ persist)
curl -s https://pull.fun -o /tmp/pf.html
grep -o 'src="[^"]*\.js"' /tmp/pf.html | sed 's/.*"\(.*\)".*/\1/' | while read -r j; do
  curl -s "https://pull.fun$j"; done > /tmp/pf_all.js
wc -c /tmp/pf_all.js                                      # ~3.27 MB (71 chunks)
grep -o '0x[0-9a-fA-F]\{40\}' /tmp/pf_all.js | sort -u | wc -l   # 0 contract-like for the game
grep -c -E 'ethers|viem|wagmi|createPublicClient' /tmp/pf_all.js # 0 used by the game
# 2) ตลาดจริงของ $TAKO (ไม่ใช่ id=tako ของ CoinGecko — อันนั้นเป็นคนละเหรียญ Ethereum)
curl -s "https://api.geckoterminal.com/api/v2/networks/robinhood/pools/0x0db676195d2da690afe67ff27444d941bcd7c056e2f512f40eb14620f3f0ead8" \
  | jq '.data.attributes | {price: .base_token_price_usd, reserve: .reserve_in_usd, fdv: .fdv_usd, vol: .volume_usd.h24, created: .pool_created_at}'
curl -s "https://api.dexscreener.com/latest/dex/search?q=TAKO" | jq '.pairs[] | select(.chainId=="robinhood")'
```
- fairness ของเกมเป็น **off-chain**: commit-reveal + HMAC + poolSnapshotHash — verify ได้ที่ `pull.fun/en/packs/.../proof` แต่ไม่ควรบอกว่า "on-chain fair"
- API ที่ใช้ได้: `/v0/fair/packs`, `/v0/fair/packs/{onChainPackId}/sets`, `/openapi.json` 
- pull-history ถูก capped ~500–2,000 → อย่าบวกเละ lifetime

## ห้ามเดา / บทเรียนจากการตรวจรอบนี้ (2026-09-30)
1. **เป็นไปได้ที่บันทึกเก่าจะเคลื่อนเชน**: รอบก่อนเขียน NetNet ว่าอยู่ Base และ $TAKO อยู่ Monad — อันที่จริงทั้งสองอยู่ Robinhood Chain (4663) ตรวจด้วย bundle + RPC เสมอ
2. **CoinGecko id เป็นเพียง slug**: id=tako คือเหรียญ Ethereum (420B supply) ไม่ใช่ $TAKO ของ pull.fun — ห้าม bind ด้วยชื่อ
3. **address ที่มี 'G' ไม่ใช่ตัวอักษร hex**: 0x…Gc96 ที่บันทึกไว้เก่าไม่ valid — ตรวจ `len==40 hex` ทุกครั้งที่ copy
4. **ข้อมูลใน JS bundle บน Robinhood Chain มีเอกลักษณ์**: contract map + "HUMAN-VERIFIED" + tx hash — ใช้เป็นแหล่งข้อมูลเริ่มต้นที่ประหยัดเวลาได้มาก แต่ต้องเรียก RPC ยืนยันต่อทุกชิ้น
5. `https://rpc.mainnet.chain.robinhood.com` รองรับ eth_call ปกติ; `robinhoodchain.blockscout.com` api/v2 โดน Cloudflare → holder concentration ไม่ได้วัด
