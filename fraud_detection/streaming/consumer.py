import os
import json
import pandas as pd
from pymongo import MongoClient
from confluent_kafka import Consumer
from dotenv import load_dotenv
from catboost import CatBoostClassifier, Pool

from fraud_detection.streaming.feature_transformer import transform_transaction

# Load env
load_dotenv()

# === MongoDB ===
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client["txn_db"]
fraud_collection = db["fraud_alerts"]
non_fraud_collection = db["non_fraud"]

# === Kafka Consumer Config ===
kafka_conf = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": os.getenv("KAFKA_USERNAME"),
    "sasl.password": os.getenv("KAFKA_PASSWORD"),
    "group.id": "fraud-detection-group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(kafka_conf)
consumer.subscribe(["txn_data"])
print("👂 Subscribed to Kafka topic: txn_data")

# === Load CatBoost Model ===
model_path = os.path.join("saved_models", "trained_model.cbm")
model = CatBoostClassifier()
model.load_model(model_path)
print("✅ Model loaded from", model_path)

# === Main Loop ===
try:
    while True:
        msg = consumer.poll(1.0)
        print("⏳ Waiting for messages...")

        if msg is None:
            continue
        if msg.error():
            print(f"❌ Kafka error: {msg.error()}")
            continue

        try:
            txn = json.loads(msg.value().decode('utf-8'))

            features_df = transform_transaction(txn)
            if features_df is None:
                print("⚠️ Skipped: Feature transformation failed.")
                continue

            print(features_df.dtypes)
            print(model.get_params())

            # Clean categorical dtypes
            categorical_cols = ['category', 'gender', 'job']
            for col in categorical_cols:
                if col in features_df.columns:
                    features_df[col] = features_df[col].astype(str)

            # Wrap the features in a CatBoost Pool
            features_pool = Pool(data=features_df, cat_features=categorical_cols)

            # Predict
            prediction = int(model.predict(features_pool)[0])

            txn["is_fraud"] = prediction

            if prediction == 1:
                print("🚨 Fraud Detected!")
                fraud_collection.insert_one(txn)
            else:
                print("✅ Legit Transaction")
                non_fraud_collection.insert_one(txn)

        except Exception as e:
            print(f"❌ Error processing transaction: {e}")

except KeyboardInterrupt:
    print("🛑 Stopping Kafka consumer...")

finally:
    consumer.close()
