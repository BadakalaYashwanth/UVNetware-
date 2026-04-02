# System Architecture: AI Marketing Analytics Pipeline

## System Context
The core system receives raw marketing and user activity data from client applications, processes it via a Python-based ML layer, and generates structured algorithmic insights for executive decision-making.

**Final Data Flow Hierarchy:**
`Client App → JSON API → Database → Python Processing → ML Models → Insights JSON → Dashboard`

## Pipeline Workflow

### Step 1: Data Retrieval
The Python pipeline simulates data ingestion representing raw JSON payloads (e.g. from MongoDB or direct API pipelines) containing unstructured tracking and event logs.

### Step 2: Data Preprocessing
- Converts JSON payloads into robust structured data arrays (DataFrames).
- Handles missing scalars and sanitizes invalid vectors.
- Standardizes data types.
- Extracts explicit chronological components (Week, Month, Year mappings).

### Step 3: Time-Based Aggregation
Groups discrete events into macro weekly, monthly, and yearly levels and calculates overarching summation layers for impressions, clicks, conversions, cost, and revenue.

### Step 4: Feature Engineering
Calculates specific optimization ratios:
- **CTR** = `clicks / impressions`
- **Conversion Rate** = `conversions / clicks`
- **ROI** = `(revenue - cost) / cost`
- **Cost per Conversion** = `cost / conversions`
- **Engagement Score** = `session_duration * clicks * (1 - bounce_rate)`

### Step 5: Channel Performance Analysis
Slices holistic data back down to the target marketing channels and ranks them rigorously by their yielded ROI and Conversions.

### Step 6: Machine Learning Processing
1. **Regression Model (XGBoost)** trains inherently mapping feature weights against predicted revenue outcomes.
2. **Anomaly Detection (Isolation Forest)** evaluates multivariate anomalies flagging irregular traffic or unpredicted conversion drop-offs.
3. **User Segmentation (KMeans)** aggregates distinct user archetypes modeling engagement properties.

### Step 7: Budget Optimization
Compares raw historical spend vs calculated dynamic capital pools recommending aggressive injection into top-ROI vectors, and siphoning spend away from underperformers.

### Step 8: Insight Generation
Produces a localized `output_insights.json` payload perfectly mirroring the target Dashboard schema required by the Front-End. 

**Final Output Target Schema:**
```json
{
  "weekly_summary": {...},
  "monthly_summary": {...},
  "yearly_summary": {...},
  "channel_performance": [...],
  "roi_insights": {...},
  "budget_recommendations": {...},
  "anomalies": [...]
}
```
