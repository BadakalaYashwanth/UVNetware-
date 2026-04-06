import pandas as pd
from sklearn.ensemble import IsolationForest

def detect_anomalies(df: pd.DataFrame, features=['impressions', 'clicks', 'conversions', 'conversion_rate', 'cost'], contamination=0.05):
    """
    Detects anomalies using Isolation Forest.
    Specifically calibrated to detect abnormal traffic volumes (impressions/clicks) 
    or sudden conversion/drop-off irregularities.
    Marks anomalies with a boolean 'is_anomaly' flag.
    """
    df = df.copy()
    
    # Fill any missing values in the features
    X = df[features].fillna(0)
    
    # Handle very small datasets for which isolation is not meaningful
    if len(df) < 5:
        df['is_anomaly'] = False
        df['anomaly_score'] = 1.0 # 1.0 means perfectly normal in IsolationForest context
        df['anomaly_reason'] = "Insuffient data for anomaly detection"
        return df

    # Initialize Isolation Forest
    # Contamination defines the expected proportion of outliers in the data set
    model = IsolationForest(contamination=contamination, random_state=42)
    
    # Fit and predict (-1 for anomaly, 1 for normal)
    predictions = model.fit_predict(X)
    
    # Convert to boolean flag
    df['is_anomaly'] = predictions == -1
    
    # Anomaly score (lower is more anomalous)
    df['anomaly_score'] = model.decision_function(X)
    
    # Phase 6: Explain causes for anomalies
    def explain_anomaly(row):
        if not row['is_anomaly']:
            return "Normal"
        causes = []
        if 'cost' in row and row['cost'] > df['cost'].mean() * 2:
            causes.append("Unusually high cost")
        if 'conversions' in row and row['conversions'] == 0 and row['clicks'] > 0:
            causes.append("Zero conversions despite traffic")
        if 'impressions' in row and row['impressions'] < df['impressions'].mean() * 0.1:
            causes.append("Sudden drop in impressions")
        if 'conversion_rate' in row and row['conversion_rate'] < df['conversion_rate'].mean() * 0.5:
            causes.append("Significant conversion rate drop")
            
        return " | ".join(causes) if causes else "Complex multivariate anomaly"

    df['anomaly_reason'] = df.apply(explain_anomaly, axis=1)
    
    return df
