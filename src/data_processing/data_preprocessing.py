# Import external libraries
import pandas as pd
import numpy as np

# Import local modules
from src.data_processing import load_csv_from_zip as lcfz

'''
Module that defines useful method to prepare the data for Machine Learning algorithms.
For convenience, a wrapper function has been developed for the model-independent transformations.

Example:

from src.data_processing import data_preprocessing as dpp

train = dpp.basic_preprocessing(train, ['temp'])
'''

def make_datetime_index(df: pd.DataFrame):
    df.set_index(pd.to_datetime(df.pop('datetime')), inplace=True)
    return df

def make_datetime_features(df: pd.DataFrame):
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['day'] = df.index.dayofweek
    df['hour'] = df.index.hour
    return df

def make_vacation_feature(df: pd.DataFrame):
    df['vacations'] = 0

    df.loc['2011-04-15':'2011-04-25', 'vacations'] = 1
    df.loc['2011-06-25':'2011-08-21', 'vacations'] = 1
    df.loc['2011-12-22':'2012-01-02', 'vacations'] = 1
    df.loc['2012-03-31':'2012-04-09', 'vacations'] = 1
    df.loc['2012-06-23':'2012-08-26', 'vacations'] = 1
    df.loc['2012-12-22':'2012-12-31', 'vacations'] = 1
    return df

def select_features(df: pd.DataFrame, featureList=[]):
    df.drop(columns=featureList, inplace=True)
    return df

def add_missing_rows(df: pd.DataFrame):
    temp = df.copy()
    temp['delta_t'] = temp.index.to_series().diff()
    temp['delta_t'].fillna(pd.Timedelta('0 hour'))
    temp[(temp['delta_t']>pd.Timedelta('1 hours')) & (temp['delta_t']< pd.Timedelta('1 days'))]['delta_t']

    last_row_before_gap = 0
    return df

def remove_outlier(df: pd.DataFrame):
    index_list = df[(df['temp'] > 20) & (df['atemp'] < 15)].index
    index_list.append(df[df['weather'] == 4].index)
    df.drop(index=index_list, inplace=True)
    return df

def target_to_log(df: pd.DataFrame):
    df['casual'] = np.log1p(df['casual'])
    df['registered'] = np.log1p(df['registered'])
    df['count'] = np.log1p(df['count'])
    return df

def hour_to_cos(df: pd.DataFrame):
    df['second_harm'] = np.cos(4.0 * np.pi * df['hour'] / 24.0)
    df['hour'] = np.cos(2.0 * np.pi * df['hour'] / 24.0)
    return df

def hour_to_sin(df: pd.DataFrame):
    df['fourth_harm'] = np.sin(8.0 * np.pi * df['hour'] / 24.0 + 3.0 * np.pi / 12.0)
    df['third_harm'] = np.sin(6.0 * np.pi * df['hour'] / 24.0 + 3.0 * np.pi / 12.0)
    df['second_harm'] = np.sin(4.0 * np.pi * df['hour'] / 24.0 + 4.0 * np.pi / 12.0)
    df['hour'] = np.sin(2.0 * np.pi * df['hour'] / 24.0 + 3.0 * np.pi / 12.0)
    return df

def basic_prep_wrapper(df: pd.DataFrame, featureList=[]):
    df = make_datetime_index(df)
    df = make_datetime_features(df)
    df = make_vacation_feature(df)
    df = remove_outlier(df)
    df = select_features(df, featureList)
    return df

if(__name__ == '__main__'):
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    train, test = lcfz.read_csv_from_zip('./../../data/input/bike-sharing-demand.zip', ['train.csv', 'test.csv'])
    train = basic_prep_wrapper(train, ['temp'])
    train = target_to_log(train)
    test = basic_prep_wrapper(test, ['temp'])
    print('='*80)
    print("Prepared train dataset:")
    print(train.sample(5))
    print('='*80)
    print("Prepared test dataset:")
    print(test.sample(5))
