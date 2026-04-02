import pandas as pd
import numpy as np

def clean_and_preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize data types, handle missing values, and validate schema.
    This acts as the gatekeeper before data moves downstream.
    """
    df = df.copy()
    
    # 1. Standardize Data Types
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # 2. Handle missing or negative metrics (Sanity checks)
    numeric_cols = ['impressions', 'clicks', 'conversions', 'cost', 'revenue']
    for col in numeric_cols:
        if col in df.columns:
            # Replace negative values with 0
            df[col] = np.where(df[col] < 0, 0, df[col])
            # Fill missing values with 0
            df[col] = df[col].fillna(0)

    # 3. Add explicit date and timeframe grouping columns (Time Aggregation prep)
    df['date'] = df['timestamp'].dt.date
    # Provide safe fallback for to_period with new pandas notation (though M often works, ME is safer)
    try:
        df['year_month'] = df['timestamp'].dt.to_period('M').dt.start_time
    except ValueError:
        df['year_month'] = df['timestamp'].dt.to_period('ME').dt.start_time
        
    df['week_start'] = df['timestamp'] - pd.to_timedelta(df['timestamp'].dt.dayofweek, unit='D')
    
    return df
