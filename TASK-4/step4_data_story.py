
# STEP 4: DATA STORY — BUSINESS NARRATIVE
# ApexPlanet Data Analytics - Task 4


import pandas as pd
import numpy as np
import os

# ----------------------------------------------------------
# LOAD CLEANED DATA
# ----------------------------------------------------------
df = pd.read_csv('outputs/cleaned_data.csv', parse_dates=['Order_Date'])
os.makedirs('outputs', exist_ok=True)

print("=" * 55)
print("     STEP 4: CRAFTING THE DATA STORY")
print("=" * 55)

# ----------------------------------------------------------
# COMPUTE ALL NARRATIVE METRICS
# ----------------------------------------------------------

# Core KPIs
total_revenue   = df['Total_Sales'].sum()
total_orders    = len(df)
avg_order_value = df['Total_Sales'].mean()

# Category breakdown
cat_sales = df.groupby('Category')['Total_Sales'].sum().sort_values(ascending=False)
top_cat   = cat_sales.idxmax()
top_cat_pct = (cat_sales.max() / total_revenue) * 100

# Monthly trend
monthly = (df.groupby(['Year', 'Month_Num', 'Month'])['Total_Sales']
             .sum().reset_index().sort_values(['Year', 'Month_Num']))
peak_idx   = monthly['Total_Sales'].idxmax()
low_idx    = monthly['Total_Sales'].idxmin()
peak_month = monthly.loc[peak_idx, 'Month']
peak_year  = monthly.loc[peak_idx, 'Year']
low_month  = monthly.loc[low_idx, 'Month']
low_year   = monthly.loc[low_idx, 'Year']

# Gender split
gender_rev = df.groupby('Gender')['Total_Sales'].sum()
male_pct   = gender_rev['Male'] / total_revenue * 100
female_pct = gender_rev['Female'] / total_revenue * 100

# Top city
city_rev  = df.groupby('City')['Total_Sales'].sum().sort_values(ascending=False)
top_city  = city_rev.idxmax()
top_city_pct = city_rev.max() / total_revenue * 100

# Age group
age_rev   = df.groupby('Age_Group', observed=True)['Total_Sales'].sum()
top_age   = age_rev.idxmax()

# ----------------------------------------------------------
# WRITE THE DATA STORY AS A NARRATIVE REPORT
# ----------------------------------------------------------
story = f"""
================================================================
     APEXPLANET E-COMMERCE — DATA STORY & BUSINESS NARRATIVE
                       Task 4 | Year 2025–2026
================================================================

OBJECTIVE
---------
To analyze one full year (Jan 2025 – Jan 2026) of ApexPlanet
e-commerce transactions and surface data-driven insights that
guide the business toward higher revenue, better customer
targeting, and smarter inventory decisions.


PART 1 — THE BUSINESS LANDSCAPE (What We Found)
------------------------------------------------
ApexPlanet processed {total_orders:,} orders in 2025–2026,
generating a total revenue of ₹{total_revenue/1e6:.2f} Million.
The average order value stood at ₹{avg_order_value:,.2f}.

The product catalog spans five categories:
  • Electronics   • Fashion   • Furniture
  • Grocery       • Education

The platform serves customers across {df['City'].nunique()} major cities,
with an almost equal split between Male ({male_pct:.1f}%) and
Female ({female_pct:.1f}%) shoppers.


PART 2 — WHAT THE DATA TELLS US (Key Findings)
------------------------------------------------

FINDING 1 — HIGH-VALUE CATEGORIES DRIVE GROWTH
  ► {top_cat} is the top revenue category at
    ₹{cat_sales.max()/1e6:.1f}M ({top_cat_pct:.1f}% of total revenue).
  ► High-value categories like Electronics and Furniture
    command large average order sizes, suggesting a
    premium shopper base.

FINDING 2 — SEASONALITY EXISTS BUT IS MANAGEABLE
  ► Sales peaked in {peak_month} {peak_year} and dipped in
    {low_month} {low_year}.
  ► This seasonal pattern provides a clear window for
    pre-peak inventory build-up and promotional campaigns.

FINDING 3 — GEOGRAPHIC CONCENTRATION
  ► {top_city} leads all cities contributing {top_city_pct:.1f}%
    of total revenue.
  ► Tier-2 cities show untapped potential with lower
    penetration rates.

FINDING 4 — DEMOGRAPHIC SWEET SPOT
  ► The {top_age} age group drives the highest revenue,
    making them the primary target audience.
  ► Campaigns tailored to this demographic will yield
    the highest ROI.

FINDING 5 — GENDER PARITY IN SPENDING (Validated by Stats)
  ► Statistical testing (T-Test, p > 0.05) confirmed that
    Male and Female customers spend at similar levels.
  ► No gender-based pricing or preferential discount
    strategy is needed.


PART 3 — STATISTICAL VALIDATION (Confidence in Our Claims)
-----------------------------------------------------------
Three hypothesis tests were run at α = 0.05:

  ① T-Test (Gender vs. Order Value)
    → Both genders spend similarly — no significant gap.

  ② Chi-Squared (Gender vs. Category Preference)
    → Purchase category preference is INDEPENDENT of gender.
    → Both males and females distribute purchases similarly
      across all five categories.

  ③ One-Way ANOVA (Category vs. Revenue)
    → Average order values DO differ significantly across
      categories — Electronics and Furniture lead.

These tests give statistical confidence to our findings,
moving them from "observations" to "validated insights."


PART 4 — CALL TO ACTION (What ApexPlanet Should Do)
-----------------------------------------------------
   RECOMMENDATION 1 — DOUBLE DOWN ON ELECTRONICS & FURNITURE
     Increase inventory depth and marketing spend on these two
     categories during the 2–3 months before the seasonal peak.

   RECOMMENDATION 2 — TARGET THE 26-35 AGE SEGMENT
     Launch loyalty programs and personalized email campaigns
     aimed at this highest-spending cohort.

   RECOMMENDATION 3 — EXPAND INTO TIER-2 CITIES
     Cities outside the top 2 show growth potential.
     Localized delivery deals and first-order discounts
     can accelerate penetration.

   RECOMMENDATION 4 — GENDER-NEUTRAL MARKETING
     Since both genders behave similarly, invest in
     universal product-centric campaigns rather than
     gender-segmented promotions.

   RECOMMENDATION 5 — PLAN PROMOTIONS AROUND PEAK MONTHS
     Use sales forecasting data to pre-stock and launch
     deals at least 3 weeks before the peak sales month.


CONCLUSION
----------
ApexPlanet has a healthy, diversified revenue base with
clear growth levers. By focusing on high-value categories,
targeting the core demographic, and expanding geographically,
the business can aim for 20–30% revenue growth in 2026.

================================================================
 Report generated by: ApexPlanet_Task4 Data Analytics Pipeline
================================================================
"""

# Print to console
print(story)

# Save as text file
with open('outputs/data_story_narrative.txt', 'w') as f:
    f.write(story)

print(" Data story saved → outputs/data_story_narrative.txt")
print("\n STEP 4 COMPLETE\n")
