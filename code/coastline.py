"""Shared helpers for the Dashboards That Get Read examples.

load() returns the order-level data with month, financial year and gross profit
columns added. monthly() and region_fy() build the summary tables used across
the book. The colour constants are the palette from Chapter 6.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib as mpl

DATA = Path(__file__).resolve().parent.parent / "data"

# Chapter 6 palette: grey for context, one accent, one alert colour
GREY = "#BDBDBD"
DARK = "#4D4D4D"
ACCENT = "#1F4E79"
ALERT = "#C8102E"
GOOD = "#2E7D32"


def fy(dates):
    """Australian financial year: July 2025 to June 2026 is FY26 -> 2026."""
    d = pd.to_datetime(dates)
    return np.where(d.dt.month >= 7, d.dt.year + 1, d.dt.year)


def load():
    o = pd.read_csv(DATA / "orders.csv", parse_dates=["order_date"])
    o["month"] = o["order_date"].dt.to_period("M").dt.to_timestamp()
    o["fy"] = fy(o["order_date"])
    o["gross_profit"] = o["revenue"] - o["cost"]
    return o


def targets():
    t = pd.read_csv(DATA / "targets.csv", parse_dates=["month"])
    t["fy"] = fy(t["month"])
    return t


def monthly(orders=None):
    o = load() if orders is None else orders
    m = (o.groupby("month")
          .agg(revenue=("revenue", "sum"), orders=("order_id", "count"),
               gross_profit=("gross_profit", "sum"))
          .join(targets().groupby("month")["revenue_target"].sum()))
    m["margin_pct"] = m["gross_profit"] / m["revenue"] * 100
    return m


def region_fy(orders=None):
    o = load() if orders is None else orders
    a = o.groupby(["region", "fy"])["revenue"].sum().unstack()
    t = targets().groupby(["region", "fy"])["revenue_target"].sum().unstack()
    out = pd.DataFrame({"FY25": a[2025], "FY26": a[2026], "Target": t[2026]})
    out["vs_LY_pct"] = (out["FY26"] / out["FY25"] - 1) * 100
    out["vs_Target_pct"] = (out["FY26"] / out["Target"] - 1) * 100
    return out


def style():
    """Quiet matplotlib defaults: no top/right spines, light grid, Inter if present."""
    mpl.rcParams.update({
        "font.family": ["Inter", "DejaVu Sans"],
        "font.size": 9,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#9E9E9E",
        "axes.titlesize": 10.5,
        "axes.titleweight": "bold",
        "axes.titlelocation": "left",
        "axes.labelcolor": DARK,
        "xtick.color": DARK,
        "ytick.color": DARK,
        "axes.grid": False,
        "figure.dpi": 100,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
    })
