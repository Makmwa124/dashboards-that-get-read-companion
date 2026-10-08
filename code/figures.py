"""Draw every chart in Dashboards That Get Read.

Run from the companion folder:  python code/figures.py
Images are written to makeovers/ at 300 dpi.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Wedge
import coastline as cl

OUT = Path(__file__).resolve().parent.parent / "makeovers"
OUT.mkdir(exist_ok=True)
cl.style()
o = cl.load()
m = cl.monthly(o)
rf = cl.region_fy(o)
fy26 = o[o["fy"] == 2026]
RAINBOW = ["#e6194b", "#3cb44b", "#ffe119", "#4363d8", "#f58231", "#911eb4"]
MLAB = [d.strftime("%b") for d in m.index]


def save(fig, name):
    fig.savefig(OUT / name, facecolor="white")
    plt.close(fig)


def money(x, pos=None):
    return f"${x/1000:,.0f}k"


# ---------------------------------------------------------------- Chapter 1
def before_overview():
    """The cluttered 14-tile Executive Overview Jess inherited."""
    fig = plt.figure(figsize=(10, 6.2))
    fig.patch.set_facecolor("#e9eef5")
    fig.suptitle("COASTLINE OUTFITTERS - EXECUTIVE OVERVIEW DASHBOARD v3 (FINAL)",
                 fontsize=11, fontweight="bold", color="#003366", x=0.02, ha="left")
    for k, lab in enumerate(["Year", "Month", "Region", "Channel", "Category", "Customer type", "Store"]):
        fig.patches.append(FancyBboxPatch((0.02 + k * 0.137, 0.905), 0.125, 0.032, transform=fig.transFigure,
                                          boxstyle="round,pad=0.002", facecolor="white", edgecolor="#7f9cc0"))
        fig.text(0.03 + k * 0.137, 0.921, f"{lab}: All  \u25be", fontsize=6.5, va="center", color="#003366")
    gs = fig.add_gridspec(3, 5, hspace=0.75, wspace=0.45, top=0.86)
    # gauges
    for j, (lab, val, tgt) in enumerate([("Revenue % Target", 99.96, 100), ("NPS", 37.4, 45),
                                         ("Stock %", 95.3, 97)]):
        ax = fig.add_subplot(gs[0, j])
        for k, c in enumerate(["#d62728", "#ffbf00", "#2ca02c"]):
            ax.add_patch(Wedge((0, 0), 1, 180 - 60 * (k + 1), 180 - 60 * k, width=0.35, color=c))
        ang = np.pi * (1 - min(val / tgt, 1.0))
        ax.plot([0, 0.8 * np.cos(ang)], [0, 0.8 * np.sin(ang)], color="black", lw=2)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-0.2, 1.1); ax.axis("off")
        ax.set_title(lab, fontsize=7.5); ax.text(0, -0.2, f"{val}", ha="center", fontsize=8)
    # pie by category
    ax = fig.add_subplot(gs[0, 3])
    cat = fy26.groupby("category")["revenue"].sum()
    ax.pie(cat, labels=cat.index, colors=RAINBOW, textprops={"fontsize": 5.5}, shadow=True)
    ax.set_title("Sales by Category", fontsize=7.5)
    # donut by channel
    ax = fig.add_subplot(gs[0, 4])
    ch = fy26.groupby("channel")["revenue"].sum()
    ax.pie(ch, labels=ch.index, colors=["#ff7f0e", "#1f77b4"], wedgeprops={"width": 0.4},
           textprops={"fontsize": 6})
    ax.set_title("Channel Mix", fontsize=7.5)
    # spaghetti lines
    ax = fig.add_subplot(gs[1, :3])
    reg = o.groupby(["month", "region"])["revenue"].sum().unstack()
    for c, col in zip(reg.columns, RAINBOW):
        ax.plot(reg.index, reg[c], color=col, lw=1.2, marker="o", ms=2, label=c)
    ax.legend(fontsize=5.5, ncol=6, loc="upper left")
    ax.set_title("Revenue Trend by Region", fontsize=7.5); ax.grid(True, color="#999", lw=0.5)
    ax.tick_params(labelsize=6)
    # dual axis
    ax = fig.add_subplot(gs[1, 3:])
    ax.bar(m.index, m["revenue"], width=20, color="#4f81bd")
    ax2 = ax.twinx(); ax2.plot(m.index, m["margin_pct"], color="#c0504d", lw=1.5); ax2.set_ylim(43.0, 45.5)
    ax.set_title("Revenue vs Margin %", fontsize=7.5); ax.tick_params(labelsize=6); ax2.tick_params(labelsize=6)
    ax2.spines["right"].set_visible(True)
    # KPI number tiles
    tiles = [("Orders", f"{len(fy26):,}"), ("AOV", f"${fy26['revenue'].mean():.2f}"),
             ("Returns", f"{fy26['returned'].mean()*100:.3f}%"),
             ("New Cust %", f"{(fy26['customer_type']=='New').mean()*100:.4f}"),
             ("GP", f"${fy26['gross_profit'].sum():,.2f}")]
    for j, (lab, val) in enumerate(tiles):
        ax = fig.add_subplot(gs[2, j]); ax.axis("off")
        ax.add_patch(FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02", color=RAINBOW[j], alpha=0.85))
        ax.text(0.5, 0.65, lab, ha="center", fontsize=7, color="white", fontweight="bold")
        ax.text(0.5, 0.3, val, ha="center", fontsize=7.5, color="white")
    save(fig, "f01_before_overview.png")


# ---------------------------------------------------------------- Chapter 4
def wireframe():
    fig, ax = plt.subplots(figsize=(7, 4.4))
    ax.set_xlim(0, 100); ax.set_ylim(0, 64); ax.axis("off")
    def box(x, y, w, h, label, sub, shade):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=shade, edgecolor="#555", lw=0.8))
        ax.text(x + 1.5, y + h - 2.6, label, fontsize=8.5, fontweight="bold", va="top")
        ax.text(x + 1.5, y + h - 6.4, sub, fontsize=7, va="top", color="#333")
    box(0, 58, 100, 6, "1  Title, period, refresh stamp", "", "#f2f2f2")
    for i, (l, s) in enumerate([("2  Revenue", "vs target, vs LY"), ("2  Gross margin", "vs LY"),
                                ("2  Orders", "vs LY"), ("2  NPS", "vs LY")]):
        box(i * 25.33, 44, 23.9, 12.5, l, s, "#dfe7f0")
    box(0, 14, 61, 28.5, "3  Main trend", "Monthly revenue vs target,\nthis year and last", "#ffffff")
    box(63, 14, 37, 28.5, "4  Where is it coming from?", "Variance to target\nby region, sorted", "#ffffff")
    box(0, 0, 100, 12.5, "5  What needs attention", "Exceptions table, notes, definitions link", "#f7f7f7")
    save(fig, "f04_wireframe.png")


def kpi_card(ax, title, value, line1, line2, bad=False):
    ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 1, 1, transform=ax.transAxes, facecolor="#f5f7fa", edgecolor="none"))
    ax.text(0.06, 0.82, title, fontsize=7.5, color=cl.DARK, transform=ax.transAxes)
    ax.text(0.06, 0.45, value, fontsize=15, fontweight="bold", color="black", transform=ax.transAxes)
    ax.text(0.06, 0.22, line1, fontsize=6.8, color=cl.ALERT if bad else cl.DARK, transform=ax.transAxes)
    ax.text(0.06, 0.07, line2, fontsize=6.8, color=cl.DARK, transform=ax.transAxes)


def after_overview(name="f04_after_overview.png"):
    fig = plt.figure(figsize=(10, 6.2))
    fig.text(0.02, 0.975, "Coastline Outfitters | Monthly performance", fontsize=12, fontweight="bold")
    fig.text(0.02, 0.945, "FY26 (Jul 2025 - Jun 2026). Revenue ex GST. Data to 30 Jun 2026, refreshed 1 Jul 2026 06:10.",
             fontsize=7.5, color=cl.DARK)
    gs = fig.add_gridspec(3, 4, height_ratios=[0.75, 2.2, 1.25], hspace=0.55, wspace=0.3,
                          top=0.91, bottom=0.04, left=0.03, right=0.98)
    a26, a25 = fy26, o[o["fy"] == 2025]
    rev, rev25 = a26["revenue"].sum(), a25["revenue"].sum()
    tgt = cl.targets().query("fy == 2026")["revenue_target"].sum()
    gm = a26["gross_profit"].sum() / rev * 100
    gm25 = a25["gross_profit"].sum() / rev25 * 100
    svc = pd.read_csv(cl.DATA / "service_monthly.csv", parse_dates=["month"])
    svc["fy"] = cl.fy(svc["month"])
    nps = svc.groupby("fy")["nps"].mean()
    kpi_card(fig.add_subplot(gs[0, 0]), "Revenue", f"${rev/1e6:.2f}m",
             f"On target ({rev/tgt*100:.1f}%)", f"{(rev/rev25-1)*100:+.1f}% vs FY25")
    kpi_card(fig.add_subplot(gs[0, 1]), "Gross margin", f"{gm:.1f}%",
             f"{gm-gm25:+.1f} pts vs FY25", "Online down 4.1 pts", bad=True)
    kpi_card(fig.add_subplot(gs[0, 2]), "Orders", f"{len(a26):,}",
             f"{(len(a26)/len(a25)-1)*100:+.1f}% vs FY25", "Online +19.6%, stores +3.8%")
    kpi_card(fig.add_subplot(gs[0, 3]), "Net Promoter Score", f"{nps[2026]:.0f}",
             f"{nps[2026]-nps[2025]:+.1f} vs FY25", "Delivery times up since Feb", bad=True)
    # main trend
    ax = fig.add_subplot(gs[1, :3])
    cur, ly = m.loc["2025-07":"2026-06"], m.loc["2024-07":"2025-06"]
    x = np.arange(12)
    ax.plot(x, ly["revenue"].values / 1000, color=cl.GREY, lw=2, label="FY25")
    ax.plot(x, cur["revenue_target"].values / 1000, color=cl.DARK, lw=1, ls="--", label="Target")
    ax.plot(x, cur["revenue"].values / 1000, color=cl.ACCENT, lw=2.6, label="FY26")
    ax.set_xticks(x, [d.strftime("%b") for d in cur.index])
    ax.set_ylabel("$k"); ax.set_ylim(0, 760)
    for lab, yv, col in [("FY26", cur["revenue"].iloc[-1] / 1000, cl.ACCENT),
                         ("Target", cur["revenue_target"].iloc[-1] / 1000 + 20, cl.DARK),
                         ("FY25", ly["revenue"].iloc[-1] / 1000 - 40, "#8a8a8a")]:
        ax.text(11.2, yv, lab, color=col, fontsize=7.5, va="center", fontweight="bold")
    ax.set_xlim(-0.3, 12.2)
    ax.set_title("Revenue tracked target all year; December was the biggest month in two years")
    # variance by region
    ax = fig.add_subplot(gs[1, 3])
    v = rf["vs_Target_pct"].sort_values()
    ax.barh(v.index, v.values, color=[cl.ALERT if x < -5 else cl.GREY for x in v.values])
    for i, val in enumerate(v.values):
        ax.text(val + (0.6 if val >= 0 else -0.6), i, f"{val:+.1f}%", va="center",
                ha="left" if val >= 0 else "right", fontsize=7)
    ax.axvline(0, color="black", lw=0.8); ax.set_xlim(-22, 12)
    ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.set_title("WA is 15% under target", fontsize=9.5)
    # attention table
    ax = fig.add_subplot(gs[2, :]); ax.axis("off")
    ax.set_title("Needs attention", fontsize=9.5)
    rows = [["WA stores", "-15.0% vs target", "Competitor opened in Perth (Sep 2025); revenue -10.7% on FY25", "Regional manager"],
            ["Online margin", "40.8% (FY25 44.9%)", "4% extra discounting since July; returns steady at 10%", "Head of eCommerce"],
            ["Delivery time", "4.5 days in June (FY25 3.1)", "Carrier change in Feb 2026; NPS 37, down 5.1 on FY25", "Operations"]]
    tb = ax.table(cellText=rows, colLabels=["Item", "Now", "Why", "Owner"], cellLoc="left",
                  colLoc="left", loc="upper left", colWidths=[0.13, 0.17, 0.52, 0.18])
    tb.auto_set_font_size(False); tb.set_fontsize(7.3); tb.scale(1, 1.35)
    for (r, c), cell in tb.get_celld().items():
        cell.set_edgecolor("#dddddd"); cell.visible_edges = "B"
        if r == 0:
            cell.set_text_props(fontweight="bold")
    save(fig, name)


# ---------------------------------------------------------------- Chapter 5
def bullet_explainer():
    fig, ax = plt.subplots(figsize=(6.4, 1.9))
    for edge, shade in [(120, "#eeeeee"), (100, "#dddddd"), (90, "#c9c9c9")]:
        ax.barh(0, edge, color=shade, height=0.8)
    ax.barh(0, 99.96, color=cl.ACCENT, height=0.28)
    ax.plot([100, 100], [-0.34, 0.34], color="black", lw=2.4)
    ax.set_xlim(0, 120); ax.set_ylim(-0.75, 0.75); ax.set_yticks([])
    ax.set_xticks(range(0, 121, 20), [f"{v}%" for v in range(0, 121, 20)])
    ax.spines["left"].set_visible(False)
    for x, lab in [(45, "below 90%: poor"), (95, "90-100%"), (110, "above 100%")]:
        ax.text(x, 0.5, lab, ha="center", fontsize=7, color=cl.DARK)
    ax.text(50, -0.08, "actual: 99.96%", color="white", fontsize=7.5, va="center", ha="center", fontweight="bold")
    ax.text(101.5, -0.58, "target line", fontsize=7.5, va="center")
    ax.set_title("Bullet chart: FY26 revenue as % of target")
    save(fig, "f05_bullet.png")


# ---------------------------------------------------------------- Chapter 6
def colour_demo():
    r = o.groupby(["month", "region"])["revenue"].sum().unstack()
    yoy = ((r / r.shift(12) - 1) * 100).loc["2025-07":"2026-06"]
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 6.0))
    ax = axes[0]
    for c, col in zip(yoy.columns, RAINBOW):
        ax.plot(yoy.index, yoy[c], color=col, lw=1.6, label=c)
    ax.legend(ncol=6, fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(0, 1.02))
    ax.set_title("Before: Revenue growth vs same month last year (%)", pad=14)
    ax = axes[1]
    for c in yoy.columns:
        hl = c == "WA"
        ax.plot(yoy.index, yoy[c], color=cl.ALERT if hl else cl.GREY, lw=2.4 if hl else 1.2,
                zorder=3 if hl else 2)
    ax.text(yoy.index[-1] + pd.Timedelta(days=8), yoy["WA"].iloc[-1], "WA", fontsize=8,
            va="center", color=cl.ALERT, fontweight="bold")
    ax.text(yoy.index[0] - pd.Timedelta(days=8), 27, "other regions", fontsize=7.5,
            color="#7a7a7a", ha="left")
    ax.set_title("After: WA has been below last year in 8 of the 10 months since September", pad=8)
    for a in axes:
        a.axhline(0, color="black", lw=0.8)
        a.set_ylim(-30, 40); a.set_ylabel("% vs last year")
        a.set_xticks(yoy.index, [d.strftime("%b") for d in yoy.index], fontsize=7)
    fig.tight_layout(h_pad=2.5)
    save(fig, "f06_colour.png")


# ---------------------------------------------------------------- Chapter 7
def titles_demo():
    cat = fy26.groupby("category")["revenue"].sum().sort_values()
    cat25 = o[o["fy"] == 2025].groupby("category")["revenue"].sum().reindex(cat.index)
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 5.4))
    ax = axes[0]
    y = np.arange(len(cat))
    ax.barh(y - 0.2, cat25 / 1000, height=0.4, color="#4f81bd", label="FY25")
    ax.barh(y + 0.2, cat / 1000, height=0.4, color="#c0504d", label="FY26")
    ax.set_yticks(y, cat.index); ax.legend(fontsize=7); ax.grid(True, axis="x", color="#ccc")
    ax.set_title("Revenue by Category"); ax.set_xlabel("Revenue ($000s)")
    ax = axes[1]
    ax.barh(y - 0.2, cat25 / 1000, height=0.4, color=cl.GREY)
    ax.barh(y + 0.2, cat / 1000, height=0.4, color=cl.ACCENT)
    for i, (a, b) in enumerate(zip(cat25, cat)):
        ax.text(b / 1000 + 15, i + 0.2, f"${b/1000:,.0f}k  ({(b/a-1)*100:+.0f}%)", va="center", fontsize=7.2)
    ax.set_yticks(y, cat.index); ax.set_xticks([]); ax.spines["bottom"].set_visible(False)
    ax.tick_params(axis="y", length=0); ax.set_xlim(0, 2600)
    ax.set_title("Tents are 37% of revenue; every category grew in FY26")
    ax.text(cat25.iloc[0] / 1000 + 15, -0.2, "FY25", color="#7a7a7a", fontsize=7, va="center")
    ax.text(cat.iloc[0] / 1000 + 440, 0.2, "FY26", color=cl.ACCENT, fontsize=7, va="center", fontweight="bold")
    fig.tight_layout(h_pad=2.5)
    save(fig, "f07_titles.png")


# ---------------------------------------------------------------- Chapter 8
def target_demo():
    cur = m.loc["2025-07":"2026-06"]
    var = (cur["revenue"] - cur["revenue_target"]) / 1000
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.4, 4.6), height_ratios=[2.2, 1], sharex=True)
    x = np.arange(12)
    a1.bar(x, cur["revenue"] / 1000, color=cl.GREY, width=0.65)
    a1.scatter(x, cur["revenue_target"] / 1000, marker="_", s=260, color="black", lw=2, zorder=3)
    a1.set_ylabel("$k"); a1.set_title("Monthly revenue (bars) against target (black marks), FY26")
    a1.text(11.45, cur["revenue_target"].iloc[-1] / 1000, "target", fontsize=7, va="center")
    sd = (cur["revenue"] / cur["revenue_target"] - 1).std() * 100
    pct = (cur["revenue"] / cur["revenue_target"] - 1) * 100
    a2.bar(x, var, color=[cl.ACCENT if v >= 0 else (cl.ALERT if p < -sd else cl.GREY)
                          for v, p in zip(var, pct)], width=0.65)
    a2.axhline(0, color="black", lw=0.8)
    for i, v in enumerate(var):
        a2.text(i, v + (2 if v >= 0 else -2), f"{v:+.0f}", ha="center", va="bottom" if v >= 0 else "top", fontsize=6.8)
    a2.set_ylabel("$k vs target"); a2.set_ylim(-36, 36)
    a2.set_xticks(x, [d.strftime("%b") for d in cur.index])
    fig.tight_layout()
    save(fig, "f08_target.png")


# ---------------------------------------------------------------- Chapter 9
def table_demo(name="f09_table.png"):
    reg = o[o["fy"] == 2026].groupby(["region", "month"])["revenue"].sum().unstack()
    t = rf.sort_values("vs_Target_pct")
    fig = plt.figure(figsize=(6.6, 2.9))
    cols = ["Region", "FY26 revenue", "vs target", "vs FY25", "Trend (Jul-Jun)"]
    xs = [0.0, 0.2, 0.42, 0.6, 0.78]
    fig.text(0.0, 0.97, "Region scorecard, FY26", fontsize=10, fontweight="bold")
    for xpos, c in zip(xs, cols):
        fig.text(xpos, 0.86, c, fontsize=7.8, fontweight="bold", color=cl.DARK,
                 ha="left" if xpos in (0.0, 0.78) else "right" if False else "left")
    fig.add_artist(plt.Line2D([0, 1], [0.84, 0.84], color="#888", lw=0.8))
    rowh = 0.125
    for i, (r, row) in enumerate(t.iterrows()):
        y = 0.76 - i * rowh
        vt = row["vs_Target_pct"]
        shade = "#f6d5d9" if vt < -5 else ("#fbeced" if vt < 0 else "#ffffff")
        fig.add_artist(Rectangle((0.405, y - 0.045), 0.15, 0.1, facecolor=shade, edgecolor="none",
                                 transform=fig.transFigure))
        fig.text(xs[0], y, r, fontsize=8, va="center")
        fig.text(xs[1] + 0.14, y, f"${row['FY26']/1000:,.0f}k", fontsize=8, va="center", ha="right")
        fig.text(xs[2] + 0.12, y, f"{vt:+.1f}%", fontsize=8, va="center", ha="right",
                 fontweight="bold" if vt < -5 else "normal")
        fig.text(xs[3] + 0.12, y, f"{row['vs_LY_pct']:+.1f}%", fontsize=8, va="center", ha="right")
        ax = fig.add_axes([xs[4], y - 0.045, 0.2, 0.09]); ax.axis("off")
        s = reg.loc[r].values
        ax.plot(s, color=cl.ALERT if vt < -5 else cl.DARK, lw=1.1)
        ax.scatter([11], [s[-1]], s=6, color=cl.ALERT if vt < -5 else cl.DARK)
        fig.add_artist(plt.Line2D([0, 1], [y - 0.06, y - 0.06], color="#e3e3e3", lw=0.6))
    save(fig, name)


# ---------------------------------------------------------------- Chapter 13 makeovers
def m1_pie():
    cat = fy26.groupby("category")["revenue"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(4.6, 3.4))
    ax.pie(cat, labels=cat.index, colors=RAINBOW, autopct="%1.1f%%", startangle=90,
           textprops={"fontsize": 7.5}, explode=[0.05] * 6, shadow=True)
    ax.set_title("Sales Breakdown by Product Category FY26")
    save(fig, "m1_before.png")
    cat = cat.sort_values()
    share = cat / cat.sum() * 100
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    ax.barh(cat.index, share, color=[cl.ACCENT if c == "Tents" else cl.GREY for c in cat.index])
    for i, (s, v) in enumerate(zip(share, cat)):
        ax.text(s + 0.6, i, f"{s:.0f}%   ${v/1000:,.0f}k", va="center", fontsize=7.8)
    ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.tick_params(axis="y", length=0)
    ax.set_xlim(0, 48)
    ax.set_title("Tents earn more than a third of revenue, nearly twice the next category")
    save(fig, "m1_after.png")


def m2_small_multiples():
    reg = o.groupby(["month", "region"])["revenue"].sum().unstack() / 1000
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    for c, col in zip(reg.columns, RAINBOW):
        ax.plot(reg.index, reg[c], color=col, marker="o", ms=2.5, lw=1.2, label=c)
    ax.legend(fontsize=6.5, ncol=3); ax.grid(True, color="#bbb")
    ax.set_title("Monthly Revenue by Region ($000)")
    save(fig, "m2_before.png")
    order = rf.sort_values("FY26", ascending=False).index
    fig, axes = plt.subplots(2, 3, figsize=(6.4, 3.8), sharex=True)
    x = np.arange(12)
    for ax, r in zip(axes.flat, order):
        cur = reg[r].loc["2025-07":"2026-06"].values
        ly = reg[r].loc["2024-07":"2025-06"].values
        bad = r == "WA"
        ax.plot(x, ly, color=cl.GREY, lw=1.4)
        ax.plot(x, cur, color=cl.ALERT if bad else cl.ACCENT, lw=1.9)
        ax.set_title(f"{r}  {rf.loc[r, 'vs_LY_pct']:+.0f}%", fontsize=8.5,
                     color=cl.ALERT if bad else "black")
        ax.set_ylim(0, None); ax.tick_params(labelsize=6.5)
        ax.set_xticks([0, 6, 11], ["Jul", "Jan", "Jun"])
    fig.suptitle("Every region grew on FY25 except WA (FY26 in colour, FY25 in grey, $k)",
                 x=0.01, ha="left", fontsize=9.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "m2_after.png")


def m3_gauges():
    vals = [("Revenue vs target", 99.96, 100), ("NPS", 37.4, 45), ("Stock availability", 95.3, 97)]
    fig, axes = plt.subplots(1, 3, figsize=(6.2, 2.0))
    for ax, (lab, v, tgt) in zip(axes, vals):
        for k, c in enumerate(["#d62728", "#ffbf00", "#2ca02c"]):
            ax.add_patch(Wedge((0, 0), 1, 180 - 60 * (k + 1), 180 - 60 * k, width=0.35, color=c))
        ang = np.pi * (1 - min(v / tgt, 1.0))
        ax.plot([0, 0.8 * np.cos(ang)], [0, 0.8 * np.sin(ang)], color="black", lw=2)
        ax.set_xlim(-1.1, 1.1); ax.set_ylim(-0.3, 1.1); ax.axis("off"); ax.set_aspect("equal")
        ax.set_title(lab, fontsize=8); ax.text(0, -0.28, f"{v}", ha="center", fontsize=9)
    save(fig, "m3_before.png")
    fig, axes = plt.subplots(3, 1, figsize=(6.2, 2.1))
    specs = [("Revenue % of target", 99.96, 100, [90, 100, 120], "%"),
             ("NPS", 37.4, 45, [30, 40, 60], ""),
             ("Stock availability %", 95.3, 97, [93, 96, 100], "%")]
    for ax, (lab, v, tgt, bands, unit) in zip(axes, specs):
        lo = 0
        for b, sh in zip(sorted(bands, reverse=True), ["#eeeeee", "#dddddd", "#c9c9c9"]):
            ax.barh(0, b - lo, left=lo, color=sh, height=0.8)
        ax.barh(0, v - lo, left=lo, color=cl.ALERT if v < tgt * 0.95 else cl.ACCENT, height=0.32)
        ax.plot([tgt, tgt], [-0.35, 0.35], color="black", lw=2)
        ax.set_xlim(lo, max(bands)); ax.set_yticks([0], [lab]); ax.tick_params(axis="y", length=0, labelsize=7.5)
        ax.tick_params(axis="x", labelsize=6.5); ax.spines["left"].set_visible(False)
        ax.text(max(bands), 0, f"  {v}{unit} (target {tgt}{unit})", va="center", fontsize=7.2)
    fig.suptitle("Revenue is on target, stock is just below, NPS is well short", x=0.01, ha="left",
                 fontsize=9.5, fontweight="bold")
    fig.tight_layout()
    save(fig, "m3_after.png")


def m4_dual_axis():
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    ax.bar(m.index, m["revenue"] / 1000, width=20, color="#4f81bd", label="Revenue")
    ax2 = ax.twinx(); ax2.spines["right"].set_visible(True)
    ax2.plot(m.index, m["margin_pct"], color="#c0504d", lw=2, label="GM%")
    ax2.set_ylim(43.0, 45.5); ax.set_title("Revenue ($000) and Gross Margin %")
    fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.86), fontsize=7)
    save(fig, "m4_before.png")
    ch = o.groupby(["month", "channel"]).agg(rev=("revenue", "sum"), gp=("gross_profit", "sum"))
    ch["gm"] = ch["gp"] / ch["rev"] * 100
    gm = ch["gm"].unstack()
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.2, 4.0), sharex=True)
    a1.bar(m.index, m["revenue"] / 1000, width=20, color=cl.GREY)
    a1.set_ylabel("$k"); a1.set_title("Revenue is seasonal and up 8.7% on last year")
    a2.plot(gm.index, gm["Store"], color=cl.GREY, lw=1.8)
    a2.plot(gm.index, gm["Online"], color=cl.ALERT, lw=2.2)
    a2.text(gm.index[-1] + pd.Timedelta(days=12), gm["Store"].iloc[-1], "Stores", fontsize=7.5, va="center", color="#7a7a7a")
    a2.text(gm.index[-1] + pd.Timedelta(days=12), gm["Online"].iloc[-1], "Online", fontsize=7.5, va="center", color=cl.ALERT)
    a2.axvline(pd.Timestamp("2025-07-01"), color="#999", lw=0.8, ls=":")
    a2.text(pd.Timestamp("2025-07-20"), 38.4, "Online discount raised July 2025", fontsize=6.8, va="bottom", color=cl.DARK)
    a2.set_ylim(38, 47); a2.set_ylabel("Gross margin %")
    a2.set_title("Online margin dropped 4 points in July 2025 and has not recovered")
    fig.tight_layout()
    save(fig, "m4_after.png")


def m5_rag_table():
    t = rf.copy()
    fig, ax = plt.subplots(figsize=(6.2, 2.4)); ax.axis("off")
    cells, colours = [], []
    for r, row in t.iterrows():
        cells.append([r, f"{row['FY26']:,.2f}", f"{row['Target']:,.2f}", f"{row['vs_Target_pct']/100:.4f}",
                      f"{row['FY25']:,.2f}", f"{row['vs_LY_pct']/100:.4f}"])
        rag = lambda v: "#ff4d4d" if v < -2 else ("#ffd24d" if v < 2 else "#5cd65c")
        colours.append(["white", "white", "white", rag(row["vs_Target_pct"]), "white", rag(row["vs_LY_pct"])])
    tb = ax.table(cellText=cells, cellColours=colours,
                  colLabels=["Region", "Revenue FY26", "Target FY26", "Var % Tgt", "Revenue FY25", "Var % LY"],
                  loc="center")
    tb.auto_set_font_size(False); tb.set_fontsize(7); tb.scale(1, 1.4)
    save(fig, "m5_before.png")
    table_demo("m5_after.png")


def m6_returns():
    r = fy26.groupby(["category", "channel"])["returned"].mean().unstack() * 100
    fig, ax = plt.subplots(figsize=(6.2, 2.8))
    r.plot.bar(ax=ax, color=["#9bbb59", "#8064a2"], edgecolor="black", width=0.75)
    ax.set_title("Return Rate % by Category and Channel"); ax.grid(True, axis="y", color="#bbb")
    ax.set_xlabel(""); ax.tick_params(axis="x", rotation=45)
    save(fig, "m6_before.png")
    r = r.sort_values("Online")
    fig, ax = plt.subplots(figsize=(6.2, 2.9))
    y = np.arange(len(r))
    ax.hlines(y, r["Store"], r["Online"], color="#d0d0d0", lw=2.5)
    ax.scatter(r["Store"], y, color=cl.GREY, s=40, zorder=3)
    ax.scatter(r["Online"], y, color=[cl.ALERT if c == "Footwear" else cl.ACCENT for c in r.index], s=40, zorder=3)
    for i, c in enumerate(r.index):
        ax.text(r.loc[c, "Online"] + 0.4, i, f"{r.loc[c, 'Online']:.0f}%", va="center", fontsize=7.5)
        ax.text(r.loc[c, "Store"] - 0.4, i, f"{r.loc[c, 'Store']:.0f}%", va="center", ha="right", fontsize=7.5, color="#7a7a7a")
    ax.set_yticks(y, r.index); ax.tick_params(axis="y", length=0); ax.set_xlim(0, 19)
    ax.set_xticks([]); ax.spines["bottom"].set_visible(False); ax.spines["left"].set_visible(False)
    ax.text(r["Store"].iloc[0], -0.75, "Store", color="#7a7a7a", fontsize=7.5, ha="center")
    ax.text(r["Online"].iloc[0], -0.75, "Online", color=cl.ACCENT, fontsize=7.5, ha="center")
    ax.set_ylim(-1.1, len(r) - 0.5)
    ax.set_title("Online footwear is returned 15% of the time, four times the store rate", pad=12)
    save(fig, "m6_after.png")


if __name__ == "__main__":
    for f in [before_overview, wireframe, after_overview, bullet_explainer, colour_demo,
              titles_demo, target_demo, table_demo, m1_pie, m2_small_multiples, m3_gauges,
              m4_dual_axis, m5_rag_table, m6_returns]:
        f()
    print("Charts written to", OUT)
