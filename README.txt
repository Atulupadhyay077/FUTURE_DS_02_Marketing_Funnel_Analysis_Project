MARKETING FUNNEL & CONVERSION PERFORMANCE ANALYSIS
=====================================================
Internship Project | Prepared by: Abhay (BCA Student)

FOLDER STRUCTURE
----------------
1_Dataset/
    marketing_funnel_data.csv / .xlsx   -> Raw dataset (1000 rows, 8 channels x 125 days)
    channel_summary.csv                 -> Channel-wise performance metrics
    dropoff_summary.csv                 -> Stage-by-stage drop-off analysis
    monthly_summary.csv                 -> Month-wise revenue and spend totals

2_Python_Scripts/
    01_generate_dataset.py   -> Generates the 1000-row synthetic dataset
    02_funnel_analysis.py    -> Calculates CTR, conversion rates, ROAS, drop-off, best/worst channel
    03_generate_charts.py    -> Builds all charts used in the dashboard and report

    Run them in this order with Python 3:
        python 01_generate_dataset.py
        python 02_funnel_analysis.py
        python 03_generate_charts.py

3_Charts/
    8 PNG charts: funnel overview, drop-off rates, channel conversion, ROAS,
    CTR vs close rate, monthly trend, revenue share, and KPI summary cards.

4_Excel_Dashboard/
    Marketing_Funnel_Dashboard.xlsx
    -> Raw Data, Channel Summary, Funnel Drop-off, and a Dashboard sheet
       with KPI cards and native Excel charts. All figures use formulas,
       so the dashboard updates automatically if you edit the Raw Data sheet.

5_Final_Report/
    Marketing_Funnel_Analysis_Report.docx
    -> Submission-ready Word report: objective, methodology, funnel analysis,
       drop-off analysis, channel performance, key findings, and recommendations.

HOW THE DATA WAS BUILT
-----------------------
The dataset is synthetic (created in Python with NumPy/Pandas) but designed to
behave like a real-world marketing funnel: each of the 8 channels has its own
realistic ranges for impressions, CTR, cost-per-click, and conversion rates at
every funnel stage (Impressions -> Clicks -> Leads -> Qualified Leads ->
Sales Calls -> Customers), so the analysis tells a believable business story.

KEY HEADLINE NUMBERS
---------------------
Overall Funnel Conversion : 0.19% (Impressions to Customers)
Overall ROAS              : 36.23x
Best Channel              : Referral
Highest ROI Channel       : Referral (491.89x ROAS)
Worst Channel             : YouTube Ads
Biggest Drop-off (volume) : Impressions -> Clicks (95.67%)
Biggest Controllable Drop : Sales Calls -> Customers (64.45%)
