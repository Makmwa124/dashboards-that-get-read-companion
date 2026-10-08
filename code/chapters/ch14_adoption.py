# Chapter 14: is the dashboard being used? Weekly active viewers from a usage log
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import pandas as pd
import coastline as cl

usage = pd.read_csv(cl.DATA / "usage_log.csv", parse_dates=["viewed_at"])
usage = usage[usage["viewer"] != "Analyst"]  # don't count the builder
audience = 8  # people the dashboard was built for

usage["week"] = usage["viewed_at"].dt.to_period("W-SUN").dt.start_time
weekly = usage.groupby("week").agg(views=("viewer", "size"),
                                   active_viewers=("viewer", "nunique"))
weekly["reach_pct"] = weekly["active_viewers"] / audience * 100
print(weekly.round(1).to_string())

never_weekly = (usage.groupby("viewer")["week"].nunique()
                .sort_values()
                .rename("weeks_active_of_12"))
print("\n", never_weekly.head(3).to_string(), sep="")
