import pandas as pd
import numpy as np

def enrich_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds engineered features like ROI, Conversion Rate, CTR, and Engagement Score to the dataset.
    """
    df = df.copy()
    
    # ROI: (Revenue - Cost) / Cost
    df['roi'] = np.where(df['cost'] > 0, 
                         (df['revenue'] - df['cost']) / df['cost'], 
                         0.0) # Adjusted per Phase 2 explicit formula. If cost is 0, keeping 0.0 placeholder.
    
    # Conversion Rate (Conversions / Clicks)
    df['conversion_rate'] = np.where(df['clicks'] > 0, df['conversions'] / df['clicks'], 0.0)
    
    # Cost Per Click (CPC)
    df['cpc'] = np.where(df['clicks'] > 0, df['cost'] / df['clicks'], 0.0)
    
    # Cost per Conversion (cost / conversions)
    df['cost_per_conversion'] = np.where(df['conversions'] > 0, df['cost'] / df['conversions'], 0.0)
    
    # Click-Through Rate (CTR) (clicks / impressions)
    df['ctr'] = np.where(df['impressions'] > 0, df['clicks'] / df['impressions'], 0.0)
    
    # Engagement Score: session_duration × clicks × (1 - bounce_rate)
    # Ensure columns exist before calculating
    if all(col in df.columns for col in ['session_duration', 'clicks', 'bounce_rate']):
        df['engagement_score'] = df['session_duration'] * df['clicks'] * (1 - df['bounce_rate'])
    else:
        df['engagement_score'] = 0.0
    
    # Extract date components for aggregation only if timestamp exists
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['date'] = df['timestamp'].dt.date
        try:
            df['year_month'] = df['timestamp'].dt.to_period('M')
        except ValueError:
            df['year_month'] = df['timestamp'].dt.to_period('ME')
            
        df['week'] = df['timestamp'].dt.isocalendar().week
    
    return df

def aggregate_insights(df: pd.DataFrame, frequency='W') -> pd.DataFrame:
    """
    Aggregates data by specific frequency and calculates period-over-period growth trends.
    W: Weekly, M: Monthly, Y: Yearly
    """
    # Resample by frequency based on timestamp
    df_time = df.set_index('timestamp')
    agg_funcs = {
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum',
        'session_duration': 'mean',
        'bounce_rate': 'mean'
    }
    
    resampled = df_time.resample(frequency).agg(agg_funcs).reset_index()
    enriched = enrich_data(resampled)
    
    # Phase 3: Trend Analysis (Growth Rates over Time)
    enriched = enriched.sort_values('timestamp')
    for col in ['revenue', 'clicks', 'conversions', 'cost']:
        enriched[f'{col}_growth'] = enriched[col].pct_change().fillna(0.0)
        # Ensure infinite percentages (e.g. from 0 previous) are handled
        enriched[f'{col}_growth'] = enriched[f'{col}_growth'].replace([np.inf, -np.inf], 0.0)
        
    return enriched

def channel_performance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates metrics by channel and ranks them by performance (ROI).
    """
    metrics = df.groupby('channel').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'conversions': 'sum',
        'cost': 'sum',
        'revenue': 'sum',
    }).reset_index()
    
    enriched = enrich_data(metrics)
    
    # Phase 3: Channel Performance Ranking (Sorted best to worst by ROI)
    ranked_channels = enriched.sort_values(by='roi', ascending=False)
    
    return ranked_channels
