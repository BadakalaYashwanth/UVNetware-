# AI-Driven Marketing Analytics Pipeline

This system analyzes raw marketing and user activity data and converts it into structured weekly, monthly, and yearly insights. It provides channel performance analysis, ROI optimization, anomaly detection, and budget recommendations to support data-driven marketing decisions.

## Features
- **Data Processing & Feature Engineering**: Robust pipelines to clean and transform raw marketing and user activity data.
- **Channel Performance Analysis**: Evaluates which channels are driving the most value.
- **ROI Optimization**: Models past performance to optimize future spend.
- **Anomaly Detection**: Identifies unusual spikes or drops in traffic and conversion rates.
- **Budget Recommendations**: Data-driven, automated budget allocation suggestions.

## Technology Stack & Machine Learning Algorithms

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

## Project Structure
```
├── data/
│   ├── raw/               # Immutable original data
│   └── processed/         # Cleaned, finalized data sets for modeling
├── notebooks/             # Jupyter notebooks for exploration and prototyping
├── src/
│   ├── data_processing/   # Scripts to fetch and clean data
│   ├── features/          # Feature engineering logic
│   ├── models/            # Anomaly, ROI, and budget recommendation models
│   ├── insights/          # Scripts to generate weekly/monthly/yearly reports
│   └── utils/             # Helper functions and configurations
├── tests/                 # Unit tests for the pipeline
├── requirements.txt       # Project dependencies
└── main.py                # Main entry point to run the pipeline
```

## How to Run the Project

Follow these steps to execute the pipeline on your machine:

1. **Open your Terminal (Command Prompt or PowerShell)**
   Navigate into the project directory:
   ```powershell
   cd "C:\Users\ASUS\OneDrive\Desktop\Saas Application"
   ```

2. **Install the Required Libraries**
   Install all the ML models and data processing engines we defined:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Pipeline**
   Execute the master orchestration file. This will automatically generate the 5,000 rows of mock data, run the feature engineering, predict the anomalies, and bundle the Insights:
   ```powershell
   python main.py
   ```

4. **View the Results**
   Once the execution completes (it only takes seconds), open the newly generated `output_insights.json` file in your editor to see the fully structured API payload!
