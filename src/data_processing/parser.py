import pandas as pd
import json

def parse_real_world_data(json_data):
    """
    Parses the new real-world JSON structure into a flattened format
    compatible with the existing pipeline as much as possible.
    """
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
        
    records = []
    
    # 1. Flatten the ai_input.sessions structure
    if "ai_input" in data and "sessions" in data["ai_input"]:
        for session in data["ai_input"]["sessions"]:
            base_record = {
                "user_id": session.get("visitorId"),
                "timestamp": session.get("createdAt"),
                "channel": session.get("source", "unknown"),
                "campaign_id": data.get("meta", {}).get("campaign_id", "none"),
                "session_duration": session.get("session_duration"),
                "bounce_rate": session.get("bounce_rate"),
                "device": session.get("device"),
                "converted": session.get("converted", False)
            }
            
            # The metrics at top level can be distributed to these session records
            # Or we can treat them as aggregated metrics.
            # To keep it compatible with existing pipeline, we add them to the record.
            metrics = data.get("marketingMetrics", {})
            base_record["impressions"] = metrics.get("impressions", 0)
            base_record["clicks"] = metrics.get("clicks", 0)
            base_record["conversions"] = metrics.get("conversions", 0)
            base_record["cost"] = metrics.get("cost", 0)
            base_record["revenue"] = metrics.get("revenue", 0)
            
            records.append(base_record)
            
    # If no sessions found but we have top level metrics
    if not records and "marketingMetrics" in data:
        metrics = data.get("marketingMetrics", {})
        record = {
            "user_id": data.get("meta", {}).get("userId", "unknown"),
            "timestamp": data.get("meta", {}).get("timestamp"),
            "channel": data.get("meta", {}).get("channel", "unknown"),
            "campaign_id": data.get("meta", {}).get("campaign_id", "none"),
            "impressions": metrics.get("impressions", 0),
            "clicks": metrics.get("clicks", 0),
            "conversions": metrics.get("conversions", 0),
            "cost": metrics.get("cost", 0),
            "revenue": metrics.get("revenue", 0),
            "session_duration": data.get("aggregated", {}).get("traffic", {}).get("avgSessionTime", 0) * 60, # convert min to sec
            "bounce_rate": data.get("aggregated", {}).get("sessionInsights", {}).get("bounceRate", 0)
        }
        records.append(record)
        
    return pd.DataFrame(records)
