import os
import sys
from fraud_detection.logger.log import logging
from fraud_detection.utils.util import read_yaml_file
from fraud_detection.exception.exception_handler import CustomException
from fraud_detection.entity.config_entity import (DataIngestionConfig, DataValidationConfig,
                                                   FeatureEngineeringConfig, ModelTrainingConfig, ModelEvaluationConfig)
from fraud_detection.constant import *


class ConfigurationManager:
    def __init__(self, config_file_path: str = CONFIG_FILE_PATH):
        try:
            self.configs_info = read_yaml_file(file_path=config_file_path)
        except Exception as e:
            raise CustomException(e, sys) from e

    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            data_ingestion_config = self.configs_info['data_ingestion_config']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            dataset_dir = data_ingestion_config['dataset_dir']

            ingested_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'])
            raw_data_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['raw_data_dir'])

            response = DataIngestionConfig(
                dataset_download_url = data_ingestion_config['dataset_download_url'],
                raw_data_dir = raw_data_dir,
                ingested_dir = ingested_data_dir
            )

            logging.info(f"Data Ingestion Config: {response}")
            return response

        except Exception as e:
            raise CustomException(e, sys) from e
        
    def get_data_validation_config(self) -> DataValidationConfig:
        try:
            data_validation_config = self.configs_info['data_validation_config']
            data_ingestion_config = self.configs_info['data_ingestion_config']
            dataset_dir = data_ingestion_config['dataset_dir']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            credit_card_fraud_transaction_csv_file = data_validation_config['credit_card_fraud_transaction_csv_file']

            credit_card_fraud_transaction_csv_file_dir = os.path.join(artifacts_dir, dataset_dir, data_ingestion_config['ingested_dir'], credit_card_fraud_transaction_csv_file)
            clean_data_path = os.path.join(artifacts_dir, dataset_dir, data_validation_config['clean_data_dir'])

            response = DataValidationConfig(
                clean_data_dir = clean_data_path,
                credit_card_fraud_transaction_csv_file = credit_card_fraud_transaction_csv_file_dir,
            )

            logging.info(f"Data Validation Config: {response}")
            return response

        except Exception as e:
            raise CustomException(e, sys) from e
        

    def get_feature_engineering_config(self) -> FeatureEngineeringConfig:
        try:
            feature_engineering_config = self.configs_info['feature_engineering_config']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            
            engineered_data_dir = os.path.join(artifacts_dir, feature_engineering_config['engineered_data_dir'])
            
            response = FeatureEngineeringConfig(
                engineered_data_dir=engineered_data_dir,
                engineered_data_file=os.path.join(engineered_data_dir, feature_engineering_config['engineered_data_file'])
            )
            
            logging.info(f"Feature Engineering Config: {response}")
            return response
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
        
    def get_model_training_config(self) -> ModelTrainingConfig:
        """
        Get Model Training Configuration
        """
        try:
            model_training_config = self.configs_info['model_training_config']
            # artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            model_dir = model_training_config['model_dir']
            model_file = os.path.join(model_dir, model_training_config['model_file'])

            response = ModelTrainingConfig(
                model_dir=model_dir,
                model_file=model_file,
                target_column=model_training_config['target_column']
            )

            logging.info(f"Model Training Config: {response}")
            return response
        
        except Exception as e:
            raise CustomException(e, sys) from e
        
        
    def get_model_evaluation_config(self) -> ModelEvaluationConfig:
        """
        Get Model Evaluation Configuration
        """
        try:
            model_evaluation_config = self.configs_info['model_evaluation_config']
            artifacts_dir = self.configs_info['artifacts_config']['artifacts_dir']
            evaluation_dir = os.path.join(artifacts_dir, model_evaluation_config['evaluation_dir'])
            evaluation_file = os.path.join(evaluation_dir, model_evaluation_config['evaluation_file'])
            shap_dir = os.path.join(evaluation_dir, model_evaluation_config['shap_dir'])
            shap_file = os.path.join(shap_dir, model_evaluation_config['shap_file'])
            response = ModelEvaluationConfig(
                evaluation_dir=evaluation_dir,
                evaluation_file=evaluation_file,
                shap_dir=shap_dir,
                shap_file=shap_file
            )
            logging.info(f"Model Evaluation Config: {response}")
            return response
        except Exception as e:
            raise CustomException(e, sys) from e

        