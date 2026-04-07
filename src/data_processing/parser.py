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
                "converted": session.get("converted", False),
                # New session fields
                "entryPage": session.get("entryPage"),
                "exitPage": session.get("exitPage"),
                "referrer": session.get("referrer"),
                "cartValue": session.get("cartValue", 0.0),
                "checkoutStarted": session.get("checkoutStarted", False),
                "paymentCompleted": session.get("paymentCompleted", False),
                "userType": session.get("userType"),
                "loyaltyScore": session.get("loyaltyScore")
            }
            
            # Root level fields
            base_record["avg_order_value_root"] = data.get("avg_order_value")
            base_record["currency"] = data.get("currency")
            base_record["transaction_id"] = data.get("transaction_id")

            # Meta fields
            meta = data.get("meta", {})
            base_record["country"] = meta.get("geoLocation", {}).get("country")
            base_record["city"] = meta.get("geoLocation", {}).get("city")
            base_record["deviceType"] = meta.get("deviceType")
            base_record["os"] = meta.get("os")
            base_record["browser"] = meta.get("browser")

            # Marketing Metrics
            metrics = data.get("marketingMetrics", {})
            base_record["impressions"] = metrics.get("impressions", 0)
            base_record["clicks"] = metrics.get("clicks", 0)
            base_record["conversions"] = metrics.get("conversions", 0)
            base_record["cost"] = metrics.get("cost", 0)
            base_record["revenue"] = metrics.get("revenue", 0)
            base_record["cpc_input"] = metrics.get("cpc")
            base_record["cpm_input"] = metrics.get("cpm")

            # User History
            history = data.get("userHistory", {})
            base_record["history_totalSessions"] = history.get("totalSessions")
            base_record["history_totalRevenue"] = history.get("totalRevenue")
            base_record["history_avgOrderValue"] = history.get("avgOrderValue")
            base_record["history_lastActiveDays"] = history.get("lastActiveDays")

            # Funnel (take only siteId for now, conversion/dropoff might be arrays)
            funnel = data.get("ai_input", {}).get("funnel", {})
            base_record["funnel_conversionRates"] = funnel.get("conversionRates")
            base_record["funnel_dropOffRates"] = funnel.get("dropOffRates")
            
            records.append(base_record)
            
    # If no sessions found but we have top level metrics
    if not records and "marketingMetrics" in data:
        metrics = data.get("marketingMetrics", {})
        agg = data.get("aggregated", {})
        meta = data.get("meta", {})
        
        record = {
            "user_id": meta.get("userId", "unknown"),
            "timestamp": meta.get("timestamp"),
            "channel": meta.get("channel", "unknown"),
            "campaign_id": meta.get("campaign_id", "none"),
            "impressions": metrics.get("impressions", 0),
            "clicks": metrics.get("clicks", 0),
            "conversions": metrics.get("conversions", 0),
            "cost": metrics.get("cost", 0),
            "revenue": metrics.get("revenue", 0),
            "session_duration": agg.get("traffic", {}).get("avgSessionTime", 0) * 60, # convert min to sec
            "bounce_rate": agg.get("sessionInsights", {}).get("bounceRate", 0),
            # New fields for agg fallback
            "country": meta.get("geoLocation", {}).get("country"),
            "city": meta.get("geoLocation", {}).get("city"),
            "deviceType": meta.get("deviceType"),
            "os": meta.get("os"),
            "browser": meta.get("browser"),
            "newUsers": agg.get("traffic", {}).get("newUsers"),
            "returningUsers": agg.get("traffic", {}).get("returningUsers"),
            "exitRate": agg.get("sessionInsights", {}).get("exitRate")
        }
        records.append(record)
        
    return pd.DataFrame(records)
