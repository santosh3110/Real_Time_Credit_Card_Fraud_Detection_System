from fraud_detection.components.stage_00_data_ingestion import DataIngestion
from fraud_detection.components.stage_01_data_validation import DataValidation
from fraud_detection.components.stage_02_feature_engineering import FeatureEngineering


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.feature_engineering = FeatureEngineering()


    def start_training_pipeline(self):
        """
        Starts the training pipeline
        :return: none
        """
        try:
            self.data_ingestion.initiate_data_ingestion()
            self.data_validation.initiate_data_validation()
            self.feature_engineering.initiate_feature_engineering()
            
        except Exception as e:
            raise e

        