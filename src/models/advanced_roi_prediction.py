import pandas as pd
import numpy as np
try:
    import xgboost as xgb
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import mean_squared_error
except ImportError:
    xgb = None

def train_roi_prediction_model(df: pd.DataFrame, target_col='revenue'):
    """
    Advanced ROI/Revenue Prediction using XGBoost.
    Uses historical spend and channel interaction to predict future returns.
    """
    if xgb is None:
        print("XGBoost is not installed. Please install it to use advanced ROI prediction.")
        return None

    df = df.copy()
    
    # 1. Feature Selection
    # For a real implementation, you'd encode categorical channels and scale numeric features.
    features = ['impressions', 'clicks', 'cost', 'session_duration']
    
    # Simple preprocessing: ensure no missing values
    X = df[features].fillna(0)
    y = df[target_col].fillna(0)
    
    # 2. Dataset Size Check
    # XGBoost and Train/Test split require more than 1 sample to function
    if len(df) < 5:
        print("Dataset size too small for advanced ML ROI prediction. Returning default benchmarks.")
        importance_dict = {f: 0.25 for f in features} # equal baseline distribution
        return None, importance_dict

    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Initialize and Train XGBoost
    model = xgb.XGBRegressor(
        objective='reg:squarederror', 
        n_estimators=100, 
        learning_rate=0.1, 
        max_depth=5
    )
    
    model.fit(X_train, y_train)
    
    # 4. Evaluate and Extract Feature Importance
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    
    # Store feature importances mapping
    importance_dict = dict(zip(features, model.feature_importances_))
    
    print(f"XGBoost ROI Prediction Model trained. Validation MSE: {mse:.2f}")
    
    return model, importance_dict

def predict_future_roi(model, upcoming_campaigns_df: pd.DataFrame):
    """
    Uses trained model to forecast revenue across hypothetical future allocations.
    """
    if model is None:
        return None
        
    features = ['impressions', 'clicks', 'cost', 'session_duration']
    X_future = upcoming_campaigns_df[features].fillna(0)
    
    predicted_revenue = model.predict(X_future)
    upcoming_campaigns_df['predicted_revenue'] = predicted_revenue
    
    # Derived ROI based on model output
    upcoming_campaigns_df['predicted_roi'] = np.where(
        upcoming_campaigns_df['cost'] > 0, 
        ((predicted_revenue - upcoming_campaigns_df['cost']) / upcoming_campaigns_df['cost']) * 100, 
        0
    )
    
    return upcoming_campaigns_df
