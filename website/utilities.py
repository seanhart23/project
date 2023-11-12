import numpy as np
import pandas as pd


def calculate_percentage(val, total):
   """Calculates the percentage of a value over a total"""
   percent = np.round((np.divide(val, total) * 100), 2)
   return percent

def data_creation(data, percent, class_labels, group=None):
   for index, item in enumerate(percent):
       data_instance = {}
       data_instance['category'] = class_labels[index]
       data_instance['value'] = item
       data_instance['group'] = group
       data.append(data_instance)

def create_data(row, column_name, stocks_portfolio=None):
    data = {
               'date': row['timestamp'].strftime('%Y-%m-%d'), 
               'value': row[column_name],
               'group': column_name,
               'stocks': stocks_portfolio
            }
    return data

def create_d3_line_data(portfolios, df, stocks_portfolio):
    df.reset_index(inplace=True)
    data_compiled = []
    for portfolio in portfolios:
        temp_df = df[['timestamp', portfolio]]
        for _, row in temp_df.iterrows():
            data_compiled.append(create_data(row, portfolio, stocks_portfolio))
    return data_compiled

def create_d3_beta_data(rolling_beta):
    beta_df = pd.DataFrame(rolling_beta, columns = ['Beta'])
    beta_df.dropna(inplace=True, axis=0)
    beta_df.reset_index(inplace=True)
    data_compiled = []
    for _, row in beta_df.iterrows():
      data_compiled.append(create_data(row, 'Beta'))
    return data_compiled

def create_d3_correlation_data(corr_df):
    data_compiled = []
    # flatten the correlation matrix
    corr_df = corr_df.stack().reset_index()

    # rename the columns
    corr_df.columns = ['FEATURE_1', 'FEATURE_2', 'CORRELATION']
    data_compiled = []
    for _, row in corr_df.iterrows():
        data = {
            'group': row['FEATURE_1'], 
            'variable': row['FEATURE_2'],
            'value': row['CORRELATION'],
        }
        data_compiled.append(data)

def create_d3_bar_data(roi):
    roi = roi.to_dict()
    barchart_data = []
    data_creation(barchart_data, list(roi.values()), list(roi.keys()), "All")
    return barchart_data
