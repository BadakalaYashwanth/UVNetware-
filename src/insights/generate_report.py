import json
import pandas as pd
import numpy as np

class DefaultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        else:
            return super(DefaultEncoder, self).default(obj)

def generate_json_report(enriched_df: pd.DataFrame, chan_perf: pd.DataFrame, anomalies_df: pd.DataFrame, budget_recs: pd.DataFrame, importance_dict: dict = None, segment_profiles: dict = None) -> dict:
    """
    Constructs the final JSON output structure based exactly on the requested target schema.
    """
    
    # 1. Summaries
    def get_concise_summary(df, freq):
        from src.features.feature_engineering import aggregate_insights
        agg_df = aggregate_insights(df, frequency=freq)
        if agg_df.empty: return {}
        
        latest = agg_df.iloc[-1]
        
        # Format growth rate to match target '+12%'
        growth = latest.get('revenue_growth', 0.0) * 100
        growth_str = f"+{growth:.0f}%" if growth >= 0 else f"{growth:.0f}%"
        
        return {
            "total_clicks": int(latest.get('clicks', 0)),
            "total_revenue": float(latest.get('revenue', 0)),
            "growth_rate": growth_str
        }

    weekly_summary = get_concise_summary(enriched_df, 'W')
    monthly_summary = get_concise_summary(enriched_df, 'ME')
    yearly_summary = get_concise_summary(enriched_df, 'YE')
    
    # 2. Channel Performance
    chan_perf_formatted = []
    for _, row in chan_perf.iterrows():
        chan_perf_formatted.append({
            "channel": row['channel'],
            "ROI": float(row.get('roi', 0.0))
        })
        
    # 3. ROI Insights (extract top ML feature importances)
    top_factors = []
    if importance_dict:
        # sort factors by highest importance value
        sorted_factors = sorted(importance_dict.items(), key=lambda item: item[1], reverse=True)
        top_factors = [k for k, v in sorted_factors][:2] # Take top 2
        
    roi_insights = {
        "top_factors": top_factors
    }
    
    # 4. Budget Recommendations (bucket channels by optimization action)
    increase_list = []
    decrease_list = []
    for _, row in budget_recs.iterrows():
        action = row.get('optimization_action', '')
        if "Increase" in action:
            increase_list.append(row['channel'])
        elif "Reduce" in action:
            decrease_list.append(row['channel'])
            
    budget_recommendations = {
        "increase": increase_list,
        "decrease": decrease_list
    }
    
    # 5. Anomalies (extract descriptive string summaries)
    anomalies_only = anomalies_df[anomalies_df['is_anomaly'] == True]
    anomalies_formatted = []
    for _, row in anomalies_only.iterrows():
        reason = row.get('anomaly_reason', 'unknown cause')
        channel = row.get('channel', 'Unknown channel')
        # Extract day of the week if timestamp available
        date_str = pd.to_datetime(row['timestamp']).strftime('%A') if 'timestamp' in row else 'recently'
        
        # Target format: "Traffic dropped on Tuesday due to high bounce rate"
        anomalies_formatted.append(f"Flags raised for {channel} on {date_str} due to: {reason.lower()}")

    # Output structure exactly matching user schema requested (maintaining M/Y variants for completion)
    output_structure = {
        "weekly_summary": weekly_summary,
        "monthly_summary": monthly_summary,
        "yearly_summary": yearly_summary,
        "channel_performance": chan_perf_formatted,
        "roi_insights": roi_insights,
        "budget_recommendations": budget_recommendations,
        "anomalies": anomalies_formatted[:10] # limit to top 10 string outputs
    }
    
    return json.loads(json.dumps(output_structure, cls=DefaultEncoder))
