"""Generate the Coastline Outfitters practice data (fictional).

Creates data/orders.csv, data/targets.csv, data/service_monthly.csv,
data/coastline.sqlite and data/coastline.xlsx. Re-running gives identical files.
"""
from pathlib import Path
import sqlite3
import numpy as np
import pandas as pd

rng = np.random.default_rng(2026)
OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)

months = pd.date_range("2024-07-01", "2026-06-01", freq="MS")
regions = ["NSW", "VIC", "QLD", "SA", "WA", "Online"]
# typical monthly orders in July 2024
base_orders = {"NSW": 520, "VIC": 470, "QLD": 400, "SA": 230, "WA": 260, "Online": 610}
# camping retail seasonality by calendar month (Dec/Jan peak, Easter in Mar/Apr, winter low)
season = {1: 1.30, 2: 0.95, 3: 1.05, 4: 1.12, 5: 0.80, 6: 0.85,
          7: 0.78, 8: 0.80, 9: 0.92, 10: 1.05, 11: 1.15, 12: 1.45}
# yearly growth by region; WA falls away in FY26 after a competitor opens
growth = {"NSW": 0.04, "VIC": 0.03, "QLD": 0.09, "SA": 0.05, "WA": 0.02, "Online": 0.22}
categories = ["Tents", "Sleeping", "Apparel", "Footwear", "Cooking", "Accessories"]
cat_p = [0.14, 0.13, 0.27, 0.16, 0.12, 0.18]
cat_aov = {"Tents": 410, "Sleeping": 190, "Apparel": 115, "Footwear": 160,
           "Cooking": 95, "Accessories": 48}
cat_margin = {"Tents": 0.38, "Sleeping": 0.42, "Apparel": 0.55, "Footwear": 0.47,
              "Cooking": 0.44, "Accessories": 0.58}

rows = []
oid = 100000
for i, m in enumerate(months):
    t = i / 12
    for r in regions:
        g = (1 + growth[r]) ** t
        if r == "WA" and m >= pd.Timestamp("2025-09-01"):
            g *= 0.86  # competitor opens in Perth, Sep 2025
        n = int(base_orders[r] * season[m.month] * g * rng.normal(1, 0.03))
        days = rng.integers(0, m.days_in_month, n)
        cats = rng.choice(categories, n, p=cat_p)
        for d, c in zip(days, cats):
            oid += 1
            rev = round(float(cat_aov[c] * rng.lognormal(0, 0.35)), 2)
            disc = 0.0
            # heavier discounting online in FY26 squeezes margin
            if r == "Online" and m >= pd.Timestamp("2025-07-01"):
                disc = 0.04
            margin = cat_margin[c] - disc + rng.normal(0, 0.03)
            cost = round(rev * (1 - margin), 2)
            ret_p = 0.09 if r == "Online" else 0.035
            if c == "Footwear" and r == "Online":
                ret_p = 0.17
            rows.append((oid, (m + pd.Timedelta(days=int(d))).date().isoformat(),
                         "Online" if r == "Online" else "Store", r, c, rev, cost,
                         int(rng.random() < ret_p),
                         "New" if rng.random() < (0.38 if r == "Online" else 0.27) else "Returning"))

orders = pd.DataFrame(rows, columns=["order_id", "order_date", "channel", "region",
                                     "category", "revenue", "cost", "returned",
                                     "customer_type"])
orders = orders.sort_values(["order_date", "order_id"]).reset_index(drop=True)
orders["order_id"] = range(100001, 100001 + len(orders))
orders.to_csv(OUT / "orders.csv", index=False)

# Targets: set in June each year from the prior year's actuals plus a planned uplift
orders["month"] = pd.to_datetime(orders["order_date"]).dt.to_period("M").dt.to_timestamp()
act = orders.groupby(["month", "region"])["revenue"].sum().unstack()
uplift = {"NSW": 0.05, "VIC": 0.05, "QLD": 0.07, "SA": 0.05, "WA": 0.05, "Online": 0.18}
tg = []
for m in months:
    for r in regions:
        if m < pd.Timestamp("2025-07-01"):
            # FY25 targets: a smoothed version of what happened, a little optimistic
            v = act.loc[m, r] * rng.normal(1.02, 0.025)
        else:
            v = act.loc[m - pd.DateOffset(years=1), r] * (1 + uplift[r])
        tg.append((m.date().isoformat(), r, round(float(v), -2)))
targets = pd.DataFrame(tg, columns=["month", "region", "revenue_target"])
targets.to_csv(OUT / "targets.csv", index=False)

# Service metrics by month (company level)
svc = []
for i, m in enumerate(months):
    nps = 41 + 3 * np.sin(i / 3) - (6 if m >= pd.Timestamp("2026-02-01") else 0) + rng.normal(0, 1.5)
    stock = 96.5 - (3.5 if pd.Timestamp("2026-01-01") <= m <= pd.Timestamp("2026-04-01") else 0) + rng.normal(0, 0.6)
    deliv = 3.1 + (1.4 if m >= pd.Timestamp("2026-02-01") else 0) + rng.normal(0, 0.15)
    svc.append((m.date().isoformat(), round(float(nps), 1), round(float(stock), 1), round(float(deliv), 1)))
service = pd.DataFrame(svc, columns=["month", "nps", "stock_availability_pct", "avg_delivery_days"])
service.to_csv(OUT / "service_monthly.csv", index=False)

orders = orders.drop(columns="month")
with sqlite3.connect(OUT / "coastline.sqlite") as con:
    orders.to_sql("orders", con, if_exists="replace", index=False)
    targets.to_sql("targets", con, if_exists="replace", index=False)
    service.to_sql("service_monthly", con, if_exists="replace", index=False)

with pd.ExcelWriter(OUT / "coastline.xlsx") as xw:
    orders.to_excel(xw, sheet_name="orders", index=False)
    targets.to_excel(xw, sheet_name="targets", index=False)
    service.to_excel(xw, sheet_name="service_monthly", index=False)

print(f"{len(orders):,} orders, {len(targets)} target rows, {len(service)} service months")

# Dashboard usage log for Chapter 14: 12 weeks after the July 2026 launch
viewers = ["CEO", "CFO", "COO", "Head of Retail", "Head of eCommerce",
           "Head of Marketing", "Head of People", "WA Regional Manager", "Analyst"]
weekly_p = {"CEO": 0.9, "CFO": 0.95, "COO": 0.85, "Head of Retail": 0.8,
            "Head of eCommerce": 0.75, "Head of Marketing": 0.45, "Head of People": 0.15,
            "WA Regional Manager": 0.7, "Analyst": 1.0}
log = []
for w in range(12):
    week_start = pd.Timestamp("2026-07-06") + pd.Timedelta(weeks=w)
    fade = 1.0 if w < 4 else 0.85
    for v in viewers:
        if rng.random() < weekly_p[v] * fade:
            for _ in range(int(rng.integers(1, 4))):
                ts = week_start + pd.Timedelta(days=int(rng.integers(0, 5)),
                                               hours=int(rng.integers(7, 18)))
                log.append((ts.isoformat(sep=" "), v, "Monthly performance"))
usage = pd.DataFrame(log, columns=["viewed_at", "viewer", "report"]).sort_values("viewed_at")
usage.to_csv(OUT / "usage_log.csv", index=False)
print(f"{len(usage)} usage events")
