import os
import sys
import json

# Ensure src modules can be imported
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from data_processing.generate_mock_data import generate_mock_data
from data_processing.preprocessing import clean_and_preprocess
from features.feature_engineering import enrich_data, channel_performance
from models.anomaly_detection import detect_anomalies
from models.budget_recommendation import recommend_budget
from insights.generate_report import generate_json_report

def main():
    print("======================================================")
    print("🚀 AI Analytics: Transforming Events into Insights ✅")
    print("======================================================")
    
    real_world_path = 'data/raw/real_world_input.json'
    
    # -----------------------------------------------------
    # Phase 1: Raw Data → Preprocessing
    # -----------------------------------------------------
    print("\n[1/7] Ingesting Raw Data & Preprocessing...")
    import pandas as pd
    from data_processing.parser import parse_real_world_data
    
    raw_df = pd.DataFrame()
    input_summary = None
    
    if os.path.exists(real_world_path):
        print(f"Found real-world input: {real_world_path}. Parsing nested structure.")
        with open(real_world_path, 'r') as f:
            real_data = json.load(f)
        raw_df = parse_real_world_data(real_data)
        input_summary = real_data.get('summary')
        print(f"Loaded {len(raw_df)} records from {real_world_path}")
    elif os.path.exists(raw_data_path):
        raw_df = pd.read_json(raw_data_path)
        print(f"Loaded {len(raw_df)} records from {raw_data_path}")
    else:
        print("Real input JSON payload not found. Falling back to CSV generator.")
        raw_df = generate_mock_data(5000, 'data/raw/marketing_data.csv')
        
    cleaned_df = clean_and_preprocess(raw_df)

    # -----------------------------------------------------
    # Phase 2 & 3: Time Aggregation → Feature Engineering
    # -----------------------------------------------------
    print("[2&3/7] Performing Time Aggregation & Feature Engineering...")
    # Add advanced calculations (ROI, CTR, CPC, CPA)
    enriched_df = enrich_data(cleaned_df)
    
    # Extract channel-specific metrics for optimization step
    chan_perf = channel_performance(enriched_df)
    
    # -----------------------------------------------------
    # Phase 4: ML Models
    # -----------------------------------------------------
    print("[4/7] Running ML Models (Anomaly, ROI Prediction, Segmentation)...")
    anomalies_df = detect_anomalies(enriched_df)
    
    # User Segmentation
    from models.user_segmentation import segment_users
    segmented_df, segment_profiles = segment_users(enriched_df, n_clusters=3)
    
    # ROI Feature Extraction
    from models.advanced_roi_prediction import train_roi_prediction_model
    xgb_model, feature_importance = train_roi_prediction_model(enriched_df, target_col='revenue')

    # -----------------------------------------------------
    # Phase 5: Optimization
    # -----------------------------------------------------
    print("[5/7] Executing Optimization (Budget Recommendation)...")
    budget_recs = recommend_budget(chan_perf, total_budget=50000.0)
    
    # -----------------------------------------------------
    # Phase 6 & 7: Insight Generation → JSON Output
    # -----------------------------------------------------
    print("[6&7/7] Generating Insights & Writing JSON Output...")
    # The report generator handles the explicit Time Aggregation summarizations
    report_dict = generate_json_report(
        enriched_df, chan_perf, anomalies_df, budget_recs,
        importance_dict=feature_importance, segment_profiles=segment_profiles,
        input_summary=input_summary
    )
    
    output_path = 'output_insights.json'
    with open(output_path, 'w') as f:
        json.dump(report_dict, f, indent=2)
        
    print(f"\n✅ Pipeline Complete! Structured knowledge written to: {output_path}")

if __name__ == "__main__":
    main()
