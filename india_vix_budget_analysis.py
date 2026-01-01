#!/usr/bin/env python3
"""
India VIX Pre-Budget Analysis Script
=====================================
This script analyzes India VIX (Volatility Index) behavior before Indian Union Budget
announcements over the past 10 years (2015-2025).

Author: Generated for pre-budget volatility analysis
Date: January 2026
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
import os

warnings.filterwarnings('ignore')

# Set display options for pandas
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# Create output directory
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_progress(message: str) -> None:
    """Print a progress update."""
    print(f"[INFO] {message}")


def get_budget_dates() -> pd.DataFrame:
    """
    Define the exact dates of Indian Union Budget announcements for the past 10 years.

    Returns:
        DataFrame with budget dates, years, and budget types
    """
    budget_info = [
        {"year": 2025, "date": "2025-02-01", "type": "Full"},
        {"year": 2024, "date": "2024-07-23", "type": "Post-Election Full"},
        {"year": 2024, "date": "2024-02-01", "type": "Interim"},
        {"year": 2023, "date": "2023-02-01", "type": "Full"},
        {"year": 2022, "date": "2022-02-01", "type": "Full"},
        {"year": 2021, "date": "2021-02-01", "type": "Full"},
        {"year": 2020, "date": "2020-02-01", "type": "Full"},
        {"year": 2019, "date": "2019-07-05", "type": "Post-Election Full"},
        {"year": 2019, "date": "2019-02-01", "type": "Interim"},
        {"year": 2018, "date": "2018-02-01", "type": "Full"},
        {"year": 2017, "date": "2017-02-01", "type": "Full"},
        {"year": 2016, "date": "2016-02-29", "type": "Full"},
        {"year": 2015, "date": "2015-02-28", "type": "Full"},
    ]

    df = pd.DataFrame(budget_info)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date').reset_index(drop=True)

    return df


def load_local_vix_data(filepath: str) -> pd.DataFrame:
    """
    Load India VIX data from a local CSV file.

    Args:
        filepath: Path to the CSV file

    Returns:
        DataFrame with VIX data
    """
    print_progress(f"Loading VIX data from local file: {filepath}")

    df = pd.read_csv(filepath)

    # Try to identify the date column
    date_cols = ['Date', 'date', 'DATE', 'Timestamp', 'timestamp']
    date_col = None
    for col in date_cols:
        if col in df.columns:
            date_col = col
            break

    if date_col is None:
        # Use first column as date
        date_col = df.columns[0]

    df['Date'] = pd.to_datetime(df[date_col])

    # Rename columns to standard format if needed
    column_mapping = {
        'open': 'Open', 'OPEN': 'Open',
        'high': 'High', 'HIGH': 'High',
        'low': 'Low', 'LOW': 'Low',
        'close': 'Close', 'CLOSE': 'Close',
        'volume': 'Volume', 'VOLUME': 'Volume'
    }

    df = df.rename(columns=column_mapping)

    print_progress(f"Loaded {len(df)} records from local file")

    return df


def get_sample_vix_data() -> pd.DataFrame:
    """
    Generate sample India VIX data for demonstration/testing purposes.
    This data is based on historical patterns but is simulated for testing.

    Returns:
        DataFrame with sample VIX OHLCV data
    """
    print_progress("Using sample data for demonstration...")

    # Sample data covering key periods around budget dates (2015-2025)
    # Values are representative of typical India VIX ranges (12-30 normally, spikes to 40+)
    sample_data = [
        # 2015 Budget (Feb 28) - Pre-budget period
        {"Date": "2015-01-30", "Open": 16.5, "High": 17.2, "Low": 16.1, "Close": 16.8, "Volume": 0},
        {"Date": "2015-02-02", "Open": 16.9, "High": 17.5, "Low": 16.5, "Close": 17.1, "Volume": 0},
        {"Date": "2015-02-06", "Open": 17.2, "High": 18.0, "Low": 16.9, "Close": 17.5, "Volume": 0},
        {"Date": "2015-02-13", "Open": 17.8, "High": 18.5, "Low": 17.4, "Close": 18.2, "Volume": 0},
        {"Date": "2015-02-20", "Open": 18.5, "High": 19.2, "Low": 18.1, "Close": 18.9, "Volume": 0},
        {"Date": "2015-02-27", "Open": 19.2, "High": 20.5, "Low": 18.8, "Close": 20.1, "Volume": 0},

        # 2016 Budget (Feb 29) - Pre-budget period
        {"Date": "2016-02-01", "Open": 21.5, "High": 22.3, "Low": 21.1, "Close": 21.8, "Volume": 0},
        {"Date": "2016-02-05", "Open": 22.1, "High": 23.0, "Low": 21.7, "Close": 22.5, "Volume": 0},
        {"Date": "2016-02-12", "Open": 23.5, "High": 24.5, "Low": 23.1, "Close": 24.0, "Volume": 0},
        {"Date": "2016-02-19", "Open": 24.2, "High": 25.5, "Low": 23.8, "Close": 25.1, "Volume": 0},
        {"Date": "2016-02-26", "Open": 25.5, "High": 26.8, "Low": 25.0, "Close": 26.2, "Volume": 0},
        {"Date": "2016-02-29", "Open": 26.5, "High": 27.5, "Low": 25.5, "Close": 26.0, "Volume": 0},

        # 2017 Budget (Feb 1) - Pre-budget period
        {"Date": "2017-01-04", "Open": 13.5, "High": 14.0, "Low": 13.2, "Close": 13.8, "Volume": 0},
        {"Date": "2017-01-11", "Open": 13.9, "High": 14.5, "Low": 13.6, "Close": 14.2, "Volume": 0},
        {"Date": "2017-01-18", "Open": 14.5, "High": 15.0, "Low": 14.2, "Close": 14.8, "Volume": 0},
        {"Date": "2017-01-25", "Open": 15.0, "High": 15.8, "Low": 14.7, "Close": 15.5, "Volume": 0},
        {"Date": "2017-02-01", "Open": 15.8, "High": 16.5, "Low": 15.2, "Close": 15.2, "Volume": 0},

        # 2018 Budget (Feb 1) - Pre-budget period
        {"Date": "2018-01-04", "Open": 12.8, "High": 13.2, "Low": 12.5, "Close": 13.0, "Volume": 0},
        {"Date": "2018-01-11", "Open": 13.2, "High": 13.8, "Low": 12.9, "Close": 13.5, "Volume": 0},
        {"Date": "2018-01-18", "Open": 13.8, "High": 14.5, "Low": 13.5, "Close": 14.2, "Volume": 0},
        {"Date": "2018-01-25", "Open": 14.5, "High": 15.2, "Low": 14.2, "Close": 14.9, "Volume": 0},
        {"Date": "2018-02-01", "Open": 15.2, "High": 16.0, "Low": 14.8, "Close": 15.5, "Volume": 0},

        # 2019 Interim Budget (Feb 1) - Pre-budget period
        {"Date": "2019-01-04", "Open": 17.5, "High": 18.0, "Low": 17.1, "Close": 17.8, "Volume": 0},
        {"Date": "2019-01-11", "Open": 18.0, "High": 18.8, "Low": 17.6, "Close": 18.5, "Volume": 0},
        {"Date": "2019-01-18", "Open": 18.8, "High": 19.5, "Low": 18.4, "Close": 19.2, "Volume": 0},
        {"Date": "2019-01-25", "Open": 19.5, "High": 20.2, "Low": 19.0, "Close": 19.8, "Volume": 0},
        {"Date": "2019-02-01", "Open": 20.2, "High": 21.0, "Low": 19.5, "Close": 19.5, "Volume": 0},

        # 2019 Full Budget (Jul 5) - Post-election, pre-budget period
        {"Date": "2019-06-07", "Open": 15.5, "High": 16.0, "Low": 15.1, "Close": 15.8, "Volume": 0},
        {"Date": "2019-06-14", "Open": 15.9, "High": 16.5, "Low": 15.5, "Close": 16.2, "Volume": 0},
        {"Date": "2019-06-21", "Open": 16.5, "High": 17.2, "Low": 16.1, "Close": 16.8, "Volume": 0},
        {"Date": "2019-06-28", "Open": 17.0, "High": 17.8, "Low": 16.6, "Close": 17.5, "Volume": 0},
        {"Date": "2019-07-05", "Open": 17.8, "High": 18.5, "Low": 17.2, "Close": 17.2, "Volume": 0},

        # 2020 Budget (Feb 1) - Pre-COVID, pre-budget period
        {"Date": "2020-01-03", "Open": 11.5, "High": 12.0, "Low": 11.2, "Close": 11.8, "Volume": 0},
        {"Date": "2020-01-10", "Open": 12.0, "High": 12.5, "Low": 11.7, "Close": 12.2, "Volume": 0},
        {"Date": "2020-01-17", "Open": 12.5, "High": 13.2, "Low": 12.2, "Close": 13.0, "Volume": 0},
        {"Date": "2020-01-24", "Open": 13.2, "High": 14.0, "Low": 12.8, "Close": 13.8, "Volume": 0},
        {"Date": "2020-01-31", "Open": 14.0, "High": 15.5, "Low": 13.5, "Close": 15.2, "Volume": 0},

        # 2021 Budget (Feb 1) - Post-COVID recovery, pre-budget period
        {"Date": "2021-01-04", "Open": 22.5, "High": 23.2, "Low": 22.0, "Close": 22.8, "Volume": 0},
        {"Date": "2021-01-11", "Open": 23.0, "High": 23.8, "Low": 22.5, "Close": 23.5, "Volume": 0},
        {"Date": "2021-01-18", "Open": 23.8, "High": 24.5, "Low": 23.2, "Close": 24.0, "Volume": 0},
        {"Date": "2021-01-25", "Open": 24.5, "High": 26.0, "Low": 24.0, "Close": 25.8, "Volume": 0},
        {"Date": "2021-02-01", "Open": 26.0, "High": 27.5, "Low": 24.5, "Close": 24.5, "Volume": 0},

        # 2022 Budget (Feb 1) - Pre-budget period
        {"Date": "2022-01-04", "Open": 17.5, "High": 18.2, "Low": 17.0, "Close": 17.8, "Volume": 0},
        {"Date": "2022-01-11", "Open": 18.0, "High": 18.8, "Low": 17.5, "Close": 18.5, "Volume": 0},
        {"Date": "2022-01-18", "Open": 18.8, "High": 20.5, "Low": 18.2, "Close": 20.0, "Volume": 0},
        {"Date": "2022-01-25", "Open": 20.2, "High": 22.5, "Low": 19.8, "Close": 22.0, "Volume": 0},
        {"Date": "2022-02-01", "Open": 22.5, "High": 24.0, "Low": 21.5, "Close": 21.8, "Volume": 0},

        # 2023 Budget (Feb 1) - Pre-budget period
        {"Date": "2023-01-04", "Open": 14.5, "High": 15.0, "Low": 14.2, "Close": 14.8, "Volume": 0},
        {"Date": "2023-01-11", "Open": 15.0, "High": 15.5, "Low": 14.7, "Close": 15.2, "Volume": 0},
        {"Date": "2023-01-18", "Open": 15.5, "High": 16.2, "Low": 15.2, "Close": 16.0, "Volume": 0},
        {"Date": "2023-01-25", "Open": 16.2, "High": 17.0, "Low": 15.8, "Close": 16.5, "Volume": 0},
        {"Date": "2023-02-01", "Open": 16.8, "High": 17.5, "Low": 16.0, "Close": 16.2, "Volume": 0},

        # 2024 Interim Budget (Feb 1) - Pre-election budget
        {"Date": "2024-01-04", "Open": 13.2, "High": 13.8, "Low": 13.0, "Close": 13.5, "Volume": 0},
        {"Date": "2024-01-11", "Open": 13.6, "High": 14.2, "Low": 13.3, "Close": 14.0, "Volume": 0},
        {"Date": "2024-01-18", "Open": 14.2, "High": 15.0, "Low": 13.9, "Close": 14.8, "Volume": 0},
        {"Date": "2024-01-25", "Open": 14.9, "High": 15.5, "Low": 14.5, "Close": 15.2, "Volume": 0},
        {"Date": "2024-02-01", "Open": 15.5, "High": 16.2, "Low": 14.8, "Close": 15.0, "Volume": 0},

        # 2024 Full Budget (Jul 23) - Post-election
        {"Date": "2024-06-25", "Open": 12.5, "High": 13.0, "Low": 12.2, "Close": 12.8, "Volume": 0},
        {"Date": "2024-07-02", "Open": 13.0, "High": 13.5, "Low": 12.7, "Close": 13.2, "Volume": 0},
        {"Date": "2024-07-09", "Open": 13.4, "High": 14.0, "Low": 13.1, "Close": 13.8, "Volume": 0},
        {"Date": "2024-07-16", "Open": 14.0, "High": 14.8, "Low": 13.7, "Close": 14.5, "Volume": 0},
        {"Date": "2024-07-23", "Open": 14.8, "High": 15.5, "Low": 14.2, "Close": 14.2, "Volume": 0},

        # 2025 Budget (Feb 1) - Pre-budget period (projected/estimated)
        {"Date": "2025-01-03", "Open": 13.8, "High": 14.2, "Low": 13.5, "Close": 14.0, "Volume": 0},
        {"Date": "2025-01-10", "Open": 14.2, "High": 14.8, "Low": 13.9, "Close": 14.5, "Volume": 0},
        {"Date": "2025-01-17", "Open": 14.8, "High": 15.5, "Low": 14.5, "Close": 15.2, "Volume": 0},
        {"Date": "2025-01-24", "Open": 15.4, "High": 16.2, "Low": 15.0, "Close": 16.0, "Volume": 0},
        {"Date": "2025-01-31", "Open": 16.2, "High": 17.0, "Low": 15.8, "Close": 16.5, "Volume": 0},
    ]

    df = pd.DataFrame(sample_data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def download_vix_data(start_date: str = "2015-01-01", end_date: str = None) -> pd.DataFrame:
    """
    Download India VIX historical data from Yahoo Finance.
    Falls back to sample data if download fails.

    Args:
        start_date: Start date for data download (YYYY-MM-DD)
        end_date: End date for data download (defaults to today)

    Returns:
        DataFrame with VIX OHLCV data
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    print_progress(f"Attempting to download India VIX data from {start_date} to {end_date}...")

    try:
        # Download India VIX data
        ticker = yf.Ticker("^INDIAVIX")
        vix_data = ticker.history(start=start_date, end=end_date)

        if vix_data.empty:
            raise ValueError("No data downloaded from Yahoo Finance.")

        # Reset index to make Date a column
        vix_data = vix_data.reset_index()

        # Ensure Date column is datetime
        if 'Date' in vix_data.columns:
            vix_data['Date'] = pd.to_datetime(vix_data['Date']).dt.tz_localize(None)

        # Keep only relevant columns
        columns_to_keep = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        available_columns = [col for col in columns_to_keep if col in vix_data.columns]
        vix_data = vix_data[available_columns]

        print_progress(f"Downloaded {len(vix_data)} trading days of VIX data")
        print_progress(f"Date range: {vix_data['Date'].min().date()} to {vix_data['Date'].max().date()}")

        return vix_data

    except Exception as e:
        print(f"[WARNING] Failed to download VIX data from Yahoo Finance: {e}")
        print_progress("Falling back to sample data for demonstration...")
        print_progress("NOTE: For actual analysis, please run this script in an environment with internet access")
        print_progress("      or provide a local CSV file with historical India VIX data.")

        return get_sample_vix_data()


def get_trading_day_on_or_before(vix_data: pd.DataFrame, target_date: datetime) -> Tuple[Optional[datetime], Optional[float], str]:
    """
    Find the closest trading day on or before the target date.

    Args:
        vix_data: DataFrame with VIX data
        target_date: The target date to find

    Returns:
        Tuple of (actual_date, close_value, adjustment_note)
    """
    # Filter data up to and including target date
    available_dates = vix_data[vix_data['Date'] <= target_date]

    if available_dates.empty:
        return None, None, "No data available before this date"

    # Get the closest trading day
    actual_date = available_dates['Date'].max()
    close_value = available_dates[available_dates['Date'] == actual_date]['Close'].values[0]

    # Check if adjustment was needed
    days_diff = (target_date - actual_date).days
    if days_diff == 0:
        adjustment_note = ""
    else:
        adjustment_note = f"Adjusted: Used {actual_date.strftime('%Y-%m-%d')} ({days_diff} day(s) earlier)"

    return actual_date, close_value, adjustment_note


def analyze_budget_vix(vix_data: pd.DataFrame, budget_df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze VIX levels and changes for each budget announcement.

    Args:
        vix_data: DataFrame with VIX data
        budget_df: DataFrame with budget dates

    Returns:
        DataFrame with analysis results
    """
    print_section("ANALYZING VIX LEVELS FOR EACH BUDGET")

    results = []

    for _, budget in budget_df.iterrows():
        budget_date = budget['date']
        budget_year = budget['year']
        budget_type = budget['type']

        print_progress(f"Processing budget: {budget_date.strftime('%Y-%m-%d')} ({budget_type})")

        # Define time points before budget (in days)
        time_points = {
            '4w_before': 28,
            '3w_before': 21,
            '2w_before': 14,
            '1w_before': 7,
            'budget_day': 0
        }

        row = {
            'Year': budget_year,
            'Budget_Date': budget_date.strftime('%Y-%m-%d'),
            'Budget_Type': budget_type
        }

        vix_values = {}
        adjustments = []

        # Get VIX values for each time point
        for label, days_before in time_points.items():
            target_date = budget_date - timedelta(days=days_before)
            actual_date, vix_value, adjustment_note = get_trading_day_on_or_before(vix_data, target_date)

            col_name = f'VIX_{label}'
            row[col_name] = vix_value
            vix_values[label] = vix_value

            if adjustment_note:
                adjustments.append(f"{label}: {adjustment_note}")

        # Calculate percentage changes
        if vix_values['4w_before'] and vix_values['3w_before']:
            row['Change_4w_to_3w_pct'] = ((vix_values['3w_before'] - vix_values['4w_before']) / vix_values['4w_before']) * 100
        else:
            row['Change_4w_to_3w_pct'] = None

        if vix_values['3w_before'] and vix_values['2w_before']:
            row['Change_3w_to_2w_pct'] = ((vix_values['2w_before'] - vix_values['3w_before']) / vix_values['3w_before']) * 100
        else:
            row['Change_3w_to_2w_pct'] = None

        if vix_values['2w_before'] and vix_values['1w_before']:
            row['Change_2w_to_1w_pct'] = ((vix_values['1w_before'] - vix_values['2w_before']) / vix_values['2w_before']) * 100
        else:
            row['Change_2w_to_1w_pct'] = None

        if vix_values['1w_before'] and vix_values['budget_day']:
            row['Change_1w_to_budget_pct'] = ((vix_values['budget_day'] - vix_values['1w_before']) / vix_values['1w_before']) * 100
        else:
            row['Change_1w_to_budget_pct'] = None

        if vix_values['4w_before'] and vix_values['budget_day']:
            row['Total_change_4w_to_budget_pct'] = ((vix_values['budget_day'] - vix_values['4w_before']) / vix_values['4w_before']) * 100
        else:
            row['Total_change_4w_to_budget_pct'] = None

        # Store adjustment notes
        row['Date_Adjustments'] = "; ".join(adjustments) if adjustments else "None"

        results.append(row)

    results_df = pd.DataFrame(results)

    return results_df


def calculate_summary_statistics(results_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Calculate summary statistics for VIX changes across different budget types.

    Args:
        results_df: DataFrame with analysis results

    Returns:
        Dictionary of summary DataFrames
    """
    print_section("CALCULATING SUMMARY STATISTICS")

    change_columns = [
        'Change_4w_to_3w_pct',
        'Change_3w_to_2w_pct',
        'Change_2w_to_1w_pct',
        'Change_1w_to_budget_pct',
        'Total_change_4w_to_budget_pct'
    ]

    summaries = {}

    # Define budget type groups
    groups = {
        'All_Budgets': results_df,
        'Full_Budgets': results_df[results_df['Budget_Type'] == 'Full'],
        'Interim_Budgets': results_df[results_df['Budget_Type'] == 'Interim'],
        'Post_Election_Budgets': results_df[results_df['Budget_Type'].str.contains('Post-Election', na=False)]
    }

    for group_name, group_df in groups.items():
        if len(group_df) == 0:
            print_progress(f"No data for {group_name}")
            continue

        print_progress(f"Calculating statistics for {group_name} ({len(group_df)} budgets)")

        stats = []
        for col in change_columns:
            valid_data = group_df[col].dropna()

            if len(valid_data) == 0:
                continue

            col_stats = {
                'Metric': col.replace('_pct', ' (%)').replace('_', ' '),
                'Count': len(valid_data),
                'Mean': valid_data.mean(),
                'Median': valid_data.median(),
                'Std_Dev': valid_data.std(),
                'Min': valid_data.min(),
                'Max': valid_data.max(),
            }

            # Find year of max and min
            if len(valid_data) > 0:
                max_idx = group_df[col].idxmax()
                min_idx = group_df[col].idxmin()
                col_stats['Max_Year'] = f"{group_df.loc[max_idx, 'Year']} ({group_df.loc[max_idx, 'Budget_Date']})"
                col_stats['Min_Year'] = f"{group_df.loc[min_idx, 'Year']} ({group_df.loc[min_idx, 'Budget_Date']})"

            stats.append(col_stats)

        if stats:
            summaries[group_name] = pd.DataFrame(stats)

    return summaries


def create_visualizations(results_df: pd.DataFrame) -> None:
    """
    Create all required visualizations.

    Args:
        results_df: DataFrame with analysis results
    """
    print_section("CREATING VISUALIZATIONS")

    # Set style
    plt.style.use('seaborn-v0_8-whitegrid')
    sns.set_palette("husl")

    # 1. Line chart: Average VIX movement pattern across all years
    print_progress("Creating line chart of average VIX movement pattern...")

    fig, ax = plt.subplots(figsize=(12, 7))

    vix_columns = ['VIX_4w_before', 'VIX_3w_before', 'VIX_2w_before', 'VIX_1w_before', 'VIX_budget_day']
    time_labels = ['4 Weeks Before', '3 Weeks Before', '2 Weeks Before', '1 Week Before', 'Budget Day']

    # Calculate average, median, max, and min for each time point
    avg_values = [results_df[col].mean() for col in vix_columns]
    median_values = [results_df[col].median() for col in vix_columns]
    max_values = [results_df[col].max() for col in vix_columns]
    min_values = [results_df[col].min() for col in vix_columns]

    x = range(len(time_labels))

    ax.fill_between(x, min_values, max_values, alpha=0.2, color='blue', label='Min-Max Range')
    ax.plot(x, avg_values, 'b-o', linewidth=2, markersize=10, label='Mean VIX')
    ax.plot(x, median_values, 'g--s', linewidth=2, markersize=8, label='Median VIX')

    ax.set_xticks(x)
    ax.set_xticklabels(time_labels, fontsize=11)
    ax.set_xlabel('Time Relative to Budget', fontsize=12)
    ax.set_ylabel('India VIX Level', fontsize=12)
    ax.set_title('Average India VIX Movement Pattern Before Union Budget\n(2015-2025)', fontsize=14, fontweight='bold')
    ax.legend(loc='best', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/01_average_vix_pattern.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 2. Heatmap: VIX percentage changes for each year and time period
    print_progress("Creating heatmap of VIX percentage changes...")

    fig, ax = plt.subplots(figsize=(14, 10))

    change_columns = [
        'Change_4w_to_3w_pct',
        'Change_3w_to_2w_pct',
        'Change_2w_to_1w_pct',
        'Change_1w_to_budget_pct',
        'Total_change_4w_to_budget_pct'
    ]

    change_labels = [
        '4W → 3W',
        '3W → 2W',
        '2W → 1W',
        '1W → Budget',
        'Total (4W → Budget)'
    ]

    # Create a label combining year and budget type
    results_df['Label'] = results_df.apply(
        lambda r: f"{r['Budget_Date'][:7]} ({r['Budget_Type'][:4]})"
        if r['Budget_Type'] != 'Full' else f"{r['Budget_Date'][:7]}",
        axis=1
    )

    heatmap_data = results_df[['Label'] + change_columns].set_index('Label')
    heatmap_data.columns = change_labels

    # Create diverging colormap centered at 0
    cmap = sns.diverging_palette(240, 10, n=20, as_cmap=True)

    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap=cmap, center=0,
                linewidths=0.5, cbar_kws={'label': 'Percentage Change (%)'}, ax=ax)

    ax.set_title('India VIX Percentage Changes Before Each Budget\n(Blue = Decrease, Red = Increase)',
                 fontsize=14, fontweight='bold')
    ax.set_xlabel('Time Period', fontsize=12)
    ax.set_ylabel('Budget Date', fontsize=12)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/02_vix_changes_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 3. Bar chart: Total 4-week pre-budget VIX changes by year
    print_progress("Creating bar chart of total pre-budget VIX changes...")

    fig, ax = plt.subplots(figsize=(14, 7))

    # Sort by date for chronological order
    plot_data = results_df.sort_values('Budget_Date')

    colors = ['green' if x < 0 else 'red' for x in plot_data['Total_change_4w_to_budget_pct']]

    bars = ax.bar(range(len(plot_data)), plot_data['Total_change_4w_to_budget_pct'], color=colors, edgecolor='black')

    ax.set_xticks(range(len(plot_data)))
    ax.set_xticklabels([f"{d[:7]}\n({t[:4]})" if t != 'Full' else d[:7]
                        for d, t in zip(plot_data['Budget_Date'], plot_data['Budget_Type'])],
                       rotation=45, ha='right', fontsize=9)

    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    ax.set_xlabel('Budget Date', fontsize=12)
    ax.set_ylabel('Total VIX Change (%)', fontsize=12)
    ax.set_title('Total India VIX Change (4 Weeks Before to Budget Day)\n(Red = Increase, Green = Decrease)',
                 fontsize=14, fontweight='bold')

    # Add value labels on bars
    for bar, val in zip(bars, plot_data['Total_change_4w_to_budget_pct']):
        height = bar.get_height()
        ax.annotate(f'{val:.1f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3 if height >= 0 else -15),
                    textcoords="offset points",
                    ha='center', va='bottom' if height >= 0 else 'top',
                    fontsize=8, fontweight='bold')

    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/03_total_prebudget_changes.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 4. Box plot: Distribution of VIX changes at each time interval
    print_progress("Creating box plot of VIX change distributions...")

    fig, ax = plt.subplots(figsize=(12, 7))

    # Prepare data for boxplot
    box_data = []
    box_labels = []

    for col, label in zip(change_columns[:-1], change_labels[:-1]):  # Exclude total
        valid_data = results_df[col].dropna().values
        box_data.append(valid_data)
        box_labels.append(label)

    bp = ax.boxplot(box_data, labels=box_labels, patch_artist=True)

    colors = plt.cm.Blues(np.linspace(0.3, 0.8, len(box_data)))
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)

    ax.axhline(y=0, color='red', linestyle='--', linewidth=1, alpha=0.7)
    ax.set_xlabel('Time Period', fontsize=12)
    ax.set_ylabel('Percentage Change (%)', fontsize=12)
    ax.set_title('Distribution of India VIX Changes at Each Time Interval\n(2015-2025)',
                 fontsize=14, fontweight='bold')
    ax.grid(True, axis='y', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/04_vix_change_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()

    # 5. Additional: Individual year trajectories
    print_progress("Creating individual year VIX trajectories...")

    fig, ax = plt.subplots(figsize=(14, 8))

    # Normalize VIX values to percentage change from 4 weeks before
    for idx, row in results_df.iterrows():
        base_value = row['VIX_4w_before']
        if pd.isna(base_value) or base_value == 0:
            continue

        normalized = [
            0,  # 4 weeks before (base)
            ((row['VIX_3w_before'] - base_value) / base_value) * 100 if pd.notna(row['VIX_3w_before']) else np.nan,
            ((row['VIX_2w_before'] - base_value) / base_value) * 100 if pd.notna(row['VIX_2w_before']) else np.nan,
            ((row['VIX_1w_before'] - base_value) / base_value) * 100 if pd.notna(row['VIX_1w_before']) else np.nan,
            ((row['VIX_budget_day'] - base_value) / base_value) * 100 if pd.notna(row['VIX_budget_day']) else np.nan,
        ]

        label = f"{row['Budget_Date'][:7]}"
        if row['Budget_Type'] != 'Full':
            label += f" ({row['Budget_Type'][:4]})"

        ax.plot(range(5), normalized, '-o', linewidth=1.5, markersize=6, label=label, alpha=0.7)

    ax.axhline(y=0, color='black', linestyle='--', linewidth=1)
    ax.set_xticks(range(5))
    ax.set_xticklabels(time_labels, fontsize=11)
    ax.set_xlabel('Time Relative to Budget', fontsize=12)
    ax.set_ylabel('Percentage Change from 4 Weeks Before (%)', fontsize=12)
    ax.set_title('India VIX Trajectories Before Each Budget\n(Normalized to 4 Weeks Before = 0%)',
                 fontsize=14, fontweight='bold')
    ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/05_individual_year_trajectories.png', dpi=300, bbox_inches='tight')
    plt.close()

    print_progress("All visualizations saved to output directory")


def generate_written_analysis(results_df: pd.DataFrame, summaries: Dict[str, pd.DataFrame]) -> str:
    """
    Generate written analysis based on the data.

    Args:
        results_df: DataFrame with analysis results
        summaries: Dictionary of summary statistics

    Returns:
        String containing the written analysis
    """
    print_section("GENERATING WRITTEN ANALYSIS")

    analysis = []
    analysis.append("=" * 80)
    analysis.append("INDIA VIX PRE-BUDGET BEHAVIOR ANALYSIS REPORT")
    analysis.append("=" * 80)
    analysis.append(f"\nAnalysis Period: 2015-2025")
    analysis.append(f"Total Budgets Analyzed: {len(results_df)}")
    analysis.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Key Findings
    analysis.append("\n" + "-" * 80)
    analysis.append("KEY FINDINGS")
    analysis.append("-" * 80)

    # Overall pattern
    if 'All_Budgets' in summaries:
        all_stats = summaries['All_Budgets']

        # Get total change stats
        total_row = all_stats[all_stats['Metric'].str.contains('Total', na=False)]
        if len(total_row) > 0:
            mean_total = total_row['Mean'].values[0]
            median_total = total_row['Median'].values[0]
            max_total = total_row['Max'].values[0]
            min_total = total_row['Min'].values[0]
            max_year = total_row['Max_Year'].values[0]
            min_year = total_row['Min_Year'].values[0]

            analysis.append(f"\n1. OVERALL PRE-BUDGET VIX BEHAVIOR (4 weeks before to Budget Day):")
            analysis.append(f"   - Average change: {mean_total:+.2f}%")
            analysis.append(f"   - Median change: {median_total:+.2f}%")
            analysis.append(f"   - Maximum spike: {max_total:+.2f}% ({max_year})")
            analysis.append(f"   - Maximum decline: {min_total:+.2f}% ({min_year})")

            if mean_total > 0:
                analysis.append(f"\n   PATTERN: VIX tends to INCREASE on average before budgets, suggesting heightened uncertainty.")
            else:
                analysis.append(f"\n   PATTERN: VIX tends to DECREASE on average before budgets, suggesting reduced uncertainty.")

        # Weekly patterns
        analysis.append(f"\n2. WEEKLY PATTERN ANALYSIS:")

        for _, row in all_stats.iterrows():
            metric = row['Metric']
            mean_val = row['Mean']
            if 'Total' not in metric:
                direction = "increases" if mean_val > 0 else "decreases"
                analysis.append(f"   - {metric}: Average {mean_val:+.2f}% (VIX typically {direction})")

        # Find the week with maximum average change
        weekly_changes = all_stats[~all_stats['Metric'].str.contains('Total', na=False)]
        if len(weekly_changes) > 0:
            max_week = weekly_changes.loc[weekly_changes['Mean'].abs().idxmax()]
            analysis.append(f"\n   MOST VOLATILE PERIOD: {max_week['Metric']} with average change of {max_week['Mean']:+.2f}%")

    # Outlier Years
    analysis.append(f"\n3. OUTLIER YEARS AND NOTABLE OBSERVATIONS:")

    # Find significant outliers (> 1.5 std from mean)
    mean_change = results_df['Total_change_4w_to_budget_pct'].mean()
    std_change = results_df['Total_change_4w_to_budget_pct'].std()

    outliers = results_df[
        (results_df['Total_change_4w_to_budget_pct'] > mean_change + 1.5 * std_change) |
        (results_df['Total_change_4w_to_budget_pct'] < mean_change - 1.5 * std_change)
    ]

    if len(outliers) > 0:
        for _, row in outliers.iterrows():
            change = row['Total_change_4w_to_budget_pct']
            budget_type = row['Budget_Type']
            budget_date = row['Budget_Date']
            year = row['Year']

            analysis.append(f"\n   {budget_date} ({budget_type}):")
            analysis.append(f"   - Total VIX change: {change:+.2f}%")

            # Add context for notable years
            if 'Post-Election' in budget_type:
                analysis.append(f"   - Context: Post-election budget following general elections")
            if 'Interim' in budget_type:
                analysis.append(f"   - Context: Interim budget before elections")
            if year == 2020:
                analysis.append(f"   - Context: COVID-19 pandemic beginning")
            if year == 2022:
                analysis.append(f"   - Context: Post-COVID recovery period")
    else:
        analysis.append("   No significant outliers detected (>1.5 standard deviations from mean)")

    # Budget Type Comparison
    analysis.append(f"\n4. BUDGET TYPE COMPARISON:")

    for budget_type, summary in summaries.items():
        if budget_type == 'All_Budgets':
            continue

        total_row = summary[summary['Metric'].str.contains('Total', na=False)]
        if len(total_row) > 0:
            mean_val = total_row['Mean'].values[0]
            count = total_row['Count'].values[0]
            analysis.append(f"\n   {budget_type.replace('_', ' ')} (n={count}):")
            analysis.append(f"   - Average total change: {mean_val:+.2f}%")

    # Average spike in 2-3 weeks before budget
    analysis.append(f"\n5. PRE-BUDGET SPIKE ANALYSIS (2-3 weeks before):")

    avg_2w_to_1w = results_df['Change_2w_to_1w_pct'].mean()
    avg_3w_to_2w = results_df['Change_3w_to_2w_pct'].mean()
    combined_avg = (avg_2w_to_1w + avg_3w_to_2w) / 2

    analysis.append(f"   - Average change 3W to 2W before budget: {avg_3w_to_2w:+.2f}%")
    analysis.append(f"   - Average change 2W to 1W before budget: {avg_2w_to_1w:+.2f}%")
    analysis.append(f"   - Combined average for 2-3 week period: {combined_avg:+.2f}%")

    # Consistency analysis
    analysis.append(f"\n6. PATTERN CONSISTENCY:")

    positive_count = (results_df['Total_change_4w_to_budget_pct'] > 0).sum()
    negative_count = (results_df['Total_change_4w_to_budget_pct'] <= 0).sum()
    total = len(results_df)

    analysis.append(f"   - Budgets with VIX increase: {positive_count}/{total} ({100*positive_count/total:.1f}%)")
    analysis.append(f"   - Budgets with VIX decrease: {negative_count}/{total} ({100*negative_count/total:.1f}%)")

    cv = (std_change / abs(mean_change)) * 100 if mean_change != 0 else float('inf')
    analysis.append(f"   - Coefficient of Variation: {cv:.1f}%")

    if cv > 100:
        analysis.append("   - CONCLUSION: HIGH VARIABILITY - Pre-budget VIX behavior is NOT consistent year-to-year")
    elif cv > 50:
        analysis.append("   - CONCLUSION: MODERATE VARIABILITY - Some pattern exists but with significant variation")
    else:
        analysis.append("   - CONCLUSION: LOW VARIABILITY - Pre-budget VIX behavior shows consistent pattern")

    # Trading implications
    analysis.append(f"\n7. KEY INSIGHTS FOR VOLATILITY ANALYSIS:")
    analysis.append(f"   - VIX typically {'rises' if mean_change > 0 else 'falls'} in the 4 weeks before budget")
    analysis.append(f"   - The most significant moves occur in the {max_week['Metric'].split('(')[0].strip()} period")
    analysis.append(f"   - Post-election budgets may show different patterns due to reduced policy uncertainty")
    analysis.append(f"   - Interim budgets preceding elections tend to have unique volatility characteristics")

    analysis.append("\n" + "=" * 80)
    analysis.append("END OF ANALYSIS REPORT")
    analysis.append("=" * 80)

    return "\n".join(analysis)


def save_outputs(results_df: pd.DataFrame, summaries: Dict[str, pd.DataFrame], analysis: str) -> None:
    """
    Save all outputs to files.

    Args:
        results_df: DataFrame with analysis results
        summaries: Dictionary of summary statistics
        analysis: Written analysis string
    """
    print_section("SAVING OUTPUT FILES")

    # Save detailed results CSV
    print_progress("Saving detailed results CSV...")
    results_df.to_csv(f'{OUTPUT_DIR}/india_vix_budget_analysis_detailed.csv', index=False)

    # Save summary statistics
    print_progress("Saving summary statistics...")
    with pd.ExcelWriter(f'{OUTPUT_DIR}/india_vix_summary_statistics.xlsx', engine='openpyxl') as writer:
        for sheet_name, df in summaries.items():
            df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Excel sheet name limit

    # Also save summaries as CSV
    for name, df in summaries.items():
        df.to_csv(f'{OUTPUT_DIR}/summary_{name.lower()}.csv', index=False)

    # Save written analysis
    print_progress("Saving written analysis...")
    with open(f'{OUTPUT_DIR}/india_vix_analysis_report.txt', 'w') as f:
        f.write(analysis)

    print_progress(f"All outputs saved to '{OUTPUT_DIR}/' directory")


def main():
    """Main function to run the complete analysis."""
    print_section("INDIA VIX PRE-BUDGET ANALYSIS")
    print_progress("Starting analysis...")
    print_progress("This script analyzes India VIX behavior before Union Budget announcements (2015-2025)")

    try:
        # Step 1: Get budget dates
        print_section("STEP 1: LOADING BUDGET DATES")
        budget_df = get_budget_dates()
        print_progress(f"Loaded {len(budget_df)} budget dates")
        print(budget_df.to_string(index=False))

        # Step 2: Download VIX data
        print_section("STEP 2: DOWNLOADING INDIA VIX DATA")
        vix_data = download_vix_data(start_date="2014-12-01", end_date=None)

        # Step 3: Analyze VIX for each budget
        print_section("STEP 3: ANALYZING VIX LEVELS")
        results_df = analyze_budget_vix(vix_data, budget_df)

        # Display results
        print("\nDetailed Results:")
        print(results_df.to_string(index=False))

        # Step 4: Calculate summary statistics
        print_section("STEP 4: CALCULATING SUMMARY STATISTICS")
        summaries = calculate_summary_statistics(results_df)

        for name, summary in summaries.items():
            print(f"\n{name.replace('_', ' ')}:")
            print(summary.to_string(index=False))

        # Step 5: Create visualizations
        print_section("STEP 5: CREATING VISUALIZATIONS")
        create_visualizations(results_df)

        # Step 6: Generate written analysis
        print_section("STEP 6: GENERATING WRITTEN ANALYSIS")
        analysis = generate_written_analysis(results_df, summaries)
        print(analysis)

        # Step 7: Save all outputs
        print_section("STEP 7: SAVING OUTPUTS")
        save_outputs(results_df, summaries, analysis)

        print_section("ANALYSIS COMPLETE")
        print_progress("All files have been saved to the 'output' directory:")
        print("  - india_vix_budget_analysis_detailed.csv (detailed data)")
        print("  - india_vix_summary_statistics.xlsx (summary stats)")
        print("  - summary_*.csv (individual summary CSVs)")
        print("  - india_vix_analysis_report.txt (written analysis)")
        print("  - 01_average_vix_pattern.png")
        print("  - 02_vix_changes_heatmap.png")
        print("  - 03_total_prebudget_changes.png")
        print("  - 04_vix_change_distribution.png")
        print("  - 05_individual_year_trajectories.png")

    except Exception as e:
        print(f"\n[ERROR] Analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
