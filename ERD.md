# LAB-08: ERD for Daily Stock Gainer List Analysis

## Overview

This ERD models how automated data collected from Yahoo Finance and Wall Street Journal gainers lists is transformed into unified, intermediate, and final tables for analysis. Data is scraped and saved multiple times daily using cron jobs and Python scripts. Additional historical data per symbol (candlestick format) is also included for future trend analysis.

The goal is to enable insights such as identifying recurring stock symbols, analyzing price distributions, and summarizing volume trends for stakeholder reporting.

## Use Cases

- **Recurring Stocks**: Detect which symbols appear most often across multiple days and times.
- **Daily Summaries**: Calculate average, minimum, and maximum price and volume data per trading day.
- **Cross-Source Comparison**: Compare gainers reported by Yahoo vs WSJ.
- **Intra-day Trend Tracking**: Understand how gainers change from morning to afternoon.
- **Symbol Volatility Insight**: Determine which stocks show highest % change repeatedly.
- **Candlestick Trend Analysis**: Leverage open/high/low/close data to detect momentum patterns.

## Methods

The data pipeline begins with automated collection and ends in analytics-ready tables.

1. **Raw Collection**:
   - `collect_gainers.py` is run by `run_collection.sh` and scheduled via cron to pull data from Yahoo and WSJ throughout the day.
   - Files are saved in `data/yahoo/` and `data/wsj/` with timestamped filenames.
   - Candlestick data is pulled separately as historical CSVs for each stock and stored in `CANDLESTICK_RAW`.

2. **Normalization**:
   - Source formats differ slightly. `normalize_csv.py` standardizes all fields (e.g., percent change, price, volume) across sources.

3. **Merging**:
   - `merge_csvs.py` combines Yahoo and WSJ data into one dataset called `COMBINED_GAINERS`.
   - A `source` column is added to track origin (Yahoo or WSJ).

4. **Intermediate and Final Tables**:
   - `SYMBOL_RECURRENCE` is created to identify how frequently a symbol appears across dates.
   - `DAILY_STATS` summarizes price and volume metrics by date.
   - `CANDLESTICK_RAW` is currently not summarized into a final table, but included in the ERD for future trend-based analysis.

These tables are used to create visualizations, reports, or further analysis in DBT and Snowflake in later labs.

## Summary

This ERD captures the full data flow from raw collection to analysis-ready tables, covering all critical stages of the data pipeline. The model includes the ingestion of multiple daily CSVs from both Yahoo Finance and the Wall Street Journal, automated via scheduled scripts, and tracks how this data is cleaned, normalized, merged, and ultimately summarized for analytical use.

We focused on key business questions such as:
- Which stock symbols appear most frequently over the week?
- What are the average, minimum, and maximum prices and volumes per day?
- How do gainer lists from Yahoo and WSJ differ?

The current ERD is also forward-compatible. We’ve incorporated a `CANDLESTICK_RAW` table for future trend analysis based on open/high/low/close data. While this raw table isnt transformed into summaries(not provided yet), it sets the foundation for upcoming labs where we will integrate more technical indicators or perform pattern analysis (e.g., volatility tracking, correlation with gainers, etc.).

The data model is designed to be easily extensible. With minor additions, it could support sector-based analysis, moving averages, correlation between stocks, or even integration with external sources like news sentiment or earnings reports. These would enable richer visualizations and deeper insights for both technical and non-technical stakeholders.

In its current form, the ERD achieves the core goal of the lab(08): to build a structure that transforms raw stock gainer data into meaningful, queryable formats for downstream exploration, storytelling, and business intelligence.


## Mermaid ERD

```mermaid
erDiagram
    YAHOO_GAINERS_RAW {
        string symbol
        string name
        float price
        string change
        string percent_change
        date date
    }

    WSJ_GAINERS_RAW {
        string symbol
        string company
        int volume
        float price
        float change
        float percent_change
        date date
    }

    COMBINED_GAINERS {
        string symbol
        string name
        float price
        float change
        float percent_change
        int volume
        string source
        date date
    }

    SYMBOL_RECURRENCE {
        string symbol
        int count_days_appeared
        date first_appearance
        date last_appearance
    }

    DAILY_STATS {
        date date
        float avg_price
        float min_price
        float max_price
        float avg_change
        float avg_percent_change
        int total_volume
    }

    CANDLESTICK_RAW {
        string symbol
        date date
        float open
        float high
        float low
        float close
        int volume
    }

    YAHOO_GAINERS_RAW ||--o{ COMBINED_GAINERS : feeds
    WSJ_GAINERS_RAW   ||--o{ COMBINED_GAINERS : feeds
    COMBINED_GAINERS  ||--o{ SYMBOL_RECURRENCE : generates
    COMBINED_GAINERS  ||--o{ DAILY_STATS : summarizes
    CANDLESTICK_RAW   ||--o{ COMBINED_GAINERS : supplements
