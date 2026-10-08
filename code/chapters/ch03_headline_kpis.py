# Chapter 3: the four headline numbers for FY26, each with its comparison
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import pandas as pd
import coastline as cl

o = cl.load()
t = cl.targets()
svc = pd.read_csv(cl.DATA / "service_monthly.csv", parse_dates=["month"])
svc["fy"] = cl.fy(svc["month"])

def headline(year):
    d = o[o["fy"] == year]
    return pd.Series({
        "revenue": d["revenue"].sum(),
        "gross_margin_pct": (d["gross_profit"].sum()
                             / d["revenue"].sum() * 100),
        "orders": len(d),
        "nps": svc.loc[svc["fy"] == year, "nps"].mean(),
    })

kpi = pd.DataFrame({"FY25": headline(2025), "FY26": headline(2026)})
kpi["change"] = kpi["FY26"] - kpi["FY25"]
kpi["change_pct"] = kpi["change"] / kpi["FY25"] * 100
print(kpi.round(1))
target = t.loc[t["fy"] == 2026, "revenue_target"].sum()
print(f"\nFY26 revenue target: ${target:,.0f}")
pct = kpi.loc["revenue", "FY26"] / target * 100
print(f"Revenue as % of target: {pct:.2f}%")
