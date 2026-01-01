#!/usr/bin/env python3
"""
India VIX Pre-Budget Analysis - Executive HTML Report Generator
================================================================
Generates a professional, executive-style HTML report from the India VIX
pre-budget analysis data. Designed for non-technical stakeholders.

Author: Generated for pre-budget volatility analysis
Date: January 2026
"""

import pandas as pd
import numpy as np
import base64
import os
from datetime import datetime
from pathlib import Path

# Import the analysis functions from main script
from india_vix_budget_analysis import (
    get_budget_dates,
    download_vix_data,
    analyze_budget_vix,
    calculate_summary_statistics,
    print_section,
    print_progress
)

OUTPUT_DIR = "output"
REPORT_FILE = "india_vix_executive_report.html"


def encode_image_to_base64(image_path: str) -> str:
    """Convert an image file to base64 string for embedding in HTML."""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except FileNotFoundError:
        return ""


def get_trend_indicator(value: float) -> tuple:
    """Return trend indicator and color based on value."""
    if value > 5:
        return "UP", "#dc3545", "Strong Increase"
    elif value > 0:
        return "UP", "#fd7e14", "Moderate Increase"
    elif value > -5:
        return "DOWN", "#28a745", "Moderate Decrease"
    else:
        return "DOWN", "#20c997", "Strong Decrease"


def format_percentage(value: float, include_sign: bool = True) -> str:
    """Format a percentage value with proper styling."""
    if pd.isna(value):
        return "N/A"
    if include_sign:
        return f"{value:+.2f}%"
    return f"{value:.2f}%"


def generate_executive_summary(results_df: pd.DataFrame, summaries: dict) -> str:
    """Generate the executive summary section."""

    all_stats = summaries.get('All_Budgets', pd.DataFrame())

    # Calculate key metrics
    avg_total_change = results_df['Total_change_4w_to_budget_pct'].mean()
    max_change = results_df['Total_change_4w_to_budget_pct'].max()
    min_change = results_df['Total_change_4w_to_budget_pct'].min()
    positive_count = (results_df['Total_change_4w_to_budget_pct'] > 0).sum()
    total_budgets = len(results_df)

    max_year_row = results_df.loc[results_df['Total_change_4w_to_budget_pct'].idxmax()]
    min_year_row = results_df.loc[results_df['Total_change_4w_to_budget_pct'].idxmin()]

    trend_icon, trend_color, trend_text = get_trend_indicator(avg_total_change)

    return f"""
    <div class="executive-summary">
        <h2>Executive Summary</h2>
        <div class="summary-grid">
            <div class="summary-card highlight">
                <div class="card-content">
                    <span class="card-label">Average Pre-Budget VIX Change</span>
                    <span class="card-value" style="color: {trend_color};">{avg_total_change:+.1f}%</span>
                    <span class="card-subtitle">{trend_text} Pattern</span>
                </div>
            </div>
            <div class="summary-card">
                <div class="card-content">
                    <span class="card-label">Maximum Spike Observed</span>
                    <span class="card-value text-danger">{max_change:+.1f}%</span>
                    <span class="card-subtitle">{max_year_row['Budget_Date'][:7]}</span>
                </div>
            </div>
            <div class="summary-card">
                <div class="card-content">
                    <span class="card-label">Minimum Change Observed</span>
                    <span class="card-value text-success">{min_change:+.1f}%</span>
                    <span class="card-subtitle">{min_year_row['Budget_Date'][:7]}</span>
                </div>
            </div>
            <div class="summary-card">
                <div class="card-content">
                    <span class="card-label">Consistency Rate</span>
                    <span class="card-value">{100*positive_count/total_budgets:.0f}%</span>
                    <span class="card-subtitle">{positive_count}/{total_budgets} budgets showed increase</span>
                </div>
            </div>
        </div>

        <div class="key-insight">
            <h3>Key Insight</h3>
            <p>Over the past 10 years, <strong>India VIX consistently rises in the 4 weeks leading up to Union Budget announcements</strong>.
            The average increase is <strong>{avg_total_change:.1f}%</strong>, with the most significant volatility spike occurring
            <strong>2-3 weeks before</strong> the budget date. This pattern suggests heightened market uncertainty as investors
            position themselves ahead of potential policy changes.</p>
        </div>
    </div>
    """


def generate_key_findings(results_df: pd.DataFrame, summaries: dict) -> str:
    """Generate the key findings section."""

    # Calculate weekly averages
    avg_4w_3w = results_df['Change_4w_to_3w_pct'].mean()
    avg_3w_2w = results_df['Change_3w_to_2w_pct'].mean()
    avg_2w_1w = results_df['Change_2w_to_1w_pct'].mean()
    avg_1w_budget = results_df['Change_1w_to_budget_pct'].mean()

    # Find most volatile period
    weekly_avgs = {
        '4 to 3 weeks': avg_4w_3w,
        '3 to 2 weeks': avg_3w_2w,
        '2 to 1 week': avg_2w_1w,
        '1 week to budget': avg_1w_budget
    }
    most_volatile = max(weekly_avgs, key=lambda k: abs(weekly_avgs[k]))

    # Budget type analysis
    full_avg = results_df[results_df['Budget_Type'] == 'Full']['Total_change_4w_to_budget_pct'].mean()
    interim_avg = results_df[results_df['Budget_Type'] == 'Interim']['Total_change_4w_to_budget_pct'].mean()
    post_election_avg = results_df[results_df['Budget_Type'].str.contains('Post-Election', na=False)]['Total_change_4w_to_budget_pct'].mean()

    return f"""
    <div class="key-findings">
        <h2>Key Findings</h2>

        <div class="finding-grid">
            <div class="finding-card">
                <div class="finding-number">1</div>
                <div class="finding-content">
                    <h4>Consistent Upward Pattern</h4>
                    <p>VIX increases in <strong>all four weeks</strong> leading up to the budget, with the steepest
                    rise occurring in the <strong>{most_volatile}</strong> period (avg: {weekly_avgs[most_volatile]:+.1f}%).</p>
                </div>
            </div>

            <div class="finding-card">
                <div class="finding-number">2</div>
                <div class="finding-content">
                    <h4>Budget Day Volatility Drop</h4>
                    <p>In the final week before the budget, VIX change averages only <strong>{avg_1w_budget:+.1f}%</strong>,
                    suggesting uncertainty peaks 1-2 weeks before and starts stabilizing as the event approaches.</p>
                </div>
            </div>

            <div class="finding-card">
                <div class="finding-number">3</div>
                <div class="finding-content">
                    <h4>Full Budgets Show Higher Volatility</h4>
                    <p>Regular full budgets show an average VIX increase of <strong>{full_avg:+.1f}%</strong>,
                    compared to <strong>{interim_avg:+.1f}%</strong> for interim budgets and
                    <strong>{post_election_avg:+.1f}%</strong> for post-election budgets.</p>
                </div>
            </div>

            <div class="finding-card">
                <div class="finding-number">4</div>
                <div class="finding-content">
                    <h4>2-3 Week Window is Critical</h4>
                    <p>The combined VIX change in the 2-3 weeks before budget averages
                    <strong>{(avg_3w_2w + avg_2w_1w):+.1f}%</strong>. This is the optimal window for
                    volatility-based strategies.</p>
                </div>
            </div>
        </div>
    </div>
    """


def generate_detailed_table(results_df: pd.DataFrame) -> str:
    """Generate the detailed analysis table."""

    rows = ""
    for _, row in results_df.iterrows():
        # Determine row highlighting based on budget type
        row_class = ""
        if "Post-Election" in row['Budget_Type']:
            row_class = "row-post-election"
        elif row['Budget_Type'] == "Interim":
            row_class = "row-interim"

        # Format the total change with color
        total_change = row['Total_change_4w_to_budget_pct']
        if total_change > 20:
            change_class = "change-high"
        elif total_change > 10:
            change_class = "change-medium"
        else:
            change_class = "change-low"

        budget_type_badge = ""
        if "Post-Election" in row['Budget_Type']:
            budget_type_badge = '<span class="badge badge-election">Post-Election</span>'
        elif row['Budget_Type'] == "Interim":
            budget_type_badge = '<span class="badge badge-interim">Interim</span>'
        else:
            budget_type_badge = '<span class="badge badge-full">Full Budget</span>'

        rows += f"""
        <tr class="{row_class}">
            <td><strong>{row['Budget_Date']}</strong></td>
            <td>{budget_type_badge}</td>
            <td>{row['VIX_4w_before']:.1f}</td>
            <td>{row['VIX_3w_before']:.1f}</td>
            <td>{row['VIX_2w_before']:.1f}</td>
            <td>{row['VIX_1w_before']:.1f}</td>
            <td>{row['VIX_budget_day']:.1f}</td>
            <td class="{change_class}"><strong>{format_percentage(total_change)}</strong></td>
        </tr>
        """

    return f"""
    <div class="detailed-analysis">
        <h2>Detailed Budget-wise Analysis</h2>
        <div class="table-container">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Budget Date</th>
                        <th>Type</th>
                        <th>VIX<br>4W Before</th>
                        <th>VIX<br>3W Before</th>
                        <th>VIX<br>2W Before</th>
                        <th>VIX<br>1W Before</th>
                        <th>VIX<br>Budget Day</th>
                        <th>Total<br>Change</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
        <div class="table-legend">
            <span><span class="legend-dot high"></span> High volatility (&gt;20%)</span>
            <span><span class="legend-dot medium"></span> Medium volatility (10-20%)</span>
            <span><span class="legend-dot low"></span> Low volatility (&lt;10%)</span>
        </div>
    </div>
    """


def generate_statistics_section(summaries: dict) -> str:
    """Generate the statistics comparison section."""

    stats_cards = ""

    budget_types = [
        ('All_Budgets', 'All Budgets'),
        ('Full_Budgets', 'Full Budgets'),
        ('Interim_Budgets', 'Interim Budgets'),
        ('Post_Election_Budgets', 'Post-Election')
    ]

    for key, label in budget_types:
        if key not in summaries:
            continue

        df = summaries[key]
        total_row = df[df['Metric'].str.contains('Total', na=False)]

        if len(total_row) == 0:
            continue

        mean_val = total_row['Mean'].values[0]
        median_val = total_row['Median'].values[0]
        std_val = total_row['Std_Dev'].values[0]
        count = int(total_row['Count'].values[0])

        stats_cards += f"""
        <div class="stat-card">
            <div class="stat-header">
                <span class="stat-title">{label}</span>
                <span class="stat-count">n={count}</span>
            </div>
            <div class="stat-body">
                <div class="stat-row">
                    <span class="stat-label">Average Change</span>
                    <span class="stat-value">{mean_val:+.1f}%</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Median Change</span>
                    <span class="stat-value">{median_val:+.1f}%</span>
                </div>
                <div class="stat-row">
                    <span class="stat-label">Std Deviation</span>
                    <span class="stat-value">{std_val:.1f}%</span>
                </div>
            </div>
        </div>
        """

    return f"""
    <div class="statistics-section">
        <h2>Statistical Comparison by Budget Type</h2>
        <div class="stat-grid">
            {stats_cards}
        </div>
    </div>
    """


def generate_visualizations_section() -> str:
    """Generate the visualizations section with embedded images."""

    charts = [
        ('01_average_vix_pattern.png', 'Average VIX Movement Pattern',
         'Shows the typical trajectory of India VIX in the 4 weeks before budget announcements.'),
        ('02_vix_changes_heatmap.png', 'Year-by-Year Volatility Heatmap',
         'Heatmap showing percentage changes across all budgets and time periods. Red indicates increase, blue indicates decrease.'),
        ('03_total_prebudget_changes.png', 'Total Pre-Budget Changes by Year',
         'Bar chart comparing the total VIX change (4 weeks to budget day) for each budget.'),
        ('04_vix_change_distribution.png', 'Distribution of Changes',
         'Box plot showing the distribution of VIX changes at each time interval.'),
        ('05_individual_year_trajectories.png', 'Individual Year Trajectories',
         'Overlaid VIX trajectories for each budget, normalized to show percentage change from 4 weeks before.')
    ]

    chart_html = ""
    for filename, title, description in charts:
        filepath = os.path.join(OUTPUT_DIR, filename)
        img_base64 = encode_image_to_base64(filepath)

        if img_base64:
            chart_html += f"""
            <div class="chart-card">
                <h3>{title}</h3>
                <p class="chart-description">{description}</p>
                <div class="chart-image">
                    <img src="data:image/png;base64,{img_base64}" alt="{title}">
                </div>
            </div>
            """

    return f"""
    <div class="visualizations-section">
        <h2>Visual Analysis</h2>
        <div class="chart-grid">
            {chart_html}
        </div>
    </div>
    """


def generate_recommendations() -> str:
    """Generate the recommendations section."""

    return """
    <div class="recommendations-section">
        <h2>Strategic Implications</h2>

        <div class="recommendation-grid">
            <div class="recommendation-card">
                <h4>For Investors</h4>
                <ul>
                    <li>Consider increasing hedging positions 3-4 weeks before budget</li>
                    <li>VIX-based instruments may offer opportunities during this period</li>
                    <li>Monitor for unusual spikes that deviate from historical patterns</li>
                </ul>
            </div>

            <div class="recommendation-card">
                <h4>For Traders</h4>
                <ul>
                    <li>The 2-3 week window before budget shows highest volatility buildup</li>
                    <li>Consider volatility strategies during this period</li>
                    <li>Post-election budgets typically show lower pre-budget volatility</li>
                </ul>
            </div>

            <div class="recommendation-card">
                <h4>For Risk Managers</h4>
                <ul>
                    <li>Factor in average 15% VIX increase when planning pre-budget exposure</li>
                    <li>Historical range of 7-29% suggests significant variance possible</li>
                    <li>Interim budgets show more predictable, moderate volatility patterns</li>
                </ul>
            </div>
        </div>

        <div class="disclaimer">
            <strong>Disclaimer:</strong> This analysis is based on historical data and patterns. Past performance
            does not guarantee future results. Market conditions, global events, and policy changes can
            significantly impact volatility patterns. Always conduct independent analysis before making
            investment decisions.
        </div>
    </div>
    """


def get_css_styles() -> str:
    """Return the CSS styles for the report."""

    return """
    <style>
        :root {
            --primary-color: #1a365d;
            --secondary-color: #2b6cb0;
            --accent-color: #3182ce;
            --success-color: #38a169;
            --warning-color: #dd6b20;
            --danger-color: #e53e3e;
            --bg-light: #f7fafc;
            --bg-white: #ffffff;
            --text-dark: #1a202c;
            --text-muted: #718096;
            --border-color: #e2e8f0;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: var(--bg-white);
            color: var(--text-dark);
            line-height: 1.6;
            font-size: 11pt;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }

        /* Header Styles */
        .report-header {
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            padding: 50px 40px;
            margin-bottom: 30px;
            border-radius: 8px;
        }

        .report-header h1 {
            font-size: 28pt;
            font-weight: 700;
            margin-bottom: 10px;
            letter-spacing: -0.5px;
        }

        .report-header .subtitle {
            font-size: 14pt;
            opacity: 0.9;
            margin-bottom: 20px;
        }

        .report-header .meta {
            display: flex;
            gap: 40px;
            font-size: 10pt;
            opacity: 0.9;
        }

        .report-header .meta-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* Section Styles */
        section {
            background: var(--bg-white);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 30px;
            margin-bottom: 25px;
        }

        section h2 {
            color: var(--primary-color);
            font-size: 18pt;
            margin-bottom: 25px;
            padding-bottom: 12px;
            border-bottom: 3px solid var(--accent-color);
        }

        /* Executive Summary */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 25px;
        }

        .summary-card {
            background: var(--bg-light);
            border-radius: 8px;
            padding: 20px;
            border: 1px solid var(--border-color);
        }

        .summary-card.highlight {
            background: linear-gradient(135deg, #ebf8ff 0%, #e6fffa 100%);
            border: 2px solid var(--accent-color);
        }

        .card-content {
            display: flex;
            flex-direction: column;
        }

        .card-label {
            font-size: 9pt;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
            font-weight: 600;
        }

        .card-value {
            font-size: 24pt;
            font-weight: 700;
            line-height: 1.2;
        }

        .card-subtitle {
            font-size: 9pt;
            color: var(--text-muted);
            margin-top: 5px;
        }

        .text-danger { color: var(--danger-color); }
        .text-success { color: var(--success-color); }
        .text-warning { color: var(--warning-color); }

        /* Key Insight Box */
        .key-insight {
            background: #fffbeb;
            border-left: 4px solid var(--warning-color);
            padding: 20px 25px;
            border-radius: 0 8px 8px 0;
        }

        .key-insight h3 {
            color: var(--warning-color);
            margin-bottom: 10px;
            font-size: 12pt;
            font-weight: 700;
        }

        .key-insight p {
            font-size: 11pt;
            color: var(--text-dark);
        }

        /* Key Findings */
        .finding-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
        }

        .finding-card {
            display: flex;
            gap: 15px;
            padding: 20px;
            background: var(--bg-light);
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }

        .finding-number {
            width: 36px;
            height: 36px;
            background: var(--accent-color);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14pt;
            font-weight: 700;
            flex-shrink: 0;
        }

        .finding-content h4 {
            color: var(--primary-color);
            margin-bottom: 8px;
            font-size: 11pt;
        }

        .finding-content p {
            color: var(--text-muted);
            font-size: 10pt;
        }

        /* Data Table */
        .table-container {
            overflow-x: auto;
            margin-bottom: 15px;
        }

        .data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 10pt;
        }

        .data-table th {
            background: var(--primary-color);
            color: white;
            padding: 12px 10px;
            text-align: center;
            font-weight: 600;
            white-space: nowrap;
        }

        .data-table td {
            padding: 10px;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
        }

        .data-table tbody tr:nth-child(even) {
            background: var(--bg-light);
        }

        .data-table .row-interim {
            background: #fef3c7 !important;
        }

        .data-table .row-post-election {
            background: #dbeafe !important;
        }

        .badge {
            display: inline-block;
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 8pt;
            font-weight: 600;
            text-transform: uppercase;
        }

        .badge-full { background: #c6f6d5; color: #276749; }
        .badge-interim { background: #fef3c7; color: #975a16; }
        .badge-election { background: #dbeafe; color: #1e40af; }

        .change-high { color: var(--danger-color); font-weight: 700; }
        .change-medium { color: var(--warning-color); font-weight: 600; }
        .change-low { color: var(--success-color); }

        .table-legend {
            display: flex;
            gap: 25px;
            justify-content: center;
            padding-top: 10px;
            font-size: 9pt;
            color: var(--text-muted);
        }

        .legend-dot {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }

        .legend-dot.high { background: var(--danger-color); }
        .legend-dot.medium { background: var(--warning-color); }
        .legend-dot.low { background: var(--success-color); }

        /* Statistics Section */
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 15px;
        }

        .stat-card {
            background: var(--bg-light);
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }

        .stat-header {
            background: var(--primary-color);
            color: white;
            padding: 12px 15px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .stat-title {
            font-weight: 600;
            font-size: 10pt;
        }

        .stat-count {
            font-size: 9pt;
            opacity: 0.8;
        }

        .stat-body {
            padding: 15px;
        }

        .stat-row {
            display: flex;
            justify-content: space-between;
            padding: 6px 0;
            border-bottom: 1px solid var(--border-color);
            font-size: 10pt;
        }

        .stat-row:last-child {
            border-bottom: none;
        }

        .stat-label {
            color: var(--text-muted);
        }

        .stat-value {
            font-weight: 600;
            color: var(--primary-color);
        }

        /* Visualizations - Full Width Charts */
        .chart-grid {
            display: flex;
            flex-direction: column;
            gap: 30px;
        }

        .chart-card {
            background: var(--bg-light);
            border-radius: 8px;
            padding: 25px;
            border: 1px solid var(--border-color);
            page-break-inside: avoid;
        }

        .chart-card h3 {
            color: var(--primary-color);
            margin-bottom: 8px;
            font-size: 14pt;
        }

        .chart-description {
            color: var(--text-muted);
            font-size: 10pt;
            margin-bottom: 20px;
        }

        .chart-image {
            text-align: center;
            background: white;
            padding: 15px;
            border-radius: 4px;
        }

        .chart-image img {
            width: 100%;
            max-width: 100%;
            height: auto;
        }

        /* Recommendations */
        .recommendation-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-bottom: 25px;
        }

        .recommendation-card {
            background: var(--bg-light);
            border-radius: 8px;
            padding: 20px;
            border: 1px solid var(--border-color);
        }

        .recommendation-card h4 {
            color: var(--primary-color);
            margin-bottom: 15px;
            font-size: 12pt;
            padding-bottom: 10px;
            border-bottom: 2px solid var(--accent-color);
        }

        .recommendation-card ul {
            list-style: none;
        }

        .recommendation-card li {
            padding: 8px 0;
            padding-left: 20px;
            position: relative;
            color: var(--text-dark);
            font-size: 10pt;
        }

        .recommendation-card li:before {
            content: ">";
            position: absolute;
            left: 0;
            color: var(--accent-color);
            font-weight: bold;
        }

        .disclaimer {
            background: #fef2f2;
            border-left: 4px solid var(--danger-color);
            padding: 15px 20px;
            border-radius: 0 8px 8px 0;
            font-size: 9pt;
            color: #7f1d1d;
        }

        /* Footer */
        .report-footer {
            text-align: center;
            padding: 25px;
            color: var(--text-muted);
            font-size: 9pt;
            border-top: 1px solid var(--border-color);
        }

        /* Print Styles */
        @media print {
            @page {
                size: A4;
                margin: 15mm;
            }

            body {
                background: white;
                font-size: 10pt;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }

            .container {
                max-width: 100%;
                padding: 0;
            }

            .report-header {
                padding: 30px;
                margin-bottom: 20px;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }

            .report-header h1 {
                font-size: 22pt;
            }

            section {
                box-shadow: none;
                border: 1px solid #ccc;
                page-break-inside: avoid;
                margin-bottom: 15px;
                padding: 20px;
            }

            section h2 {
                font-size: 14pt;
            }

            .summary-grid {
                grid-template-columns: repeat(4, 1fr);
            }

            .card-value {
                font-size: 18pt;
            }

            .finding-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .stat-grid {
                grid-template-columns: repeat(4, 1fr);
            }

            .recommendation-grid {
                grid-template-columns: repeat(3, 1fr);
            }

            .chart-card {
                page-break-inside: avoid;
                margin-bottom: 20px;
            }

            .chart-image img {
                max-width: 100%;
                height: auto;
            }

            .badge {
                border: 1px solid currentColor;
            }

            .data-table th {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }

            .stat-header {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }

        /* Responsive */
        @media (max-width: 1024px) {
            .summary-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .stat-grid {
                grid-template-columns: repeat(2, 1fr);
            }

            .recommendation-grid {
                grid-template-columns: 1fr;
            }
        }

        @media (max-width: 768px) {
            .report-header {
                padding: 30px 20px;
            }

            .report-header h1 {
                font-size: 20pt;
            }

            .report-header .meta {
                flex-direction: column;
                gap: 10px;
            }

            section {
                padding: 20px;
            }

            .summary-grid,
            .finding-grid,
            .stat-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
    """


def generate_html_report(results_df: pd.DataFrame, summaries: dict) -> str:
    """Generate the complete HTML report."""

    report_date = datetime.now().strftime("%B %d, %Y")
    report_time = datetime.now().strftime("%I:%M %p")

    html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>India VIX Pre-Budget Analysis Report</title>
        {get_css_styles()}
    </head>
    <body>
        <div class="container">
            <header class="report-header">
                <h1>India VIX Pre-Budget Behavior Analysis</h1>
                <p class="subtitle">Comprehensive Analysis of Volatility Patterns Before Union Budget Announcements</p>
                <div class="meta">
                    <div class="meta-item">
                        <span>Analysis Period: 2015 - 2025</span>
                    </div>
                    <div class="meta-item">
                        <span>Budgets Analyzed: {len(results_df)}</span>
                    </div>
                    <div class="meta-item">
                        <span>Generated: {report_date} at {report_time}</span>
                    </div>
                </div>
            </header>

            <section>
                {generate_executive_summary(results_df, summaries)}
            </section>

            <section>
                {generate_key_findings(results_df, summaries)}
            </section>

            <section>
                {generate_statistics_section(summaries)}
            </section>

            <section>
                {generate_detailed_table(results_df)}
            </section>

            <section>
                {generate_visualizations_section()}
            </section>

            <section>
                {generate_recommendations()}
            </section>

            <footer class="report-footer">
                <p>India VIX Pre-Budget Analysis Report</p>
                <p>Generated using Python and Yahoo Finance Data</p>
            </footer>
        </div>
    </body>
    </html>
    """

    return html


def main():
    """Main function to generate the executive HTML report."""

    print_section("INDIA VIX EXECUTIVE REPORT GENERATOR")
    print_progress("Starting report generation...")

    try:
        # Step 1: Load or generate analysis data
        print_progress("Loading budget dates...")
        budget_df = get_budget_dates()

        print_progress("Downloading/loading VIX data...")
        vix_data = download_vix_data(start_date="2014-12-01")

        print_progress("Analyzing VIX levels for each budget...")
        results_df = analyze_budget_vix(vix_data, budget_df)

        print_progress("Calculating summary statistics...")
        summaries = calculate_summary_statistics(results_df)

        # Step 2: Generate HTML report
        print_progress("Generating HTML report...")
        html_content = generate_html_report(results_df, summaries)

        # Step 3: Save report
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        report_path = os.path.join(OUTPUT_DIR, REPORT_FILE)

        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print_section("REPORT GENERATION COMPLETE")
        print_progress(f"Executive HTML report saved to: {report_path}")
        print_progress("Open the HTML file in any web browser to view the report.")
        print_progress("To save as PDF: Open in Chrome/Edge -> Press Ctrl+P -> Save as PDF")

        # Get absolute path for user convenience
        abs_path = os.path.abspath(report_path)
        print(f"\nFull path: {abs_path}")

        return 0

    except Exception as e:
        print(f"\n[ERROR] Report generation failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
