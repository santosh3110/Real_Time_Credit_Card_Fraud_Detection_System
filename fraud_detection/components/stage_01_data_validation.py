import os
import sys
import ast 
import pandas as pd
import pickle
from fraud_detection.logger.log import logging
from fraud_detection.config.configuration import ConfigurationManager
from fraud_detection.exception.exception_handler import CustomException



class DataValidation:
    def __init__(self, app_config = ConfigurationManager()):
        try:
            self.data_validation_config= app_config.get_data_validation_config()
        except Exception as e:
            raise CustomException(e, sys) from e


    
    def preprocess_data(self):
        try:
            fraud_transactions = pd.read_csv(self.data_validation_config.credit_card_fraud_transaction_csv_file, sep=",", on_bad_lines='skip', encoding='utf-8', low_memory=False)
            
            logging.info(f" Shape of fraud transactions data file: {fraud_transactions.shape}")

            #Here Image URL columns is important for the poster. So, we will keep it
            fraud_transactions = fraud_transactions[['trans_date_trans_time', 'cc_num', 'merchant', 'category',
                                                     'amt', 'first', 'last', 'gender', 'street', 'city', 'state', 'zip',
                                                     'lat', 'long', 'city_pop', 'job', 'dob', 'merch_lat', 'merch_long', 'is_fraud']]
            
                        
            # Saving the cleaned data for feature engineering
            os.makedirs(self.data_validation_config.clean_data_dir, exist_ok=True)
            fraud_transactions.to_csv(os.path.join(self.data_validation_config.clean_data_dir,'clean_data.csv'), index = False)
            logging.info(f"Saved cleaned data to {self.data_validation_config.clean_data_dir}")


        except Exception as e:
            raise CustomException(e, sys) from e

    
    def initiate_data_validation(self):
        try:
            logging.info(f"{'='*20}Data Validation log started.{'='*20} ")
            self.preprocess_data()
            logging.info(f"{'='*20}Data Validation log completed.{'='*20} \n\n")
        except Exception as e:
            raise CustomException(e, sys) from e