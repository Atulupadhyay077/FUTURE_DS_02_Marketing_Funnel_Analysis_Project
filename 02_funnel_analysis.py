import pandas as pd
import numpy as np
import json

df = pd.read_csv("/home/claude/funnel_project/data/marketing_funnel_data.csv", parse_dates=["Date"])

stage_cols = ["Impressions", "Clicks", "Leads", "Qualified Leads", "Sales Calls", "Customers"]
totals = df[stage_cols + ["Revenue", "Ad Spend"]].sum()

overall = {
    "Total Impressions": int(totals["Impressions"]),
    "Total Clicks": int(totals["Clicks"]),
    "Total Leads": int(totals["Leads"]),
    "Total Qualified Leads": int(totals["Qualified Leads"]),
    "Total Sales Calls": int(totals["Sales Calls"]),
    "Total Customers": int(totals["Customers"]),
    "Total Revenue": round(float(totals["Revenue"]), 2),
    "Total Ad Spend": round(float(totals["Ad Spend"]), 2),
}

overall["CTR (%)"] = round(totals["Clicks"] / totals["Impressions"] * 100, 2)
overall["Lead Conversion Rate (%)"] = round(totals["Leads"] / totals["Clicks"] * 100, 2)
overall["Qualification Rate (%)"] = round(totals["Qualified Leads"] / totals["Leads"] * 100, 2)
overall["Sales Call Rate (%)"] = round(totals["Sales Calls"] / totals["Qualified Leads"] * 100, 2)
overall["Close Rate (%)"] = round(totals["Customers"] / totals["Sales Calls"] * 100, 2)
overall["Lead to Customer Conversion (%)"] = round(totals["Customers"] / totals["Leads"] * 100, 2)
overall["Overall Funnel Conversion (%)"] = round(totals["Customers"] / totals["Impressions"] * 100, 2)
overall["ROAS (x)"] = round(totals["Revenue"] / totals["Ad Spend"], 2)

stage_pairs = [
    ("Impressions", "Clicks"),
    ("Clicks", "Leads"),
    ("Leads", "Qualified Leads"),
    ("Qualified Leads", "Sales Calls"),
    ("Sales Calls", "Customers"),
]
dropoff_rows = []
for a, b in stage_pairs:
    start, end = totals[a], totals[b]
    dropoff_pct = round((1 - end / start) * 100, 2)
    dropoff_rows.append({
        "Stage": f"{a} -> {b}",
        "Entered": int(start),
        "Passed Through": int(end),
        "Lost": int(start - end),
        "Drop-off Rate (%)": dropoff_pct,
    })
dropoff_df = pd.DataFrame(dropoff_rows)
biggest_dropoff = dropoff_df.loc[dropoff_df["Drop-off Rate (%)"].idxmax()]

channel = df.groupby("Marketing Channel")[stage_cols + ["Revenue", "Ad Spend"]].sum().reset_index()
channel["CTR (%)"] = round(channel["Clicks"] / channel["Impressions"] * 100, 2)
channel["Lead Conversion Rate (%)"] = round(channel["Leads"] / channel["Clicks"] * 100, 2)
channel["Qualification Rate (%)"] = round(channel["Qualified Leads"] / channel["Leads"] * 100, 2)
channel["Close Rate (%)"] = round(channel["Customers"] / channel["Sales Calls"] * 100, 2)
channel["Overall Funnel Conversion (%)"] = round(channel["Customers"] / channel["Impressions"] * 100, 2)
channel["ROAS (x)"] = round(channel["Revenue"] / channel["Ad Spend"], 2)
channel["Cost per Customer"] = round(channel["Ad Spend"] / channel["Customers"].replace(0, np.nan), 2)
channel = channel.sort_values("Overall Funnel Conversion (%)", ascending=False).reset_index(drop=True)

best_channel = channel.iloc[0]
worst_channel = channel.iloc[-1]
highest_roas_channel = channel.sort_values("ROAS (x)", ascending=False).iloc[0]

monthly = df.copy()
monthly["Month"] = monthly["Date"].dt.to_period("M").astype(str)
day_counts = monthly.groupby("Month")["Date"].nunique()
full_months = day_counts[day_counts >= 25].index
monthly_summary = monthly[monthly["Month"].isin(full_months)].groupby("Month")[stage_cols + ["Revenue", "Ad Spend"]].sum().reset_index()
monthly_summary["ROAS (x)"] = round(monthly_summary["Revenue"] / monthly_summary["Ad Spend"], 2)

channel.to_csv("/home/claude/funnel_project/data/channel_summary.csv", index=False)
dropoff_df.to_csv("/home/claude/funnel_project/data/dropoff_summary.csv", index=False)
monthly_summary.to_csv("/home/claude/funnel_project/data/monthly_summary.csv", index=False)

with open("/home/claude/funnel_project/data/overall_summary.json", "w") as f:
    json.dump({k: (float(v) if isinstance(v, (np.floating, np.integer)) else v) for k, v in overall.items()}, f, indent=2)

print("OVERALL FUNNEL METRICS")
for k, v in overall.items():
    print(f"  {k}: {v}")

print("\nDROP-OFF BY STAGE")
print(dropoff_df.to_string(index=False))
print(f"\nBIGGEST DROP-OFF STAGE: {biggest_dropoff['Stage']} ({biggest_dropoff['Drop-off Rate (%)']}%)")

print("\nCHANNEL PERFORMANCE (sorted by Overall Funnel Conversion %)")
print(channel.to_string(index=False))

print(f"\nBEST CHANNEL (funnel conversion): {best_channel['Marketing Channel']} - {best_channel['Overall Funnel Conversion (%)']}%")
print(f"WORST CHANNEL (funnel conversion): {worst_channel['Marketing Channel']} - {worst_channel['Overall Funnel Conversion (%)']}%")
print(f"HIGHEST ROI CHANNEL (ROAS): {highest_roas_channel['Marketing Channel']} - {highest_roas_channel['ROAS (x)']}x")
