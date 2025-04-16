import os
import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from catboost import CatBoostClassifier
from fraud_detection.logger.log import logging
from fraud_detection.exception.exception_handler import CustomException
from fraud_detection.config.configuration import ConfigurationManager
from fraud_detection.utils.util import read_yaml_file

class ModelTraining:

    def __init__(self, app_config=ConfigurationManager()):
        """
        Model Training Initialization
        app_config: ConfigurationManager
        """
        try:
            self.model_training_config = app_config.get_model_training_config()
            self.feature_engineering_config = app_config.get_feature_engineering_config()
            logging.info(f"{'='*20}Model Training log started.{'='*20} ")
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def load_data(self):
        """
        Load the engineered data for training.
        """
        try:
            # Read the engineered data
            df = pd.read_csv(self.feature_engineering_config.engineered_data_file)
            
            # Split data into features and target
            X = df.drop(columns=[self.model_training_config.target_column], axis=1)
            y = df[self.model_training_config.target_column]
            
            # Split data into training and validation sets
            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.25, random_state=42)
            
            logging.info(f"Data split into training and validation sets.")
            return X_train, X_val, y_train, y_val
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def get_cat_features(self, X_train):
        """
        Get categorical features.
        """
        try:
            cat_features = X_train.select_dtypes(include=['object', 'category']).columns.tolist()
            logging.info(f"Categorical features: {cat_features}")
            return cat_features
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def train_model(self, X_train, y_train):
        """
        Train the CatBoost model.
        """
        try:
            # Define the CatBoost classifier
            model = CatBoostClassifier(
                cat_features=self.get_cat_features(X_train),
                eval_metric='Recall',
                random_state=42,
                iterations=1000,
                learning_rate=0.177575,
                verbose=1
            )
            
            # Train the model
            model.fit(X_train, y_train)
            
            logging.info("Model training completed.")
            return model
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def save_model(self, model):
        """
        Save the trained model.
        """
        try:
            # Create the model directory if it doesn't exist
            os.makedirs(self.model_training_config.model_dir, exist_ok=True)
            
            # Save the model
            model.save_model(self.model_training_config.model_file)
            
            logging.info(f"Model saved to: {self.model_training_config.model_file}")
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def initiate_model_training(self):
        """
        Initiate model training.
        """
        try:
            # Load the data
            X_train, X_val, y_train, y_val = self.load_data()
            
            # Train the model
            model = self.train_model(X_train, y_train)
            
            # Save the model
            self.save_model(model)
            
            logging.info(f"{'='*20}Model Training log completed.{'='*20} \n\n")
            
        except Exception as e:
            raise CustomException(e, sys) from e