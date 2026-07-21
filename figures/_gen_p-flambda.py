"""Generate figures/p-flambda.svg — wavelength vs frequency across the amateur bands.

lambda(m) = 300 / f(MHz)  (the canon's working quick-conversion form).
Single-color (pure black) output on a transparent background; post-processed
by the caller into a theme-able (currentColor) inline SVG fragment.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

f_mhz = np.logspace(0, np.log10(400), 400)
wavelength = 300.0 / f_mhz

fig, ax = plt.subplots(figsize=(6.4, 4.8))

ax.plot(f_mhz, wavelength, color="black", linewidth=2.2, solid_capstyle="round", zorder=3)

# Amateur band points, named by their nominal wavelength; frequency follows
# the same lambda = 300/f convention used throughout the book (matches the
# canon's own anchor values for 80/40/20/10 m exactly).
bands = [
    ("160 m", 160.0, (8, 8)),
    ("80 m", 80.0, (8, 8)),
    ("40 m", 40.0, (8, 8)),
    ("20 m", 20.0, (8, 8)),
    ("10 m", 10.0, (8, 8)),
    ("2 m", 2.0, (-42, -16)),
]

for name, lam, (dx, dy) in bands:
    f = 300.0 / lam
    ax.plot([f], [lam], marker="o", color="black", markersize=6,
            markeredgecolor="black", zorder=5)
    ax.annotate(f"{name}\n{f:g} MHz", (f, lam), textcoords="offset points",
                xytext=(dx, dy), fontsize=9.5, color="black", ha="left")

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(1, 400)
ax.set_ylim(1, 400)

ticks = [1, 10, 100]
ax.set_xticks(ticks)
ax.set_xticklabels([str(t) for t in ticks], color="black")
ax.set_yticks(ticks)
ax.set_yticklabels([str(t) for t in ticks], color="black")
ax.xaxis.set_minor_formatter(mticker.NullFormatter())
ax.yaxis.set_minor_formatter(mticker.NullFormatter())

ax.set_xlabel("Frequency  f  (MHz)", fontsize=11, color="black")
ax.set_ylabel("Wavelength  λ  (m)", fontsize=11, color="black")
ax.set_title(r"$\lambda\ (\mathrm{m}) = 300 \,/\, f\ (\mathrm{MHz})$", fontsize=13, color="black")

for spine in ax.spines.values():
    spine.set_color("black")
ax.tick_params(colors="black", labelsize=9.5)
ax.grid(True, which="major", linestyle=":", linewidth=0.7, color="black", alpha=0.45)
ax.grid(True, which="minor", linestyle=":", linewidth=0.4, color="black", alpha=0.2)

fig.savefig("figures/p-flambda.svg", transparent=True, bbox_inches="tight")
print("wrote figures/p-flambda.svg")
