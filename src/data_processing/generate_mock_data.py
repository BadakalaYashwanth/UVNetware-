import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_mock_data(num_records=1000, output_path='data/raw/marketing_data.csv'):
    """
    Generates mock marketing data based on the provided schema.
    """
    np.random.seed(42)
    
    channels = ['Organic Search', 'Paid Search', 'Social Media', 'Email', 'Referral']
    campaigns = ['Summer Promo', 'Winter Sale', 'Spring Fling', 'Fall Cleanup', 'None']
    
    data = {
        "user_id": [f"user_{np.random.randint(10000, 99999)}" for _ in range(num_records)],
        "timestamp": [datetime.now() - timedelta(days=np.random.randint(0, 365), hours=np.random.randint(0, 24)) for _ in range(num_records)],
        "channel": np.random.choice(channels, num_records),
        "campaign_id": np.random.choice(campaigns, num_records),
        "impressions": np.random.randint(100, 5000, num_records),
        "clicks": np.random.randint(10, 500, num_records),
        "conversions": np.random.randint(0, 50, num_records),
        "cost": np.random.uniform(10.0, 500.0, num_records).round(2),
        "revenue": np.random.uniform(0.0, 2000.0, num_records).round(2),
        "session_duration": np.random.randint(30, 600, num_records), # in seconds
        "bounce_rate": np.random.uniform(0.1, 0.9, num_records).round(2)
    }
    
    df = pd.DataFrame(data)
    
    # Ensure cost is 0 for Organic and Referral unless specified otherwise
    df.loc[df['channel'].isin(['Organic Search', 'Referral']), 'cost'] = 0.0
    
    # Save to CSV
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"Generated {num_records} records at {output_path}")
    return df

if __name__ == "__main__":
    generate_mock_data(5000)
