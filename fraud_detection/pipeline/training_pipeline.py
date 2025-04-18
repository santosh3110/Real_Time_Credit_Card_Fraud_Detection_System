from fraud_detection.components.stage_00_data_ingestion import DataIngestion
from fraud_detection.components.stage_01_data_validation import DataValidation
from fraud_detection.components.stage_02_feature_engineering import FeatureEngineering
from fraud_detection.components.stage_03_model_training import ModelTraining
from fraud_detection.components.stage_04_model_evaluation import ModelEvaluation


class TrainingPipeline:
    def __init__(self):
        self.data_ingestion = DataIngestion()
        self.data_validation = DataValidation()
        self.feature_engineering = FeatureEngineering()
        self.model_training = ModelTraining()
        self.model_evaluation = ModelEvaluation()


    def start_training_pipeline(self):
        """
        Starts the training pipeline
        :return: none
        """
        try:
            self.data_ingestion.initiate_data_ingestion()
            self.data_validation.initiate_data_validation()
            self.feature_engineering.initiate_feature_engineering()
            self.model_training.initiate_model_training()
            self.model_evaluation.initiate_model_evaluation()
            
        except Exception as e:
            raise e

        