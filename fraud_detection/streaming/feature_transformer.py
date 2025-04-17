import pandas as pd
import numpy as np
from datetime import datetime
from geopy.distance import geodesic


def transform_transaction(txn: dict) -> pd.DataFrame:
    """
    Transforms a raw transaction dict into model-ready features as a DataFrame.
    Args:
        txn (dict): Raw transaction from Kafka.
    Returns:
        pd.DataFrame: Single-row dataframe with transformed features.
    """
    try:
        # Parse dates
        txn_time = datetime.strptime(txn["trans_date_trans_time"], '%Y-%m-%d %H:%M:%S')
        dob = datetime.strptime(txn["dob"], '%Y-%m-%d')
        # Geolocation
        cust_loc = (txn["lat"], txn["long"])
        merch_loc = (txn["merch_lat"], txn["merch_long"])
        distance_km = geodesic(cust_loc, merch_loc).km
        # Feature dictionary
        features = {
            "category": txn["category"],
            "job": txn["job"],
            "gender": txn["gender"],
            "city_pop": txn["city_pop"],
            "lat": txn["lat"],
            "long": txn["long"],
            "merch_lat": txn["merch_lat"],
            "merch_long": txn["merch_long"],
            "log_amt": np.log1p(txn["amt"]),
            "is_large_transaction": int(txn["amt"] > 200),
            "hour": txn_time.hour,
            "day": txn_time.day,
            "weekday": txn_time.weekday(),
            "age": (txn_time - dob).days // 365,
            "distance_km": distance_km
        }
        df = pd.DataFrame([features])
        # Set categorical columns
        categorical_cols = ["category", "job", "gender"]
        for col in categorical_cols:
            df[col] = df[col].astype("category")
        return df
    
    except Exception as e:
        print(f"❌ Feature transformation failed: {e}")
        return None