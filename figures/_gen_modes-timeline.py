#!/usr/bin/env python3
"""Generate figures/modes-timeline.svg (Figure 9.1).

A horizontal timeline, 1900-2025, marking the arrival of key amateur-radio
technologies by decade. Single color (black), transparent background;
post-processed to currentColor so it themes with the page.

Dates are taken from accuracy-canon.md's Pinned Timeline / Core Technology
by Era sections.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# (year, label, sublabel, side) -- side: 1 = above axis, -1 = below axis
EVENTS = [
    (1901, "Spark", "damped-wave CW", 1),
    (1919, "CW / Tubes", "triode, regeneration", -1),
    (1920, "Superhet", "Armstrong patent", 1),
    (1947, "Transistor", "Bell Labs point-contact", -1),
    (1948, "SSB", "phasing method", 1),
    (1961, "Satellites", "OSCAR 1", -1),
    (1970, "FM / Repeaters", "2 m FM boom", 1),
    (1981, "Packet", "TAPR / AX.25", -1),
    (1998, "PSK31", "G3PLX", 1),
    (2003, "SDR", "FlexRadio SDR-1000", -1),
    (2017, "FT8", "WSJT-X", 1),
]

YEAR_MIN, YEAR_MAX = 1900, 2025

# Small manual x-nudges (display position only) so markers that fall within
# a year or two of each other don't visually collide. The printed year text
# next to each marker always shows the true, un-nudged date.
DISPLAY_NUDGE = {
    1919: -1.3,
    1920: 1.3,
    1947: -1.3,
    1948: 1.3,
}

fig, ax = plt.subplots(figsize=(12.5, 5.6), dpi=200)

# --- main timeline spine -------------------------------------------------
axis_y = 0.0
ax.add_line(Line2D([YEAR_MIN, YEAR_MAX], [axis_y, axis_y],
                    color="black", linewidth=2.2, solid_capstyle="round",
                    zorder=2))

# arrowhead at the right end (time moving forward)
ax.annotate("", xy=(YEAR_MAX + 3, axis_y), xytext=(YEAR_MAX, axis_y),
            arrowprops=dict(arrowstyle="-|>", color="black", linewidth=2.2,
                             mutation_scale=16), zorder=2)

# --- decade ticks along the spine ----------------------------------------
event_years = {yr for yr, *_ in EVENTS}
decades = list(range(1900, 2030, 10))
for dec in decades:
    ax.plot([dec, dec], [axis_y - 0.045, axis_y + 0.045],
             color="black", linewidth=1.0, zorder=2)
    # Skip the printed decade number if an event marker already labels a
    # year within 2 of it -- avoids stacking two near-duplicate numerals.
    if not any(abs(dec - ey) <= 2 for ey in event_years):
        ax.text(dec, axis_y - 0.14, f"{dec}", ha="center", va="top",
                 fontsize=8.5, color="black", family="monospace")

# --- event markers, stems, and labels ------------------------------------
STEM_H = 0.62
LABEL_GAP = 0.09

for year, label, sub, side in EVENTS:
    dx = DISPLAY_NUDGE.get(year, 0.0)
    xpos = year + dx

    # marker dot on the spine (display position, may be nudged)
    ax.plot([xpos], [axis_y], marker="o", linestyle="None", markersize=7,
             markerfacecolor="white", markeredgecolor="black",
             markeredgewidth=1.7, zorder=4)

    # true year, printed right under/over the marker
    ax.text(xpos, axis_y + side * 0.06, str(year), ha="center",
             va="bottom" if side > 0 else "top",
             fontsize=7.8, color="black")

    # stem from spine to label block
    y_end = side * STEM_H
    ax.add_line(Line2D([xpos, xpos], [axis_y + side * 0.17, y_end],
                        color="black", linewidth=1.1, zorder=3))

    ytext = y_end + side * LABEL_GAP
    va = "bottom" if side > 0 else "top"

    ax.text(xpos, ytext, label, ha="center", va=va,
             fontsize=11.5, fontweight="bold", color="black")
    sub_y = ytext + side * 0.155
    ax.text(xpos, sub_y, sub, ha="center", va=va,
             fontsize=8.5, color="black", style="italic")

# --- title -----------------------------------------------------------------
ax.text((YEAR_MIN + YEAR_MAX) / 2, 1.35,
        "A Century of the Art: Key Amateur Radio Technologies by Decade",
        ha="center", va="bottom", fontsize=13, fontweight="bold",
        color="black")

ax.set_xlim(YEAR_MIN - 8, YEAR_MAX + 12)
ax.set_ylim(-1.25, 1.55)
ax.axis("off")

fig.tight_layout()
fig.savefig("/home/kasm-user/200-meters-and-down/figures/modes-timeline.svg",
            transparent=True, bbox_inches="tight")
print("saved modes-timeline.svg")
