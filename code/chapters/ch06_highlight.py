# Chapter 6: grey for context, one colour for the story
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
import matplotlib.pyplot as plt
import coastline as cl

def highlight_lines(df, focus, title, colour="#C8102E"):
    """Plot every column of df in grey, then the focus column."""
    fig, ax = plt.subplots(figsize=(6.4, 3))
    for col in df.columns:
        if col != focus:
            ax.plot(df.index, df[col], color="#BDBDBD", lw=1.2)
    ax.plot(df.index, df[focus], color=colour, lw=2.4)
    ax.text(df.index[-1], df[focus].iloc[-1], f"  {focus}",
            color=colour, va="center", fontweight="bold")
    ax.axhline(0, color="black", lw=0.8)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title(title, loc="left", fontweight="bold")
    return fig

o = cl.load()
rev = o.groupby(["month", "region"])["revenue"].sum().unstack()
yoy = (rev / rev.shift(12) - 1).loc["2025-07":] * 100
fig = highlight_lines(yoy, "WA", "WA is the only region shrinking")
fig.savefig("ch06_highlight.png", dpi=200, bbox_inches="tight")
print(yoy["WA"].round(1).tolist())
