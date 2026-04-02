# AI Marketing Analytics Pipeline - Implementation Plan

This document tracks the formal development phases for the analytics layer.

## ✅ Phase 1: Data Processing + Aggregation
- **Handle missing values and invalid data**: Handled in `src/data_processing/preprocessing.py`, securely capturing missing and negative edge-cases via Numpy and Pandas `.fillna()`.
- **Convert timestamp into week, month, year**: Processed within `clean_and_preprocess()`, isolating distinct time buckets.
- **Aggregate metrics (clicks, revenue, conversions)**: Configured in `src/features/feature_engineering.py` via `aggregate_insights()`, utilizing dynamic time resampling.
- **Generate basic summaries**: Built successfully inside `src/insights/generate_report.py`, wrapping aggregated DataFrames into pristine JSON properties.

## ✅ Phase 2: Feature Engineering (COMPLETED)
- **CTR**: Calculated strictly as `clicks / impressions`.
- **Conversion Rate**: Extracted via `conversions / clicks`.
- **ROI**: Implemented as the raw ratio `(revenue - cost) / cost`.
- **Cost per Conversion**: Calculated via `cost / conversions`.
- **Engagement Score**: Computed using multi-variate formula `session_duration × clicks × (1 - bounce_rate)`.

## ✅ Phase 3: Core Analytics (COMPLETED)
- **Channel performance ranking**: Achieved inside `channel_performance()` by automatically ranking descending outputs via `.sort_values(by='roi', ascending=False)`. Best and worst dynamically load into JSON mapping.
- **Trend analysis**: Added period-over-period `.pct_change()` calculations inside `aggregate_insights()` tracking growth vectors for revenue, clicks, conversions, and cost across `weekly`, `monthly`, and `yearly` datasets.

## ✅ Phase 4: Machine Learning Models (COMPLETED)
- **ROI Prediction**: Scaffolding instantiated using `XGBoost`. Calculates loss algorithms efficiently and explicitly returns mapped `feature_importances_` to isolate drivers of revenue.
- **Anomaly Detection**: Configured `Scikit-Learn IsolationForest` formally tuned to scrutinize `impressions`, `clicks`, and `conversion_rates` explicitly for drop-offs.
- **User Segmentation**: Added new KMeans model inside `user_segmentation.py` that normalizes and clusters unique `user_id` aggregates into grouped `engagement profiles`.
- **Pipeline Injection**: Successfully orchestrated `main.py` and `generate_report.py` to nest these predictive metrics into the standardized `"ml_insights"` json dictionary.

## ✅ Phase 5: Budget Optimization (COMPLETED)
- **Allocation logic**: Adjusted `recommend_budget()` to calculate a proportional distribution scalar derived fundamentally from normalized ROI pools.
- **Spend adjustments**: Created an explicit mathematical constraint forcing a minimum `0.05` allocation base weight, while explicitly shifting capital away from negative ROI channels to dynamically increase high ROI channel caps.
- **Actionable reporting**: Added precise new nodes for `"optimization_action"` (Increase/Decrease/Maintain) and `"adjustment_amount"` inside the final JSON output payload mapping `historic_cost` vs `recommended_cost`.

## ✅ Phase 6: Insight Generation (COMPLETED)
- **Identify top-performing channels**: Safely extrapolated within `generate_report.py`, locking the literal best/worst channels as dashboard header metrics.
- **Detect anomalies and explain causes**: Re-engineered `anomaly_detection.py` to evaluate the row data that flagged the IsolationForest, mapping explicit textual tags like `"Zero conversions despite traffic"` or `"Unusually high cost"` against historical dataset means.
- **Generate actionable recommendations**: Formalized an `'executive_summary'` node in the structural JSON payload that parses the math into direct executive actions (e.g. "Double down on [X]", "Reduce spend on [Y]").

## 🛠️ Technology Stack & Machine Learning Algorithms

### Language & Core Tech Stack

| Name | Purpose | Where did you use and how does it work | Output of the work |
| :--- | :--- | :--- | :--- |
| **Python** | Core Programming Language | Acts as the foundational backend language running the entire pipeline via `main.py` and the `src/` modular filesystem. | The executable `.py` scripts and data logic powering your application. |

### Project Libraries & Dependencies

| Name | Purpose | Where did you use and how does it work | Output of the work |
| :--- | :--- | :--- | :--- |
| **Pandas** | Data Manipulation & Processing | Heavily used spanning across `preprocessing.py`, `feature_engineering.py`, and all machine learning scripts. It loads the core JSON data and handles tabular aggregation and manipulation. | Cleaned robust `.DataFrame` structures used extensively to pipe data across the program. |
| **NumPy** | Numerical Operations | Used within `advanced_roi_prediction.py` to efficiently map mathematical array conditionals (like division computations for conditional ROI forecasting). | Optimized arrays and numerical output calculations. |
| **Scikit-learn** *(sklearn)* | Foundational Machine Learning Toolset | Imported in `anomaly_detection.py` and `user_segmentation.py`. Provides the standardized implementations for clustering algorithms, anomaly detection, and data scalers (like `StandardScaler`). | Structured clustering mappings and standardized analytical models. |
| **XGBoost** | High-Performance Predictive Modeling | Imported in `advanced_roi_prediction.py` to deploy advanced gradient-boosted decision trees for regression and continuous feature analysis. | Heavily optimized models mapping dataset behaviors. |
| **Matplotlib, Seaborn, Plotly** *(v5.18.0)* | Data Visualization Tools | Available in `requirements.txt` to power visualization tools, visual graph generation, and potentially connecting with front-end analytical dashboards. | Front-end readable charts, plots, and graphical interfaces. |
| **SciPy, StatsModels** | Advanced Statistical Analysis | Listed within the project's dependencies to assist in calculating deep statistical distributions, variations, and advanced descriptive statistics. | Statistical arrays and hypothesis validation outputs. |

### Machine Learning Algorithms & Custom Engine Logic

| Name | Purpose | Where did you use and how does it work | Output of the work |
| :--- | :--- | :--- | :--- |
| **KMeans Clustering** *(via Scikit-learn)* | User Behavioral Segmentation | **Where**: `src/models/user_segmentation.py`<br><br>**How it works**: Aggregates data by user and runs it through a `StandardScaler`. It maps behaviors using features like `revenue`, `clicks`, `session_duration`, and `conversions` to cluster and identify high-value vs. bargain shopper groups. | Maps each `user_id` to a unique `segment_id` identifying their behavioral profile, and provides a dashboard-ready data object of segment traits. |
| **XGBoost Regressor** *(XGBRegressor)* | ROI & Future Revenue Prediction | **Where**: `src/models/advanced_roi_prediction.py`<br><br>**How it works**: Deploys a regression decision tree (`reg:squarederror`) leveraging historical spend attributes (`impressions`, `clicks`, `cost`, `session_duration`). Evaluated securely via Mean Squared Error (MSE). | A `predicted_revenue` numeric mapping output, derived predictive ROI, and an extracted `feature_importances` dictionary detailing exactly what drives revenue. |
| **Isolation Forest** *(via Scikit-learn)* | Anomaly & Outlier Detection | **Where**: `src/models/anomaly_detection.py`<br><br>**How it works**: Fits an Isolation Forest model to detect unusual dataset volume spikes or erratic events, assuming roughly a 5% data contamination rate (`contamination=0.05`). | Appends an `is_anomaly` boolean flag onto operations, an `anomaly_score`, and explicitly computes a contextual `anomaly_reason` string. |
| **ROI Weighting Mathematical Algorithm** *(Custom)* | Dynamic Budget Optimization | **Where**: `src/models/budget_recommendation.py`<br><br>**How it works**: Analyzes historical `ROI` distributions across channels. It computes proportional allocations algorithmically with a custom baseline safety net to ensure smaller experimental channels aren't starved completely. | A DataFrame dictating a specific `recommended_budget`, numerical `adjustment_amount`, and programmatic text actions (e.g., *"Increase Spend (High ROI)"*). |

## 📂 How the Code Works (File Execution Order)

Here is a simple explanation of exactly what every file does in the project, in the exact order they run:

1. `requirements.txt`: Before anything runs, this file tells your computer exactly which outside tools (like Pandas or XGBoost) it needs to install to work.
2. `src/data_processing/generate_mock_data.py`: If we don't have real customer data plugged in, this script automatically creates realistic fake data so the project doesn't break.
3. `src/data_processing/preprocessing.py`: Once we have data, this file cleans it up. It fixes empty blank spaces and organizes all the random dates into neat weeks, months, and years.
4. `src/features/feature_engineering.py`: This script does the core math. It takes the clean data and calculates important numbers like ROI (Return on Investment) and CTR (Click-Through Rate).
5. `src/models/anomaly_detection.py`: This file acts like a security guard. It looks at the data and flags any weird behavior (like sudden drops in sales or random traffic spikes) as an "anomaly".
6. `src/models/user_segmentation.py`: This groups our users into different buckets (like "High Value" vs. "Bargain Shoppers") based on how they interact with our platform.
7. `src/models/advanced_roi_prediction.py`: The "fortune teller." It looks at how much money we've spent in the past to predict how much revenue we will make in the future.
8. `src/models/budget_recommendation.py`: The financial advisor. It looks at the data and tells us exactly which marketing channels we should spend more money on, and which ones we should cut.
9. `src/insights/generate_report.py`: The summarizing reporter. It takes all the complicated math, findings, and predictions from the previous steps and bundles them into one simple, clean digital report.
10. `main.py`: The boss. It is the file you actually run. It triggers all the steps above automatically, completely in order, and then spits out the final `output_insights.json` payload!
