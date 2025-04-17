from confluent_kafka import Producer
from faker import Faker
from dotenv import load_dotenv
from datetime import datetime
import os
import json
import random
import time
from datetime import datetime


# Load secrets from .env
load_dotenv()

fake = Faker('en_US')

conf = {
    "bootstrap.servers": os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "sasl.username": os.getenv("KAFKA_USERNAME"),
    "sasl.password": os.getenv("KAFKA_PASSWORD")
}

producer = Producer(conf)

categories = ['misc_net', 'grocery_pos', 'entertainment', 'gas_transport',
              'misc_pos', 'grocery_net', 'shopping_net', 'shopping_pos',
              'food_dining', 'personal_care', 'health_fitness', 'travel',
              'kids_pets', 'home']

genders = ['M', 'F']

def generate_transaction():
    """
    Generate a transaction with fake data.
    
    Returns:
        dict: A dictionary containing the transaction data.
    """
    user_lat = fake.latitude()
    user_long = fake.longitude()
    trans_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dob = fake.date_of_birth(minimum_age=18, maximum_age=90)

    # Generate merchant coordinates
    merch_lat = fake.latitude()
    merch_long = fake.longitude()

    # Check if user and merchant coordinates are the same
    while (user_lat, user_long) == (merch_lat, merch_long):
        merch_lat = fake.latitude()
        merch_long = fake.longitude()

    transaction_data = {
        "transaction_id": fake.uuid4(),
        "trans_date_trans_time": trans_time,
        "cc_num": fake.credit_card_number(),
        "merchant": "fraud_"+fake.company(),
        "category": random.choice(categories),
        "amt": float(round(random.uniform(1, 30000), 1)),
        "first": fake.first_name(),
        "last": fake.last_name(),
        "gender": random.choice(genders),
        "street": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip": fake.zipcode(),
        "lat": float(user_lat),
        "long": float(user_long),
        "city_pop": random.randint(20, 3000000),
        "job": fake.job(),
        "dob": dob.strftime('%Y-%m-%d'),
        "merch_lat": float(merch_lat),
        "merch_long": float(merch_long)
    }
    return transaction_data

def delivery_report(err, msg):
    if err is not None:
        print(f"❌ Delivery failed: {err}")
    else:
        print(f"✅ Delivered to {msg.topic()} [{msg.partition()}]")

if __name__ == "__main__":
    print("🚀 Kafka Producer for Real-Time Fraud Simulation Started!")
    while True:
        txn = generate_transaction()
        producer.produce(
            topic="txn_data",
            value=json.dumps(txn),
            key=str(txn["cc_num"]),
            callback=delivery_report
        )
        producer.flush()
        time.sleep(10)
 