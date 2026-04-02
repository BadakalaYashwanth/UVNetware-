import pandas as pd

def recommend_budget(channel_performance_df: pd.DataFrame, total_budget: float = None) -> pd.DataFrame:
    """
    Recommends budget allocation across channels based on their historic ROI distribution.
    Allocates more budget to high ROI channels and reduces spend on low-performing channels.
    """
    df = channel_performance_df.copy()
    
    # If no total budget is provided, reallocate the historical total spend
    if total_budget is None:
        total_budget = df['cost'].sum()
        
    # Phase 5: Recommendation based on ROI distribution
    # We clip ROI at 0 so channels with negative ROI don't drag the formula math, but they still get a tiny baseline
    # Add a small epsilon logic if we want to keep channels alive, but for now we follow strict ROI weighting
    base_weight = 0.05 # Give every channel at least 5% weight to keep experimental budgets alive
    
    df['roi_normalized'] = df['roi'].apply(lambda x: x if x > 0 else 0)
    total_roi_score = df['roi_normalized'].sum()
    
    if total_roi_score <= 0:
        # Fallback: distribute evenly if all channels perform poorly
        df['recommended_budget'] = total_budget / len(df)
    else:
        # Distribute based on ROI performance + a small baseline
        df['budget_weight'] = base_weight + (df['roi_normalized'] / total_roi_score * (1 - len(df)*base_weight))
        df['recommended_budget'] = df['budget_weight'] * total_budget
    
    # Explicit Optimization Directions
    # Compare recommended budget against historical cost to dictate explicit actions
    df['adjustment_amount'] = df['recommended_budget'] - df['cost']
    
    def determine_action(row):
        if row['adjustment_amount'] > (row['cost'] * 0.1): # Over 10% increase
            return "Increase Spend (High ROI)"
        elif row['adjustment_amount'] < -(row['cost'] * 0.1): # Over 10% decrease
            return "Reduce Spend (Low ROI)"
        else:
            return "Maintain Spend"
            
    df['optimization_action'] = df.apply(determine_action, axis=1)
    
    return df[['channel', 'cost', 'revenue', 'roi', 'recommended_budget', 'adjustment_amount', 'optimization_action']]
