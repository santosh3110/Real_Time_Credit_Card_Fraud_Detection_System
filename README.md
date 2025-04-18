# Real-Time Credit Card Fraud Detection System
A real-time machine learning pipeline for detecting fraudulent credit card transactions using CatBoost, Kafka, MongoDB and Streamlit. This system leverages CatBoost classifier to detect fraudulent transactions as they occur. This model simulates streaming transactions using faker library, classifies them on-the-fly, provides an immediate email alert using SMTP PORT and SMTP SERVER, stores them in MongoDB and visualizes fraud patterns on a live dashboard.
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![Kafka](https://img.shields.io/badge/Kafka-3.0-orange)](https://kafka.apache.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-6.0-green)](https://www.mongodb.com/)
[![CatBoost](https://img.shields.io/badge/CatBoost-1.7-yellow)](https://catboost.ai/)
[![Streamlit](https://img.shields.io/badge/Streamlit-2.0-blue)](https://streamlit.io/)



🔗 **Live Streamlit App**: [Launch Dashboard](https://realtimecreditcardfrauddetectionsystem-csbhj8exeew6z7xew4g8xo.streamlit.app/)

---

## 📌 Table of Contents

- [📸 Demo Screenshots](#-demo-screenshots)
- [📦 Features](#-features)
- [🧱 Project Architecture](#-project-architecture)
- [🚀 Getting Started](#-getting-started)
- [📊 Streamlit Dashboard](#-streamlit-dashboard)
- [🧠 Model & Evaluation](#-model--evaluation)
- [🔄 Streaming Pipeline](#-streaming-pipeline)
- [📁 Directory Structure](#-directory-structure)
- [🛠️ Tech Stack](#️-tech-stack)
- [📜 License](#-license)

---

## 📸 Demo Screenshots

> 🔻 Add screenshots here for:
- Dashboard homepage
- Filter view
- Fraud map/trend view
- Kafka stream logs

---

## 📦 Features

✅ Real-time transaction simulation using **Faker**  
✅ Kafka Producer + Consumer for streaming pipeline  
✅ Feature engineering and transformation logic  
✅ **CatBoostClassifier** for high-performance fraud detection  
✅ **SHAP** visualizations for model explainability  
✅ MongoDB integration for storing flagged transactions  
✅ Live, interactive dashboard built with **Streamlit**  
✅ Email alerts for fraudulent activity  
✅ Fully modular and production-style architecture

---

## 🧱 Project Architecture

```text
[Kafka Producer] ---> [Kafka Broker] ---> [Kafka Consumer]
         |                                    |
     [Faker Txn]                         [Feature Transformer]
                                              |
                                       [CatBoost Model]
                                              |
                                 [MongoDB: fraud_alerts / non_fraud]
                                              |
                                      [Streamlit Dashboard + Alerting]
```

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.10+
- Kafka Cluster (e.g., Confluent Cloud or local)
- MongoDB Instance (Cloud or local)

### 📥 Clone the Repository

```bash
git clone https://github.com/your-username/Real_Time_Credit_Card_Fraud_Detection_System.git
cd Real_Time_Credit_Card_Fraud_Detection_System
```

### 📦 Install Requirements

```bash
pip install -r requirements.txt
```

### 🔐 Setup `.env`

```env
KAFKA_BOOTSTRAP_SERVERS=your_kafka_server
KAFKA_USERNAME=your_kafka_username
KAFKA_PASSWORD=your_kafka_password
MONGO_URI=your_mongodb_connection_string
SMTP_SERVER=smtp.yourmail.com
SMTP_PORT=587
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_email_password
EMAIL_RECEIVER=receiver_email@example.com
```

---

## 📊 Streamlit Dashboard

Launch the dashboard to view fraud patterns in real-time:

```bash
streamlit run app.py
```

Or open directly:
👉 [realtimecreditcardfrauddetectionsystem.streamlit.app](https://realtimecreditcardfrauddetectionsystem-csbhj8exeew6z7xew4g8xo.streamlit.app/)

---

## 🧠 Model & Evaluation

- Model: `CatBoostClassifier`
- Evaluation Metrics:
  - **Accuracy**: 99.94%
  - **ROC AUC**: 99.94%
  - **Log Loss**: 0.0020
- SHAP-based interpretability with feature importance ranking

📂 Outputs:
- `trained_model.cbm`
- `evaluation_metrics.csv`
- `shap_values.pkl`

---

## 🔄 Streaming Pipeline

Run the full pipeline:

```bash
python fraud_detection/pipeline/streaming_pipeline.py
```

This runs:
- `kafka_producer` → Sends transactions
- `kafka_consumer` → Classifies and stores transactions
- `alerting` → Sends email for frauds

---

## 📁 Directory Structure

```bash
fraud_detection/
│
├── components/               # All modular ML pipeline stages
├── config/                   # Config & constants
├── streaming/                # Kafka consumer, transformer, producer
├── data_generator/           # Faker-based Kafka producer
├── utils/                    # Utility and alerting modules
├── pipeline/                 # Training and streaming pipelines
├── saved_models/             # Trained model
├── artifacts/                # Data: raw, cleaned, engineered
├── logs/                     # Pipeline logs
├── reports/                  # Evaluation metrics & SHAP
├── app.py                    # Streamlit dashboard
├── main.py                   # Entry point
└── requirements.txt
```

---

## 🛠️ Tech Stack

| Component       | Tool/Library                    |
|----------------|----------------------------------|
| ML Model       | CatBoost                        |
| Stream         | Kafka + Confluent               |
| Data Sim       | Faker                            |
| Dashboard      | Streamlit + Plotly              |
| Storage        | MongoDB                         |
| Geo Analysis   | Geopy                            |
| Email Alerts   | SMTP                             |
| Explainability | SHAP                             |
| Packaging      | YAML, Python-dotenv             |

---

## 📜 License

This project is licensed under the MIT License.  
Feel free to use, contribute, or fork!

---

## 🙌 Acknowledgements

- Thanks to **CatBoost** for blazing-fast tree boosting
- Thanks to **Streamlit** for effortless dashboards
- Inspired by real-world streaming data and fraud challenges
