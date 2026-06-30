
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

def run_apexplanet_certification_pipeline():
    # --------------------------------------------------------------------------
    # TASK 1: DATA INGESTION & DATA IMMERSION
    # --------------------------------------------------------------------------
    target_csv = "ecommerce_sales_34500.csv"
    
    if not os.path.exists(target_csv):
        print(f"[ERROR]: '{target_csv}' was not found in your workspace folder.")
        print("Please place this python script and the dataset together in the same directory.")
        return

    print("==================================================================")
    print("TASK 1: DATA INGESTION AND METADATA IMMERSION")
    print("==================================================================")
    
    # Load dataset into primary DataFrame structure
    df = pd.read_csv(target_csv)
    print(f"[SUCCESS]: Data loaded into memory framework.")
    print(f"Dataset Size Metrics: {df.shape[0]} Observations (Rows) | {df.shape[1]} Structural Attributes (Columns).\n")
    
    print("--- DATA DICTIONARY DETAILED PROFILE SCHEMATICS ---")
    print(df.info())
    print("\n--- VISUALIZING TOP SAMPLE RECORDS ---")
    print(df.head())
    print("\n")

    # --------------------------------------------------------------------------
    # TASK 2: DATA WRANGLING & QUALITY ASSESSMENT
    # --------------------------------------------------------------------------
    print("==================================================================")
    print("TASK 2: QUALITY CONTROLS AUDITING & WRANGLING INTERVENTIONS")
    print("==================================================================")
    
    # Audit for empty records / missing metrics
    null_registry = df.isnull().sum()
    print("Null Evaluation Scan Matrix:")
    print(null_registry)
    
    # Audit for duplicated rows across indices
    duplicate_registry = df.duplicated().sum()
    print(f"\nScanning for Duplicates... Result: {duplicate_registry} identical rows detected.")
    
    if duplicate_registry > 0:
        df = df.drop_duplicates()
        print("[ACTION]: Duplicate rows isolated and cleaned from the frame.")
    else:
        print("[ACTION]: Data Quality verified clean. No deduplication required.")
    print("\n")

    # --------------------------------------------------------------------------
    # TASK 3: EXPLORATORY DATA ANALYSIS (EDA) & CORE BUSINESS AGGREGATIONS
    # --------------------------------------------------------------------------
    print("==================================================================")
    print("TASK 3: EXPLORATORY DATA ANALYSIS & CORE KPIs")
    print("==================================================================")
    
    # Metric 1: Financial Topline Gross Sales Revenue Ingestion
    gross_revenue = df['total_amount'].sum()
    print(f"Metric 1: Gross Sales Revenue Invoiced: ${gross_revenue:,.2f}")
    
    # Metric 2: Gross Consolidated Operational Profit Margin
    net_profit = df['profit_margin'].sum()
    print(f"Metric 2: Cumulative Realized Profits: ${net_profit:,.2f}")
    
    # Metric 3: Category Rank Distribution based on Revenue Ingestion
    category_revenue_distribution = df.groupby('category')['total_amount'].sum().sort_values(ascending=False)
    print("\nMetric 3: Top Performing Product Categories (by Revenue):")
    print(category_revenue_distribution.apply(lambda value: f"${value:,.2f}"))
    
    # Metric 4: Geographical Volumetric Density across Markets
    regional_revenue_distribution = df.groupby('region')['total_amount'].sum().sort_values(ascending=False)
    print("\nMetric 4: Geographic Sales Volume Distribution across Markets:")
    print(regional_revenue_distribution.apply(lambda value: f"${value:,.2f}"))

    # Metric 5: Average Shipping Overhead Burden Across Category Channels
    shipping_burdens = df.groupby('category')['shipping_cost'].mean().sort_values(ascending=False)
    print("\nMetric 5: Mean Structural Logistics Cost Burden per Order:")
    print(shipping_burdens.apply(lambda value: f"${value:,.2f}"))
    print("\n")

    # --------------------------------------------------------------------------
    # TASK 4: PRESENTATION LAYER INTERACTIVE DASHBOARD ARCHITECTURE
    # --------------------------------------------------------------------------
    print("==================================================================")
    print("TASK 4: ASSEMBLING INTERACTIVE PERFORMANCE DASHBOARD PRESENTATION")
    print("==================================================================")
    
    # Configure plotting canvas theme structures
    sns.set_theme(style="whitegrid")
    
    # Build out a multi-pane matrix environment (2x2 Plotting Grid)
    fig, axes = plt.subplots(2, 2, figsize=(16, 11))
    fig.suptitle(f"ApexPlanet E-Commerce Executive Sales Dashboard\nGlobal Volume Revenue: ${gross_revenue:,.2f} | Net System Profit: ${net_profit:,.2f}", 
                 fontsize=20, fontweight='bold', color='#1a365d', y=0.97)

    # Subplot A: Total Sales Value By Core Category
    cat_chart_df = df.groupby('category')['total_amount'].sum().reset_index().sort_values(by='total_amount', ascending=False)
    sns.barplot(x='total_amount', y='category', data=cat_chart_df, ax=axes[0, 0], palette='Blues_r', hue='category', legend=False)
    axes[0, 0].set_title("Total Revenue Generation by Product Category", fontsize=12, fontweight='bold')
    axes[0, 0].set_xlabel("Invoiced Sales Volume ($)")
    axes[0, 0].set_ylabel("Product Category Classification")

    # Subplot B: Geographical Ingestion Breakdowns
    reg_chart_df = df.groupby('region')['total_amount'].sum().reset_index().sort_values(by='total_amount', ascending=False)
    sns.barplot(x='region', y='total_amount', data=reg_chart_df, ax=axes[0, 1], palette='Greens_r', hue='region', legend=False)
    axes[0, 1].set_title("Geographic Purchase Ingestion Density by Region", fontsize=12, fontweight='bold')
    axes[0, 1].set_xlabel("Operational Regions")
    axes[0, 1].set_ylabel("Invoiced Sales Volume ($)")

    # Subplot C: System Payment Method Instruments Share Allocation
    payment_allocation = df['payment_method'].value_counts().reset_index()
    axes[1, 0].pie(payment_allocation['count'], labels=payment_allocation['payment_method'], autopct='%1.1f%%', 
                   startangle=140, colors=['#3182ce', '#319795', '#dd6b20', '#e53e3e', '#805ad5', '#718096'])
    axes[1, 0].set_title("Channel Distribution of Utilized Payment Instruments", fontsize=12, fontweight='bold')

    # Subplot D: Net Operational Profits Across Core Categories
    profit_chart_df = df.groupby('category')['profit_margin'].sum().reset_index().sort_values(by='profit_margin', ascending=False)
    sns.barplot(x='profit_margin', y='category', data=profit_chart_df, ax=axes[1, 1], palette='Purples_r', hue='category', legend=False)
    axes[1, 1].set_title("Accumulated Net Realized Profit Margins by Category", fontsize=12, fontweight='bold')
    axes[1, 1].set_xlabel("Net Operational Income Profit ($)")
    axes[1, 1].set_ylabel("Product Category Classification")

    # Final Adjustment constraints to ensure clean visibility
    plt.tight_layout(rect=[0, 0, 1, 0.94])
    
    # Save the output visualization image to disk for GitHub submission
    output_filename = "apexplanet_executive_dashboard.png"
    plt.savefig(output_filename, dpi=300)
    print(f"[EXPORT SUCCESS]: Visual Dashboard saved to directory workspace file as: '{output_filename}'")
    
    print("\n>>> Spawning independent Interactive User Application Display...")
    print("==================================================================")
    
    # Launch interactive GUI viewport application window
    plt.show()

if __name__ == "__main__":
    run_apexplanet_certification_pipeline()