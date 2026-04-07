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

def generate_json_report(enriched_df: pd.DataFrame, chan_perf: pd.DataFrame, anomalies_df: pd.DataFrame, budget_recs: pd.DataFrame, importance_dict: dict = None, segment_profiles: dict = None, input_summary: dict = None) -> dict:
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
            "growth_rate": growth_str,
            "avg_order_value": float(latest.get('avg_order_value_root', 0.0)) if 'avg_order_value_root' in latest else 0.0
        }

    weekly_summary = get_concise_summary(enriched_df, 'W')
    monthly_summary = get_concise_summary(enriched_df, 'ME')
    yearly_summary = get_concise_summary(enriched_df, 'YE')
    
    # 2. Channel Performance
    chan_perf_formatted = []
    for _, row in chan_perf.iterrows():
        chan_perf_formatted.append({
            "channel": row['channel'],
            "ROI": float(row.get('roi', 0.0)),
            "CPC": float(row.get('cpc', 0.0)),
            "CPM": float(row.get('cpm', 0.0))
        })
        
    # 3. ROI Insights (extract top ML feature importances)
    top_factors = []
    if importance_dict:
        sorted_factors = sorted(importance_dict.items(), key=lambda item: item[1], reverse=True)
        top_factors = [k for k, v in sorted_factors][:3] 
        
    roi_insights = {
        "top_factors": top_factors,
        "key_drivers": ["Device Type", "Geo Location", "User History"]
    }
    
    # 4. Budget Recommendations
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
    
    # 5. User Behavior & Device/Geo Insights
    user_behavior = {
        "top_devices": enriched_df['deviceType'].value_counts().to_dict() if 'deviceType' in enriched_df.columns else {},
        "top_os": enriched_df['os'].value_counts().to_dict() if 'os' in enriched_df.columns else {},
        "user_types": enriched_df['userType'].value_counts().to_dict() if 'userType' in enriched_df.columns else {},
        "geo_distribution": enriched_df['country'].value_counts().to_dict() if 'country' in enriched_df.columns else {}
    }
    
    # 6. Funnel Analysis
    funnel_analysis = {}
    if 'funnel_conversionRates' in enriched_df.columns:
        rates = enriched_df['funnel_conversionRates'].iloc[0]
        drops = enriched_df['funnel_dropOffRates'].iloc[0]
        funnel_analysis = {
            "avg_conversion_rates": rates,
            "avg_drop_off_rates": drops,
            "bottleneck_step": "Step 3" if len(drops) > 2 and drops[2] > 0.4 else "None"
        }

    # 7. User History Metrics
    history_metrics = {
        "avg_total_sessions": float(enriched_df['history_totalSessions'].mean()) if 'history_totalSessions' in enriched_df.columns else 0.0,
        "avg_total_revenue": float(enriched_df['history_totalRevenue'].mean()) if 'history_totalRevenue' in enriched_df.columns else 0.0,
        "loyalty_engagement_score": float(enriched_df['loyaltyScore'].mean()) if 'loyaltyScore' in enriched_df.columns else 0.0
    }

    # 8. Anomalies
    anomalies_only = anomalies_df[anomalies_df['is_anomaly'] == True]
    anomalies_formatted = []
    for _, row in anomalies_only.iterrows():
        reason = row.get('anomaly_reason', 'unknown cause')
        channel = row.get('channel', 'Unknown channel')
        date_str = pd.to_datetime(row['timestamp']).strftime('%A') if 'timestamp' in row else 'recently'
        anomalies_formatted.append(f"Flags raised for {channel} on {date_str} due to: {reason.lower()}")

    # Output structure
    output_structure = {
        "weekly_summary": weekly_summary,
        "monthly_summary": monthly_summary,
        "yearly_summary": yearly_summary,
        "channel_performance": chan_perf_formatted,
        "roi_insights": roi_insights,
        "budget_recommendations": budget_recommendations,
        "user_behavior_insights": user_behavior,
        "funnel_analytics": funnel_analytics,
        "geo_insights": user_behavior["geo_distribution"],
        "user_history_metrics": history_metrics,
        "anomalies": anomalies_formatted[:10],
        "executive_summary": input_summary if input_summary else "N/A"
    }
    
    return json.loads(json.dumps(output_structure, cls=DefaultEncoder))
