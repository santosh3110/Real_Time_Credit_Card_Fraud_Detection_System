import os
import sys
import pandas as pd
import numpy as np
from fraud_detection.logger.log import logging
from fraud_detection.exception.exception_handler import CustomException
from fraud_detection.config.configuration import ConfigurationManager
from fraud_detection.utils.util import read_yaml_file
from geopy.distance import geodesic

class FeatureEngineering:

    def __init__(self, app_config=ConfigurationManager()):
        """
        Feature Engineering Initialization
        app_config: ConfigurationManager
        """
        try:
            self.feature_engineering_config = app_config.get_feature_engineering_config()
            self.data_validation_config = app_config.get_data_validation_config()
            logging.info(f"{'='*20}Feature Engineering log started.{'='*20} ")
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def handle_missing_values(self, df):
        """
        Handle missing values in the dataset.
        """
        try:
            # Replace missing values with appropriate defaults
            df['category'] = df['category'].fillna('unknown')
            df['job'] = df['job'].fillna('unknown')
            df['merchant'] = df['merchant'].fillna('unknown')
            
            logging.info("Missing values have been handled.")
            return df
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def convert_data_types(self, df):
        """
        Convert data types to appropriate types.
        """
        try:
            # Convert categorical variables to categorical type
            categorical_cols = ['category', 'job', 'merchant', 'gender']
            df[categorical_cols] = df[categorical_cols].astype('category')
            
            logging.info("Data types have been converted.")
            return df
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def create_new_features(self, df):
        """
        Create new features.
        """
        try:
            
            # Step 1: Ensure datetime types
            df['trans_date_trans_time'] = pd.to_datetime(df['trans_date_trans_time'])
            df['dob'] = pd.to_datetime(df['dob'], errors='coerce')

            # Step 2: Extract years
            trans_year = df['trans_date_trans_time'].dt.year
            dob_year = df['dob'].dt.year

            # Step 3: Find where dob year > transaction year
            mask = dob_year > trans_year

            # Step 4: Fix those dates by subtracting 100 years
            df.loc[mask, 'dob'] = df.loc[mask, 'dob'] - pd.DateOffset(years=100)

            # Extract hour, day, weekday
            df['hour'] = df['trans_date_trans_time'].dt.hour
            df['day'] = df['trans_date_trans_time'].dt.day
            df['weekday'] = df['trans_date_trans_time'].dt.weekday
            df['age'] = (df['trans_date_trans_time'] - df['dob']).dt.days // 365
            df['is_large_transaction'] = (df['amt'] > 200).astype(int)
            df['log_amt'] = np.log1p(df['amt'])
            
            logging.info("New features have been created.")
            return df
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def calculate_distance(self, df):
        """
        Calculate distance between customer and merchant locations.
        """
        try:
            def haversine_distance(row):
                cust_loc = (row['lat'], row['long'])
                merch_loc = (row['merch_lat'], row['merch_long'])
                return geodesic(cust_loc, merch_loc).km
            
            df['distance_km'] = df.apply(haversine_distance, axis=1)
            
            logging.info("Distance between customer and merchant locations has been calculated.")
            return df
            
        except Exception as e:
            raise CustomException(e, sys) from e
        
    def initiate_feature_engineering(self):
        """
        Initiate feature engineering.
        """
        try:
            # Get the preprocessed data
            df = pd.read_csv(os.path.join(self.data_validation_config.clean_data_dir, 'clean_data.csv'))
            
            logging.info(f"Shape of the data: {df.shape}")
            
            # Handle missing values
            df = self.handle_missing_values(df)
            
            # Convert data types
            df = self.convert_data_types(df)
            
            # Create new features
            df = self.create_new_features(df)
            
            # Calculate distance
            df = self.calculate_distance(df)
            
            # Drop unnecessary columns
            df = df.drop(['trans_date_trans_time', 'cc_num', 'merchant', 'amt',
                          'first', 'last', 'street', 'city', 'state', 'zip','dob'], axis=1)
            
            logging.info(f"Preprocessed data shape: {df.shape}")
            
            # Save the engineered data
            os.makedirs(self.feature_engineering_config.engineered_data_dir, exist_ok=True)
            df.to_csv(self.feature_engineering_config.engineered_data_file, index=False)
            logging.info(f"Saved engineered data to: {self.feature_engineering_config.engineered_data_file}")
            
            logging.info(f"{'='*20}Feature Engineering log completed.{'='*20} \n\n")
            
        except Exception as e:
            raise CustomException(e, sys) from e