from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig", ["dataset_download_url", "raw_data_dir", "ingested_dir"])

DataValidationConfig = namedtuple("DataValidationConfig", ["clean_data_dir", "credit_card_fraud_transaction_csv_file"]) 

FeatureEngineeringConfig = namedtuple("FeatureEngineeringConfig", ["engineered_data_dir", "engineered_data_file"])

ModelTrainingConfig = namedtuple("ModelTrainingConfig", ["model_dir", "model_file", "target_column"])
