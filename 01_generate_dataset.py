import pandas as pd
import numpy as np

np.random.seed(42)

CHANNELS = {
    "Google Ads":      dict(impr=(5000, 15000), ctr=(0.030, 0.060), cpc=(14, 24), lead=(0.20, 0.30), qual=(0.50, 0.65), call=(0.70, 0.85), close=(0.25, 0.35), rev=(5000, 8000)),
    "Facebook Ads":    dict(impr=(8000, 20000), ctr=(0.015, 0.030), cpc=(8, 15),   lead=(0.15, 0.25), qual=(0.40, 0.55), call=(0.65, 0.80), close=(0.20, 0.30), rev=(4000, 6000)),
    "Instagram Ads":   dict(impr=(7000, 18000), ctr=(0.012, 0.028), cpc=(7, 14),   lead=(0.13, 0.22), qual=(0.38, 0.52), call=(0.60, 0.78), close=(0.18, 0.28), rev=(3800, 5800)),
    "LinkedIn Ads":    dict(impr=(2000, 6000),  ctr=(0.020, 0.040), cpc=(30, 50),  lead=(0.18, 0.28), qual=(0.60, 0.75), call=(0.72, 0.85), close=(0.30, 0.40), rev=(10000, 15000)),
    "Email Marketing": dict(impr=(3000, 8000),  ctr=(0.080, 0.150), cpc=(2, 5),    lead=(0.30, 0.40), qual=(0.55, 0.65), call=(0.75, 0.85), close=(0.30, 0.40), rev=(5000, 7000)),
    "Organic Search":  dict(impr=(6000, 15000), ctr=(0.040, 0.080), cpc=(1, 3),    lead=(0.20, 0.28), qual=(0.50, 0.60), call=(0.68, 0.80), close=(0.35, 0.45), rev=(6000, 9000)),
    "Referral":        dict(impr=(1000, 4000),  ctr=(0.100, 0.200), cpc=(1, 3),    lead=(0.40, 0.50), qual=(0.65, 0.75), call=(0.78, 0.88), close=(0.40, 0.50), rev=(7000, 10000)),
    "YouTube Ads":     dict(impr=(5000, 12000), ctr=(0.010, 0.030), cpc=(10, 20),  lead=(0.15, 0.22), qual=(0.35, 0.50), call=(0.60, 0.75), close=(0.15, 0.25), rev=(4000, 6000)),
}

N_DAYS = 125
dates = pd.date_range("2025-01-01", periods=N_DAYS, freq="D")

rows = []
for d in dates:
    weekday_factor = 0.85 if d.weekday() >= 5 else 1.0
    for ch, p in CHANNELS.items():
        impressions = int(np.random.uniform(*p["impr"]) * weekday_factor)
        ctr = np.random.uniform(*p["ctr"])
        clicks = max(1, int(impressions * ctr))

        lead_rate = np.random.uniform(*p["lead"])
        leads = max(0, int(clicks * lead_rate))

        qual_rate = np.random.uniform(*p["qual"])
        qualified_leads = max(0, int(leads * qual_rate))

        call_rate = np.random.uniform(*p["call"])
        sales_calls = max(0, int(qualified_leads * call_rate))

        close_rate = np.random.uniform(*p["close"])
        customers = max(0, int(sales_calls * close_rate))

        cpc = np.random.uniform(*p["cpc"])
        ad_spend = round(clicks * cpc, 2)

        rev_per_cust = np.random.uniform(*p["rev"])
        revenue = round(customers * rev_per_cust, 2)

        rows.append([d.date(), ch, impressions, clicks, leads, qualified_leads, sales_calls, customers, revenue, ad_spend])

df = pd.DataFrame(rows, columns=["Date", "Marketing Channel", "Impressions", "Clicks", "Leads",
                                  "Qualified Leads", "Sales Calls", "Customers", "Revenue", "Ad Spend"])

df = df.sort_values(["Date", "Marketing Channel"]).reset_index(drop=True)
assert len(df) == 1000

df.to_csv("/home/claude/funnel_project/data/marketing_funnel_data.csv", index=False)
df.to_excel("/home/claude/funnel_project/data/marketing_funnel_data_raw.xlsx", index=False)
print(df.shape)
print(df.head(10).to_string())
print(df["Marketing Channel"].value_counts())
