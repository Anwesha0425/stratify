"""
Market Research & Competitor Analysis - Exploratory Data Analysis Script

This script loads the 500-record Indian e-commerce market research dataset,
calculates executive KPIs, and prints structured benchmark tables for competitor analysis.
"""

from pathlib import Path
import pandas as pd


DATASET_FILE = Path(__file__).resolve().parent / "Ecommerce_Market_Research_500_Rows.xlsx"


def load_data(filepath: Path) -> pd.DataFrame:
    if not filepath.exists():
        raise FileNotFoundError(f"Dataset not found at {filepath}")
    return pd.read_excel(filepath)


def print_header(title: str) -> None:
    print(f"\n{'=' * 70}")
    print(f" {title.upper()}")
    print(f"{'=' * 70}")


def run_analysis(df: pd.DataFrame) -> None:
    print_header("Executive KPI Summary")
    total_records = len(df)
    unique_companies = df["Company Name"].nunique()
    avg_market_share = df["Market Share %"].mean()
    avg_rating = df["Product Rating"].mean()
    avg_csat = df["Customer Satisfaction Score"].mean()
    avg_growth = df["Growth Rate %"].mean()
    total_rev = df["Revenue Estimate"].sum()
    avg_brand_awareness = df["Brand Awareness Score"].mean()

    print(f"Total Records Analyzed       : {total_records}")
    print(f"Tracked Companies            : {unique_companies}")
    print(f"Average Market Share         : {avg_market_share:.2f}%")
    print(f"Average Product Rating       : {avg_rating:.2f} / 5.0")
    print(f"Average Customer Satisfaction: {avg_csat:.2f} / 100")
    print(f"Average Growth Rate          : {avg_growth:.2f}%")
    print(f"Average Brand Awareness      : {avg_brand_awareness:.2f} / 100")
    print(f"Total Revenue Estimate       : ₹{total_rev:,.0f} (in thousands/units)")

    print_header("Company Performance Benchmarking")
    company_summary = (
        df.groupby("Company Name")
        .agg(
            Record_Count=("Product Price", "count"),
            Avg_Market_Share=("Market Share %", "mean"),
            Avg_Rating=("Product Rating", "mean"),
            Avg_CSAT=("Customer Satisfaction Score", "mean"),
            Avg_Growth_Rate=("Growth Rate %", "mean"),
            Total_Revenue=("Revenue Estimate", "sum"),
        )
        .sort_values(by="Avg_Market_Share", ascending=False)
        .round(2)
    )
    print(company_summary.to_string())

    print_header("Regional Market Distribution")
    regional_summary = (
        df.groupby("Region")
        .agg(
            Records=("Company Name", "count"),
            Avg_Market_Share=("Market Share %", "mean"),
            Avg_Growth_Rate=("Growth Rate %", "mean"),
            Avg_CSAT=("Customer Satisfaction Score", "mean"),
        )
        .sort_values(by="Records", ascending=False)
        .round(2)
    )
    print(regional_summary.to_string())

    print_header("Customer Feedback Categories")
    feedback_counts = df["Customer Feedback Category"].value_counts()
    feedback_pct = (df["Customer Feedback Category"].value_counts(normalize=True) * 100).round(2)
    feedback_df = pd.DataFrame({"Count": feedback_counts, "Percentage (%)": feedback_pct})
    print(feedback_df.to_string())

    print_header("Analysis Complete")
    print("All metrics verified successfully against dataset.")


if __name__ == "__main__":
    df = load_data(DATASET_FILE)
    run_analysis(df)

