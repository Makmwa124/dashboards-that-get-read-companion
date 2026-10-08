# Chapter 11: the numbers the DAX measures should return, reproduced in pandas.
# Use this to test your Power BI model: put the same visuals on a page and compare.
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import coastline as cl

o = cl.load()
m = cl.monthly(o)
m["revenue_ly"] = m["revenue"].shift(12)

# A card filtered to June 2026
jun = m.loc["2026-06-01"]
print("June 2026")
print(f"  Revenue            {jun['revenue']:>12,.0f}")
print(f"  Revenue Target     {jun['revenue_target']:>12,.0f}")
print(f"  Revenue vs Target %{(jun['revenue'] / jun['revenue_target'] - 1):>12.1%}")
print(f"  Revenue LY         {jun['revenue_ly']:>12,.0f}")
print(f"  Revenue vs LY %    {(jun['revenue'] / jun['revenue_ly'] - 1):>12.1%}")

# Revenue YTD (financial year ending 30 June) at December 2025
ytd = m.loc["2025-07-01":"2025-12-01", "revenue"].sum()
print(f"\nRevenue YTD at Dec 2025: {ytd:,.0f}")

# Gross margin % and points vs LY for the whole of FY26, by channel
g = o.groupby(["channel", "fy"])[["revenue", "gross_profit"]].sum()
gm = (g["gross_profit"] / g["revenue"]).unstack()
gm["pts_vs_ly"] = (gm[2026] - gm[2025]) * 100
print("\nGross margin by channel")
print(gm.round(4).to_string())
