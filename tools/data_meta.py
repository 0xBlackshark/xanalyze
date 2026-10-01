# -*- coding: utf-8 -*-
"""Per-project metadata merged into records by tools/build.py:
field 7 (value-for-money verdict), budget ladder numbers, verification date.
Keep this file in sync with tools/data_*.py — build.py will fail on unknown slugs."""

META = {
 "renaiss": dict(
   verified_on="2026-09-30",
   value_for_money=("จ่าย 28 ได้ความน่าจะเป็นกลับ 31.00 (EV +10.7%) แต่ขายกลับทันที net -5.9% เพราะ haircut 15% + fee 2% "
     "=> 'คุ้มค่าตั๋ว' สูงสุดในบรรดาเว็บ gacha ที่ตรวจมา เพราะมีหมอนรองเป็นของจริงบนเชน; "
     "ที่ไม่คุ้มคือสภาพคล่องขาออก (~5 ดีล/วัน) ทำให้การเล่นใหญ่ต้องรอหรือยอมถูกกดราคา"),
   budget_min_usd=28, budget_entry_usd=100, budget_max_sane_usd=1000,
   capital_rule=("ถ้าจะเข้า: 28-300 USD ต่อ session, ซื้อเฉพาะรุ่นที่ EV เป็นบวก, ตั้งเป้า exit ผ่าน orderbook ที่ +/-10% ของ FMV; "
     "ห้ามเกิน 1,000 USD จนกว่าจะเห็น 30 ดีลล่าสุด > $20k/สัปดาห์; อย่าตีความว่า EV บวก = กำไรแน่นอน (FMV ตั้งเอง + haircut)")),
 "netnet": dict(
   verified_on="2026-09-30",
   value_for_money=("คุ้มสำหรับคนที่อยากมี NAV instrument ที่ verify กันเองได้ครบ — prospectus+contract ตรงกัน 100% ที่เราตรวจวันนี้; "
     "แต่ไม่คุ้มเชิงตลาดตอนนี้: คุณจ่าย $435.98 เพื่อได้ backing $173.46 (premium ~2.51×) และ round trip swap tax 5%+5% ≈ 9.75% ก่อนเห็น yield; "
     "อีกเรื่อง: float มีแค่ 3.9% ของ supply (MC $2.1M บน FDV $53.6M) ทำให้ราคาเป็นอาณาเขตของคนน้อยเดินง่าย"),
   budget_min_usd=500, budget_entry_usd=500, budget_max_sane_usd=5000,
   capital_rule=("เข้าเฉพาะเมื่อ premium < 1.1 (1 NET ≈ 1 USDG working บน NAV ไม่ใช่ market); ที่ ~2.51× คุณซื้อ ~$173.46 ของ NAV ด้วย $435.98 + tax ทีละสอง "
     "=> ถ้าจะเข้าตอนนี้ให้มองว่าเป็น yield position ต้องถือ 8-16 วันกว่า rebase จะมีผล; split order ทุกครั้งเมื่อ > $5k และตั้ง stop อย่างเข้มงวดเพราะ float มีแค่ $2.1M")),
 "pullfun": dict(
   verified_on="2026-09-30",
   value_for_money=("เหมาะในฐานะที่เล่นบันเทิงราคาถูก — odds เปิดเผย, sell-back 90/80%, fair-verify off-chain; "
     "แต่ไม่มี on-chain escrow เรื่องในคลังและ $TAKO (Robinhood) เป็นลอตเตอรี่ 7 วัน: reserve $81,944 ต่อ MC $503,785 (16.3%), ลง 88% จากไฮวันแรก"),
   budget_min_usd=10, budget_entry_usd=100, budget_max_sane_usd=500,
   capital_rule=("เพดาน $500 ครอบ 'เครื่องร้าน/pull + consign' ทั้งหมดรวมกัน — ห้ามฝากเกินนี้เพราะ escrow คลังตรวจไม่ได้และไม่มี recourse ต่อนิติบุคคลนิรนาม; "
     "$TAKO เป็น instrument อื่น (token 2/10): default แนะนำข้าม — ถ้าบังคับจะเล่น จำกัด ≤$500 ต่อ position (~0.6% ของ reserve $81.9k) และ exit ทันทีเมื่อ reserve/MC < 10%")),
 "trace": dict(
   verified_on="2026-09 (รอบแรก — raw artifacts ไม่ได้ persist)",
   value_for_money="ที่ floor 0.0108 ETH ราคาค่อนข้างถูกสำหรับ collection ที่มี on-chain activity จริง แต่ volume 59.39 ETH/7วัน แปลว่าขายยาก => 'ถูกแต่สภาพคล่องต่ำ'",
   budget_min_usd=50, budget_entry_usd=50, budget_max_sane_usd=200,
   capital_rule="ซื้อได้เฉพาะฐานะของสะสม ไม่เกิน $200; ห้ามมองเป็น investment จนกว่า proxy ที่เว็บแสดงจะตรงกับ contract จริง"),
 "clickihood": dict(
   verified_on="2026-09 (รอบแรก — raw artifacts ไม่ได้ persist)",
   value_for_money="ฟรี (mint หมดแล้ว) — ต้นทุนเหลือ gas + ค่าซื้อตลาดรอง; ความเสี่ยงหลักคือ metadata ยังไม่ freeze",
   budget_min_usd=0, budget_entry_usd=0, budget_max_sane_usd=50,
   capital_rule="อย่าซื้อ; ถ้าอยากได้ให้รอ event/allowlist. งบที่สมเหตุสมผลคือ $0"),
 "hypest": dict(
   verified_on="2026-09 (รอบแรก — ข้อมูลไม่ครบโดยเจตนา)",
   value_for_money="ยังไม่คุ้มจ่าย — prize pool ยังไม่ถูกผูกกับ on-chain escrow ที่ตรวจพบ",
   budget_min_usd=0, budget_entry_usd=0, budget_max_sane_usd=0,
   capital_rule="ใช้แรง/เวลาเท่านั้น จนกว่าจะประกาศ contract address ของ escrow แล้วตรวจสอบว่าถือ 690M $HYPE จริง"),
 "agnt": dict(
   verified_on="2026-09 (รอบแรก — ข้อมูลไม่ครบโดยเจตนา)",
   value_for_money="ไม่คุ้มที่ state ปัจจุบัน (mint 25.3%, concentration 63%, claimsOpen=false)",
   budget_min_usd=0, budget_entry_usd=0, budget_max_sane_usd=0,
   capital_rule="รอ claimsOpen=true และ top-10 < 40% ก่อนแล้วค่อยพิจารณา; ตอนนี้ $0"),
 "memebitcoin": dict(
   verified_on="2026-09 (รอบแรก)",
   value_for_money="ติดลบโดยคณิตศาสตร์ — ไม่มีความคุ้มค่ายในทุกระดับราคา",
   budget_min_usd=0, budget_entry_usd=0, budget_max_sane_usd=0,
   capital_rule="ห้ามเข้า (ห้ามแม้แต่ $100)"),
}
