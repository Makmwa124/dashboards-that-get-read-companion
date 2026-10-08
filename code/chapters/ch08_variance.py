# Chapter 8: monthly variance to target and to last year
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import coastline as cl

m = cl.monthly()
m["revenue_ly"] = m["revenue"].shift(12)
fy26 = m.loc["2025-07":"2026-06"].copy()
fy26["var_target"] = fy26["revenue"] - fy26["revenue_target"]
fy26["var_target_pct"] = (fy26["var_target"]
                          / fy26["revenue_target"] * 100)
fy26["var_ly_pct"] = (fy26["revenue"] / fy26["revenue_ly"] - 1) * 100
fy26["ytd_var_target"] = fy26["var_target"].cumsum()

out = fy26[["revenue", "revenue_target", "var_target", "var_target_pct",
            "var_ly_pct", "ytd_var_target"]]
out.columns = ["revenue", "target", "var", "var_%", "vs_LY_%", "ytd_var"]
out.index = out.index.strftime("%b %y")
print(out.round(1).to_string())

# How big is a normal monthly miss?
sd = fy26["var_target_pct"].std()
print(f"\nTypical monthly variance (1 standard deviation): {sd:.1f}%")
outside = (fy26["var_target_pct"].abs() > 2 * sd).sum()
print("Months outside +/- 2 SD:", outside)
