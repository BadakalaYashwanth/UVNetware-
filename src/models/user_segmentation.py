import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def segment_users(df: pd.DataFrame, n_clusters=3):
    """
    Groups users into behavioral segments using KMeans Clustering.
    Tailored to identify different engagement profiles (e.g., High Value vs Bargain Shoppers).
    """
    df = df.copy()
    
    # Aggregate data per user to understand their holistic lifecycle
    # Since mock data has multiple transactions per user, let's group by user_id
    user_agg = df.groupby('user_id').agg({ 
        'revenue': 'sum',
        'clicks': 'sum',
        'session_duration': 'mean',
        'conversions': 'sum'
    }).reset_index()
    
    features = ['revenue', 'clicks', 'session_duration', 'conversions']
    
    # Standardize features for KMeans to eliminate magnitude bias
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(user_agg[features].fillna(0))
    
    # Run clustering - but only if we have enough samples
    final_n_clusters = min(n_clusters, len(user_agg))
    
    if final_n_clusters > 1:
        kmeans = KMeans(n_clusters=final_n_clusters, random_state=42, n_init=10)
        user_agg['segment_id'] = kmeans.fit_predict(X_scaled)
    else:
        # Fallback for single users or small datasets where clustering isn't possible
        user_agg['segment_id'] = 0
    
    # Map segment mappings back to the original operational dataframe 
    df = df.merge(user_agg[['user_id', 'segment_id']], on='user_id', how='left')
    
    # Extract segment profiles for high-level dashboard insights
    segment_profiles = user_agg.groupby('segment_id')[features].mean().to_dict(orient='index')
    
    return df, segment_profiles
