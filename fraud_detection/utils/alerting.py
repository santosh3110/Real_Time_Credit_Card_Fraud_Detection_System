import time
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from pymongo import MongoClient
import logging
import os

load_dotenv()

SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT")) 

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_COLLECTION = os.getenv("MONGO_COLLECTION")

client = MongoClient(MONGO_URI)
db = client["txn_db"]
collection = db["fraud_alerts"]

def send_email_alert(transaction):
    subject = "🚨 Fraud Alert: Suspicious Transaction Detected!"
    body = f"""
🚨 FRAUD DETECTED 🚨
---------------------------
Transaction ID      : {transaction.get('transaction_id')}
Transaction Time    : {transaction.get('trans_date_trans_time')}
Credit Card Number  : {transaction.get('cc_num')}
Amount              : ${transaction.get('amt')}
Merchant            : {transaction.get('merchant')}
Category            : {transaction.get('category')}
Location            : {transaction.get('street')}, {transaction.get('city')}, {transaction.get('state')}
---------------------------
Please review this transaction immediately.
"""

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
        server.quit()
        print("📩 Email Alert Sent Successfully!")
    except Exception as e:
        logging.error(f"❌ Failed to send email: {e}")

def monitor_fraud_transactions():
    print("🚀 Monitoring MongoDB for Fraud Transactions...")
    last_checked_id = None

    while True:
        latest_fraud = collection.find_one(sort=[("_id", -1)])
        if latest_fraud and latest_fraud["_id"] != last_checked_id:
            print("🚨 New Fraud Transaction Detected:", latest_fraud)
            send_email_alert(latest_fraud)
            last_checked_id = latest_fraud["_id"]
        time.sleep(10)

if __name__ == "__main__":
    monitor_fraud_transactions()