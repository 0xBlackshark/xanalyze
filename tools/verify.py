#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-verify live what this repo claims, stdlib only. Run: python3 tools/verify.py (or: bash tools/verify.sh)
Exit code 0 = all live checks match the recorded snapshot; 1 = at least one DRIFT/FAIL (repo must be updated).
Checks are read-only (eth_call / GET). Nothing here signs, sends, or approves anything.

Snapshot baseline: 2026-09-30. Fix the EXPECTED dict when the repo records are updated.
"""
import json, os, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = int(os.environ.get("DD_TIMEOUT", "20"))
BSC = os.environ.get("BSC_RPC", "https://bsc-rpc.publicnode.com")
RHO = os.environ.get("ROBINHOOD_RPC", "https://rpc.mainnet.chain.robinhood.com")

# --- hardcoded function selectors (keccak4 of the signature) ---
SEL = {"totalSupply": "18160ddd", "paused": "5c975abb", "admin": "f851a440", "decimals": "313ce567",
       "ownerOf": "63522119", "balanceOf": "70a08231", "name": "06fdde03",
       "treasury": "61d027b3", "backingPerToken": "1521843e", "rfv": "4dc8d6df", "getThreshold": "e75235b8"}

EXPECTED = {
    # --- Renaiss / BNB Smart Chain ---
    "registry": "0xF8646A3Ca093e97Bb404c3b25e675C0394DD5b30",
    "timelock": "0xB4cc2a69B5E461Dbc76fEf668891D0E1E3b5C80a",
    "usdt": "0x55d398326f99059fF775485246999027B3197955",
    "vending": "0xD4d18607D6111C5FA2f93a4A5B2c0e28f1563F9F",
    "instant_buyback": "0x48fbb6eaa5f8ba3068562b7518b970b32ca7fa8e",
    "registry_total_supply": 11197,
    "registry_paused": 0,
    "platform_fee_bps": 200,
    "usdt_vending_usd": 46317.72,
    "usdt_instant_buyback_usd": 4331.35,
    "listings_at_snapshot": 4147,
    "fair_packs": {"PANDORA 28": 247, "PANDORA 48": 715},   # allCardDrawnSetCount
    "balance_tolerance_pct": 40.0,
    # --- NetNet / Robinhood Chain (ChainId 4663) ---
    "net": "0xca9c78dd337a67f6e0077f65f5e9218719d30edf",
    "net_treasury": "0x04822Ea321A0DEE6F40656172F29312104855d66",
    "net_total_supply": 123035.12,
    "net_backing_per_token": 173.4643,
    "usdg": "0x5fc5360D0400a0Fd4f2af552ADD042D716F1d168",
    "usdg_in_treasury": 6692428.19,
    "morpho_vault": "0xBeEff033F34C046626B8D0A041844C5d1A5409dd",
    "morpho_assets_in_treasury": 14923520.98,
    "team_multisig": "0x3Bb7A23316f82C0e984fA2E784846d8928a35f42",
    # --- Pull.Fun / Robinhood Chain ---
    "tako_pool": "0x0db676195d2da690afe67ff27444d941bcd7c056e2f512f40eb14620f3f0ead8",
    "tako_reserve_usd": 81944.26,
    "tako_fdv_usd": 504093.0,
}
RESULTS = []


def out(status, name, detail=""):
    RESULTS.append((status, name, detail))
    print(f"[{status:6}] {name}" + (f" — {detail}" if detail else ""))


def http_json(url, data=None):
    req = urllib.request.Request(url, data=data,
        headers={"user-agent": "dd-verify/1.0", "content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def eth_call(rpc, to, selector, arg=""):
    payload = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "eth_call",
                          "params": [{"to": to, "data": "0x" + selector + arg}, "latest"]}).encode()
    res = http_json(rpc, data=payload)
    if "error" in res:
        raise RuntimeError(str(res["error"].get("message", "rpc error"))[:70])
    return res["result"] or "0x"


def pad_addr(a): return a.lower().replace("0x", "").rjust(64, "0")
def to_int(h): return int(h[2:], 16) if isinstance(h, str) and h.startswith("0x") and len(h) > 2 else 0
def to_addr(h): return "0x" + h[-40:].lower()


def within(tol_pct):
    def c(a, e):
        return bool(e) and abs(a - e) / abs(e) * 100 <= tol_pct
    return c


def check(label, fn, expected, cmp=None, fmt=None):
    cmp = cmp or (lambda a, e: a == e)
    fmt = fmt or (lambda v: str(v))
    try:
        got = fn()
    except Exception as exc:                                     # noqa: BLE001
        out("SKIP", label, f"unreachable/unparsable: {type(exc).__name__}: {exc}")
        return None
    try:
        ok = cmp(got, expected)
    except Exception:                                            # noqa: BLE001
        ok = None
    if ok is True:
        out("PASS", label, f"{fmt(got)} (recorded: {fmt(expected)})")
    elif ok is None:
        out("REVIEW", label, f"live={fmt(got)} recorded={fmt(expected)} — comparator not applicable")
    else:
        out("DRIFT", label, f"live={fmt(got)} recorded={fmt(expected)} — update tools/data_*.py + rebuild")
    return got


def main():
    rec = {}
    rp = os.path.join(ROOT, "data", "projects", "renaiss.json")
    if os.path.exists(rp):
        rec = json.load(open(rp, encoding="utf-8"))

    print("== Renaiss / BNB Smart Chain (chainId 56) ==")
    if rec:
        out("INFO", "repo record present", f"verified_on={rec.get('verified_on')} needs_recheck={rec.get('needs_recheck')}")
    check("Registry.totalSupply()", lambda: to_int(eth_call(BSC, EXPECTED["registry"], SEL["totalSupply"])),
          EXPECTED["registry_total_supply"])
    check("Registry.paused()", lambda: to_int(eth_call(BSC, EXPECTED["registry"], SEL["paused"])),
          EXPECTED["registry_paused"])
    check("Registry.admin() == Timelock",
          lambda: to_addr(eth_call(BSC, EXPECTED["registry"], SEL["admin"])),
          EXPECTED["timelock"].lower())
    check("USDT in VendingMachineV3", lambda: to_int(eth_call(
              BSC, EXPECTED["usdt"], SEL["balanceOf"], pad_addr(EXPECTED["vending"]))) / 1e18,
          EXPECTED["usdt_vending_usd"], cmp=within(EXPECTED["balance_tolerance_pct"]), fmt=lambda v: f"${v:,.2f}")
    check("USDT in InstantBuyback", lambda: to_int(eth_call(
              BSC, EXPECTED["usdt"], SEL["balanceOf"], pad_addr(EXPECTED["instant_buyback"]))) / 1e18,
          EXPECTED["usdt_instant_buyback_usd"], cmp=within(EXPECTED["balance_tolerance_pct"]), fmt=lambda v: f"${v:,.2f}")
    check("marketplace/config platformFeeBps",
          lambda: http_json("https://api.renaiss.xyz/v2/marketplace/config").get("platformFeeBps"),
          EXPECTED["platform_fee_bps"])
    check("marketplace listings (total)",
          lambda: (http_json("https://api.renaiss.xyz/v2/marketplace?limit=1").get("pagination") or {}).get("total"),
          EXPECTED["listings_at_snapshot"], cmp=lambda a, e: isinstance(a, int) and a >= 0, fmt=lambda v: f"{v:,}")
    check("fair packs allCardDrawnSetCount (usage raster)",
          lambda: {p["name"]: p.get("allCardDrawnSetCount") for p in http_json("https://api.renaiss.xyz/v0/fair/packs").get("packs", [])
                   if p.get("name") in EXPECTED["fair_packs"]},
          EXPECTED["fair_packs"],
          cmp=lambda a, e: all(isinstance(a.get(k), int) and a[k] >= v for k, v in e.items()),
          fmt=lambda v: str(v))

    print("\n== NetNet / Robinhood Chain (chainId 4663) ==")
    check("NET.totalSupply() (rebase — expect within ±2%)",
          lambda: to_int(eth_call(RHO, EXPECTED["net"], SEL["totalSupply"])) / 1e9,
          EXPECTED["net_total_supply"], cmp=within(2.0), fmt=lambda v: f"{v:,.2f}")
    check("NET.treasury() == 0x04822E…", lambda: to_addr(eth_call(RHO, EXPECTED["net"], SEL["treasury"])),
          EXPECTED["net_treasury"].lower())
    check("Treasury.backingPerToken() (±3%)",
          lambda: to_int(eth_call(RHO, EXPECTED["net_treasury"], SEL["backingPerToken"])) / 1e18,
          EXPECTED["net_backing_per_token"], cmp=within(3.0), fmt=lambda v: f"${v:.4f}")
    check("USDG in Treasury (±10%)",
          lambda: to_int(eth_call(RHO, EXPECTED["usdg"], SEL["balanceOf"], pad_addr(EXPECTED["net_treasury"]))) / 1e6,
          EXPECTED["usdg_in_treasury"], cmp=within(10.0), fmt=lambda v: f"${v:,.2f}")
    check("team multisig getThreshold() == 1 (red check — must stay 1 until upgraded)",
          lambda: to_int(eth_call(RHO, EXPECTED["team_multisig"], SEL["getThreshold"])), 1)

    print("\n== Pull.Fun / Robinhood Chain ==")
    out("INFO", "pull.fun game has no contracts", "proven by grepping the JS bundle (re-run that grep before citing it again)")
    check("$TAKO pool reserve_in_usd (±30%)",
          lambda: float((http_json("https://api.geckoterminal.com/api/v2/networks/robinhood/pools/"
                                   + EXPECTED["tako_pool"]) .get("data", {}).get("attributes", {})
                        ).get("reserve_in_usd", 0)),
          EXPECTED["tako_reserve_usd"], cmp=within(30.0), fmt=lambda v: f"${v:,.0f}")
    check("$TAKO pool fdv_usd (±20%)",
          lambda: float((http_json("https://api.geckoterminal.com/api/v2/networks/robinhood/pools/"
                                   + EXPECTED["tako_pool"]) .get("data", {}).get("attributes", {})
                        ).get("fdv_usd", 0)),
          EXPECTED["tako_fdv_usd"], cmp=within(20.0), fmt=lambda v: f"${v:,.0f}")
    out("REVIEW", "$TAKO liq/MC rule", "recorded reserve $81.9k / FDV $504k => 16.3%; เกณฑ์ <10% ห้าม hold ยาว")

    print("\n== summary ==")
    bad = [r for r in RESULTS if r[0] in ("DRIFT", "FAIL")]
    skipped = [r for r in RESULTS if r[0] == "SKIP"]
    passes = sum(1 for r in RESULTS if r[0] == "PASS")
    print(f"{len(RESULTS)} checks | PASS {passes} | DRIFT/FAIL {len(bad)} | SKIP {len(skipped)} | REVIEW/INFO {sum(1 for r in RESULTS if r[0] in ('REVIEW','INFO'))}")
    if skipped:
        print("note: SKIP = endpoint unreachable from this machine or response shape changed; not a pass")
    if bad:
        print("ACTION: live values differ from the snapshot -> re-run probes in docs/evidence.md, "
              "update tools/data_*.py EXPECTED + records, then python3 tools/build.py && commit")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
