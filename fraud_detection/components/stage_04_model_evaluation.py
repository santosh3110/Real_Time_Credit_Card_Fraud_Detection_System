import os
import sys
import pandas as pd
import numpy as np
import shap
import pickle
from sklearn.metrics import accuracy_score, confusion_matrix, roc_auc_score, log_loss
from catboost import CatBoostClassifier
from fraud_detection.logger.log import logging
from fraud_detection.exception.exception_handler import CustomException
from fraud_detection.config.configuration import ConfigurationManager
from fraud_detection.utils.util import read_yaml_file


class ModelEvaluation:

    def __init__(self, app_config=ConfigurationManager()):
        """
        Model Evaluation Initialization
        app_config: ConfigurationManager
        """
        try:
            self.model_evaluation_config = app_config.get_model_evaluation_config()
            self.model_training_config = app_config.get_model_training_config()
            self.feature_engineering_config = app_config.get_feature_engineering_config()
            logging.info(f"{'='*20}Model Evaluation log started.{'='*20} ")
        except Exception as e:
            raise CustomException(e, sys) from e
        
        
    def load_model(self):
        """
        Load the trained model.
        """
        try:
            model_path = self.model_training_config.model_file
            model = CatBoostClassifier()
            model.load_model(model_path, format='cbm')
            
            logging.info(f"Model loaded from: {model_path}")
            return model
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def load_data(self):
        """
        Load the data for evaluation.
        """
        try:
            # Load the engineered data
            df = pd.read_csv(self.feature_engineering_config.engineered_data_file)
            
            # Split data into features and target
            X = df.drop(columns=[self.model_training_config.target_column], axis=1)
            y = df[self.model_training_config.target_column]
            
            logging.info(f"Data loaded for evaluation. Shape: {X.shape}")
            return X, y
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def calculate_metrics(self, model, X, y):
        """
        Calculate evaluation metrics.
        """
        try:
            # Make predictions
            y_pred = model.predict(X)
            y_proba = model.predict_proba(X)[:, 1]
            
            # Calculate metrics
            accuracy = accuracy_score(y, y_pred)
            roc_auc = roc_auc_score(y, y_proba)
            log_loss_value = log_loss(y, y_proba)
            
            # Create a metrics dictionary
            metrics = {
                "Accuracy": accuracy,
                "ROC AUC Score": roc_auc,
                "Log Loss": log_loss_value
            }
            
            logging.info("Evaluation metrics calculated.")
            return metrics
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def generate_shap_values(self, model, X):
        """
        Generate SHAP values for feature importance.
        """
        try:
            # Create an explainer
            explainer = shap.Explainer(model)
            
            # Get SHAP values
            shap_values = explainer(X)
            
            logging.info("SHAP values generated.")
            return shap_values
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def save_evaluation_report(self, metrics):
        """
        Save the evaluation report.
        """
        try:
            # Create the evaluation directory if it doesn't exist
            os.makedirs(self.model_evaluation_config.evaluation_dir, exist_ok=True)
            
            # Save the metrics to a CSV file
            metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Value'])
            metrics_df.to_csv(self.model_evaluation_config.evaluation_file, index=False)

            
            logging.info(f"Evaluation report saved to: {os.path.join(self.model_evaluation_config.evaluation_dir, self.model_evaluation_config.evaluation_file)}")
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def save_shap_values(self, shap_values):
        """
        Save the SHAP values using pickle.
        """
        try:
            os.makedirs(os.path.dirname(self.model_evaluation_config.shap_file), exist_ok=True)

            with open(self.model_evaluation_config.shap_file, 'wb') as f:
                pickle.dump(shap_values, f)

            logging.info(f"SHAP values saved to: {self.model_evaluation_config.shap_file}")

        except Exception as e:
            raise CustomException(e, sys) from e
        
    def initiate_model_evaluation(self):
        """
        Initiate model evaluation.
        """
        try:
            # Load the model
            model = self.load_model()
            
            # Load the data
            X, y = self.load_data()
            
            # Calculate metrics
            metrics = self.calculate_metrics(model, X, y)
            
            # Generate SHAP values
            shap_values = self.generate_shap_values(model, X)
            
            # Save the evaluation report
            self.save_evaluation_report(metrics)
            
            # Save the SHAP values
            self.save_shap_values(shap_values)
            
            logging.info(f"{'='*20}Model Evaluation log completed.{'='*20} \n\n")
            
        except Exception as e:
            raise CustomException(e, sys) from e