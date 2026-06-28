import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.edgecolor"] = "#444444"
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.25

COLOR_PRIMARY = "#1F4E79"
COLOR_ACCENT = "#ED7D31"
COLOR_GOOD = "#2E8B57"
COLOR_BAD = "#C0392B"
PALETTE = ["#1F4E79", "#2E86AB", "#ED7D31", "#F2C14E", "#2E8B57", "#8E44AD", "#C0392B", "#5DADE2"]

OUT = "/home/claude/funnel_project/charts"

df = pd.read_csv("/home/claude/funnel_project/data/marketing_funnel_data.csv", parse_dates=["Date"])
channel = pd.read_csv("/home/claude/funnel_project/data/channel_summary.csv")
dropoff = pd.read_csv("/home/claude/funnel_project/data/dropoff_summary.csv")
monthly = pd.read_csv("/home/claude/funnel_project/data/monthly_summary.csv")

stage_cols = ["Impressions", "Clicks", "Leads", "Qualified Leads", "Sales Calls", "Customers"]
totals = df[stage_cols].sum()

fig, ax = plt.subplots(figsize=(9.5, 6))
stages = stage_cols
values = [totals[s] for s in stages]
y_pos = np.arange(len(stages))[::-1]
bars = ax.barh(y_pos, values, height=0.55, color=PALETTE[:len(stages)], edgecolor="white")
ax.set_xscale("log")
ax.set_xlim(1, max(values) * 3)
for i, v in enumerate(values):
    ax.text(v * 1.15, y_pos[i], f"{v:,.0f}", va="center", fontsize=10.5, fontweight="bold", color="#222222")
ax.set_yticks(y_pos)
ax.set_yticklabels(stages, fontsize=11, fontweight="bold")
ax.set_xlabel("Volume (log scale)")
ax.spines[["top", "right"]].set_visible(False)
ax.set_title("Marketing Funnel: Impressions \u2192 Customers", fontsize=15, fontweight="bold", color=COLOR_PRIMARY, pad=15)
plt.tight_layout()
plt.savefig(f"{OUT}/01_funnel_overview.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(9, 5.5))
bars = ax.bar(dropoff["Stage"], dropoff["Drop-off Rate (%)"], color=[COLOR_BAD if v == dropoff["Drop-off Rate (%)"].max() else COLOR_PRIMARY for v in dropoff["Drop-off Rate (%)"]])
for b, v in zip(bars, dropoff["Drop-off Rate (%)"]):
    ax.text(b.get_x() + b.get_width() / 2, v + 1.5, f"{v:.1f}%", ha="center", fontsize=10, fontweight="bold")
ax.set_ylabel("Drop-off Rate (%)")
ax.set_title("Funnel Drop-off Rate by Stage", fontsize=14, fontweight="bold", color=COLOR_PRIMARY)
plt.xticks(rotation=20, ha="right", fontsize=9)
ax.set_ylim(0, 105)
plt.tight_layout()
plt.savefig(f"{OUT}/02_dropoff_by_stage.png", dpi=160)
plt.close()

ch_sorted = channel.sort_values("Overall Funnel Conversion (%)", ascending=True)
fig, ax = plt.subplots(figsize=(9, 5.5))
colors = [COLOR_GOOD if i == len(ch_sorted) - 1 else (COLOR_BAD if i == 0 else COLOR_PRIMARY) for i in range(len(ch_sorted))]
bars = ax.barh(ch_sorted["Marketing Channel"], ch_sorted["Overall Funnel Conversion (%)"], color=colors)
for b, v in zip(bars, ch_sorted["Overall Funnel Conversion (%)"]):
    ax.text(v + 0.02, b.get_y() + b.get_height() / 2, f"{v:.2f}%", va="center", fontsize=9, fontweight="bold")
ax.set_xlabel("Overall Funnel Conversion Rate (%)")
ax.set_title("Overall Funnel Conversion Rate by Channel\n(Impressions \u2192 Customer)", fontsize=13, fontweight="bold", color=COLOR_PRIMARY)
plt.tight_layout()
plt.savefig(f"{OUT}/03_channel_conversion.png", dpi=160)
plt.close()

ch_roas = channel.sort_values("ROAS (x)", ascending=True)
fig, ax = plt.subplots(figsize=(9, 5.5))
colors = [COLOR_GOOD if i == len(ch_roas) - 1 else (COLOR_BAD if i == 0 else COLOR_ACCENT) for i in range(len(ch_roas))]
bars = ax.barh(ch_roas["Marketing Channel"], ch_roas["ROAS (x)"], color=colors)
for b, v in zip(bars, ch_roas["ROAS (x)"]):
    ax.text(v + max(ch_roas["ROAS (x)"]) * 0.01, b.get_y() + b.get_height() / 2, f"{v:.1f}x", va="center", fontsize=9, fontweight="bold")
ax.set_xlabel("ROAS (Revenue / Ad Spend)")
ax.set_title("Return on Ad Spend (ROAS) by Channel", fontsize=14, fontweight="bold", color=COLOR_PRIMARY)
plt.tight_layout()
plt.savefig(f"{OUT}/04_channel_roas.png", dpi=160)
plt.close()

fig, ax = plt.subplots(figsize=(10, 5.5))
x = np.arange(len(channel))
w = 0.35
ax.bar(x - w/2, channel["CTR (%)"], width=w, label="CTR (%)", color=COLOR_PRIMARY)
ax.bar(x + w/2, channel["Close Rate (%)"], width=w, label="Close Rate (%)", color=COLOR_ACCENT)
ax.set_xticks(x)
ax.set_xticklabels(channel["Marketing Channel"], rotation=20, ha="right", fontsize=9)
ax.set_ylabel("Rate (%)")
ax.set_title("CTR vs Close Rate by Channel", fontsize=14, fontweight="bold", color=COLOR_PRIMARY)
ax.legend()
plt.tight_layout()
plt.savefig(f"{OUT}/05_ctr_vs_close.png", dpi=160)
plt.close()

fig, ax1 = plt.subplots(figsize=(9, 5.5))
ax1.bar(monthly["Month"], monthly["Ad Spend"], color=COLOR_ACCENT, alpha=0.7, label="Ad Spend")
ax1.set_ylabel("Ad Spend (\u20b9)", color=COLOR_ACCENT)
ax2 = ax1.twinx()
ax2.plot(monthly["Month"], monthly["Revenue"], color=COLOR_GOOD, marker="o", linewidth=2.5, label="Revenue")
ax2.set_ylim(0, monthly["Revenue"].max() * 1.15)
ax2.set_ylabel("Revenue (\u20b9)", color=COLOR_GOOD)
ax1.set_title("Monthly Revenue vs Ad Spend Trend", fontsize=14, fontweight="bold", color=COLOR_PRIMARY)
fig.legend(loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2)
plt.tight_layout()
plt.savefig(f"{OUT}/06_monthly_trend.png", dpi=160, bbox_inches="tight")
plt.close()

fig, ax = plt.subplots(figsize=(8.5, 7.2))
ch_rev = channel.sort_values("Revenue", ascending=False)
pct_of_total = ch_rev["Revenue"] / ch_rev["Revenue"].sum() * 100

def autopct_fn(pct):
    return f"{pct:.1f}%" if pct >= 3 else ""

wedges, _, _ = ax.pie(ch_rev["Revenue"], autopct=autopct_fn, colors=PALETTE,
                      startangle=90, textprops={"fontsize": 10, "fontweight": "bold", "color": "white"},
                      pctdistance=0.75)
labels = [f"{ch} ({p:.1f}%)" for ch, p in zip(ch_rev["Marketing Channel"], pct_of_total)]
ax.legend(wedges, labels, title="Channel (Revenue Share)", loc="center left", bbox_to_anchor=(1.0, 0.5), fontsize=9.5)
ax.set_title("Revenue Share by Marketing Channel", fontsize=14, fontweight="bold", color=COLOR_PRIMARY)
plt.tight_layout()
plt.savefig(f"{OUT}/07_revenue_share.png", dpi=160, bbox_inches="tight")
plt.close()

import json
with open("/home/claude/funnel_project/data/overall_summary.json") as f:
    summ = json.load(f)

fig, ax = plt.subplots(figsize=(11, 3.2))
ax.axis("off")
kpis = [
    ("Total Impressions", f"{summ['Total Impressions']:,.0f}"),
    ("Total Customers", f"{summ['Total Customers']:,.0f}"),
    ("Overall Conversion", f"{summ['Overall Funnel Conversion (%)']:.2f}%"),
    ("Total Revenue", f"\u20b9{summ['Total Revenue']:,.0f}"),
    ("ROAS", f"{summ['ROAS (x)']:.1f}x"),
]
n = len(kpis)
for i, (label, value) in enumerate(kpis):
    x0 = i / n
    ax.add_patch(plt.Rectangle((x0 + 0.01, 0.05), 1/n - 0.02, 0.9, transform=ax.transAxes,
                                facecolor=PALETTE[i % len(PALETTE)], edgecolor="none"))
    ax.text(x0 + (1/n)/2, 0.62, value, transform=ax.transAxes, ha="center", va="center",
            fontsize=18, fontweight="bold", color="white")
    ax.text(x0 + (1/n)/2, 0.25, label, transform=ax.transAxes, ha="center", va="center",
            fontsize=10.5, color="white")
plt.tight_layout()
plt.savefig(f"{OUT}/08_kpi_cards.png", dpi=160)
plt.close()

print("Charts created:")
import os
for f in sorted(os.listdir(OUT)):
    print(" -", f)
