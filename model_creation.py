import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from helpers import GetHCData

class HCData():
    def __init__(self):
        self.feature_df = pd.DataFrame()
        self.response_df = pd.DataFrame()
        self.X_train = pd.DataFrame()
        self.X_test = pd.DataFrame()
        self.y_train = pd.DataFrame()
        self.y_test = pd.DataFrame()

    def get_hc_data(self):
        HospData = GetHCData()
        HospData.limit = 1000000

        # get response_df
        HospData.send_hc_request()
        self.response_df = pd.DataFrame(HospData.get_hc_data())
        print('Feature Data Loaded: ', len(self.response_df), ' rows loaded')

        # get feature_df
        HospData.send_hc_request(hcahps=True)
        self.feature_df = pd.DataFrame(HospData.get_hc_data())
        print('Response Data Loaded: ', len(self.feature_df), ' rows loaded')

    def reshape_data(self):
        # select relevant columns & values
        self.feature_df = self.feature_df[['provider_id',
                                           'hcahps_measure_id',
                                           'hcahps_answer_percent']]
        self.response_df = self.response_df[['provider_id',
                                             'measure_id',
                                             'compared_to_national']]
        
        # reformat dataframes to have the same length, measures in columns
        self.feature_df = self.feature_df.pivot(index='provider_id',
                                                columns='hcahps_measure_id',
                                                values='hcahps_answer_percent')#.reset_index()
        print(len(self.feature_df), ' feature rows remaining after reshaping')

        self.response_df = self.response_df.pivot(index='provider_id',
                                                  columns='measure_id',
                                                  values='compared_to_national')#.reset_index()
        print(len(self.response_df), 'response rows remaining after reshaping')

    def create_split(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.feature_df, 
                                                                                self.response_df,
                                                                                test_size=0.2)
        print('X_train created with ', len(self.X_train), 'rows')
        print('X_test created with ', len(self.X_test), 'rows')
        print('y_train created with ', len(self.y_train), 'rows')
        print('y_test created with ', len(self.y_test), 'rows')

    def clean_data(self, split_data, X_cols='all', y_cols='all'):
        # choose split_data
        if split_data == 'train':
            X_df = self.X_train.copy()
            y_df = self.y_train.copy()
        elif split_data == 'test':
            X_df = self.X_test.copy()
            y_df = self.y_test.copy()

        # choose relevant columns from each
        if X_cols != 'all':
            X_df = X_df[X_cols]
        if y_cols != 'all':
            y_df = y_df[y_cols]

        # X cleaning:
        # loop through each remaining column, remove NAs, convert to numeric, then drop empties
        skip_cols = ['provider_id']
        na_values = ['Not Applicable', 'Not Available']

        for col in X_df.columns:
            if col not in skip_cols:
                X_df[col] = np.where(X_df[col].isin(na_values), np.nan, X_df[col])
                X_df[col] = pd.to_numeric(X_df[col])
                if X_df[col].count() == 0:
                    X_df = X_df.drop(columns = col)

        # y cleaning:
        # convert various values to: better, worse, same, not available. then drop empties
        y_convert_dict = {
            'No Different Than the National Rate': 'same',
            'No Different Than the National Value': 'same',
            'Better Than the National Rate': 'better',
            'Better Than the National Value': 'better',
            'Worse Than the National Rate': 'worse',
            'Worse Than the National Value': 'worse',
            'Not Available': 'not available', 
            'Number of Cases Too Small': 'not available'
        }
        skip_cols = ['provider_id']

        for col in y_df.columns:
            if col not in skip_cols:
                y_df[col] = y_df[col].map(y_convert_dict)

        # overwrite appropriate dataframes
        if split_data == 'train':
            self.X_train = X_df
            self.y_train = y_df
        elif split_data == 'test':
            self.X_test = X_df
            self.y_test = y_df        
        
        print('Chosen dataset cleaned')
        
class HCModel():
    def __init__(self, X, y):
        self.X = X
        self.y = y

    def set_binary_response(self, col, true_val, remove_nas=True):
        # drop not availables
        if remove_nas:
            


        # convert the remaining values to binary
        self.y[col] = np.where(self.y[col] == true_val, 1, 0)

    def convert_to_array(self):
        pass

    def scale_values(self):
        pass

    def model_fit(self):
        pass