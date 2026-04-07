# AI-Driven Advanced Marketing Analytics System 🚀

This system is an evolved analytics pipeline that transforms raw multi-channel marketing data and granular user activity into structured, high-level business intelligence. It provides automated weekly, monthly, and yearly insights, including ROI optimization, behavioral segmentation, and predictive budget recommendations.

---

## 🌟 Advanced System Evolution
The project has evolved from a basic tracking tool into an **Intelligent Analytics Engine**, now supporting complex e-commerce and behavioral data points.

### 🆕 New Capabilities Added:
- **Funnel Drop-off Analysis**: Automatically identifies bottlenecks in the conversion journey.
- **Geo-Behavioral Insights**: Tracks performance and user trends by country and city.
- **Loyalty & History Metrics**: Analyzes long-term user value using historical session and revenue data.
- **Advanced E-commerce Tracking**: Integrated support for `avg_order_value`, `cartValue`, and transaction-level details.
- **Device & OS Intelligence**: Granular breakdown of technical user profiles to optimize multi-platform strategies.

---

## 📊 Data Input Schema

The system now supports an extended JSON input structure (`real_world_input.json`):

### **Legacy Inputs (Maintained)**
- `meta`: userId, siteId, timestamp, channel, campaign_id.
- `marketingMetrics`: impressions, clicks, conversions, cost, revenue.
- `aggregated`: totalSessions, avgSessionTime, bounceRate, topPages.

### **New Advanced Inputs**
- **Root Level**: `avg_order_value`, `currency`, `transaction_id`.
- **Granular Meta**: `geoLocation` (country, city), `deviceType`, `os`, `browser`.
- **marketingMetrics**: `cpc` (manual input), `cpm` (manual input).
- **Advanced Aggregations**: `newUsers`, `returningUsers`, `exitRate` (per page/session).
- **AI Session Data**: `entryPage`, `exitPage`, `referrer`, `cartValue`, `checkoutStarted`, `paymentCompleted`.
- **User Intelligence**: `userType` (new/returning), `loyaltyScore`.
- **Funnel Intelligence**: `conversionRates` and `dropOffRates` per step.
- **User History**: `totalSessions`, `totalRevenue`, `avgOrderValue` (lifetime).

---

## 🛠️ Technology Stack

| Name | Purpose | Implementation |
| :--- | :--- | :--- |
| **Python** | Core Backend | Orchestrates the entire pipeline via `main.py`. |
| **Pandas** | Data Processing | Handles complex JSON parsing, flattening, and aggregation. |
| **XGBoost** | Predictive Modeling | Predicts ROI and identifies key revenue drivers. |
| **Scikit-learn** | ML Algorithms | Powers `Isolation Forest` (Anomalies) and `KMeans` (Segmentation). |
| **NumPy** | Numeric Logic | Performs high-speed vector calculations for ROI and growth rates. |

---

## 📁 Project Structure
```
├── data/
│   └── raw/               # input: real_world_input.json
├── src/
│   ├── data_processing/   # parser.py (Updated to handle new schema)
│   ├── features/          # feature_engineering.py (Advanced e-commerce logic)
│   ├── models/            # Anomaly & Budget models
│   └── insights/          # generate_report.py (Produces unified output)
├── main.py                # Pipeline orchestrator
└── output_insights.json   # Unified JSON Insights Output
```

---

## 🚀 How to Run

1. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Prepare Input**:
   Ensure `data/raw/real_world_input.json` is populated with your latest marketing/session data.

3. **Execute Pipeline**:
   ```powershell
   python main.py
   ```

4. **Review Insights**:
   Open `output_insights.json` for a comprehensive breakdown of your marketing performance, user behavior, and automated recommendations.

---

## 🏁 Final Expectation
The system successfully bridges the gap between **Basic Analytics** and **Advanced Intelligent Intelligence**, reflecting real-world business complexities in a unified, API-ready JSON format.
