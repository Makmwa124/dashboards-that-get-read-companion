# Chapter 5: a bullet chart, the compact replacement for a gauge
import matplotlib.pyplot as plt

def bullet(ax, actual, target, bands, label, colour="#1F4E79"):
    """Grey bands (worst to best), a thin actual bar, a target line."""
    shades = ["#c9c9c9", "#dddddd", "#eeeeee"]
    for edge, shade in sorted(zip(bands, shades), reverse=True):
        ax.barh(0, edge, color=shade, height=0.8)
    ax.barh(0, actual, color=colour, height=0.28)
    ax.plot([target, target], [-0.34, 0.34], color="black", lw=2.4)
    ax.set_xlim(0, max(bands))
    ax.set_yticks([0], [label])
    ax.spines[["top", "right", "left"]].set_visible(False)

fig, ax = plt.subplots(figsize=(6.4, 1.2))
bullet(ax, actual=99.96, target=100, bands=[90, 100, 120],
       label="Revenue % of target")
ax.set_xticks(range(0, 121, 20), [f"{v}%" for v in range(0, 121, 20)])
fig.savefig("ch05_bullet.png", dpi=300, bbox_inches="tight")
print("saved ch05_bullet.png")
