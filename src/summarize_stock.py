import json 
import pandas as pd
import numpy as np
import math
import yaml
from extract_data import *
from read_portfolio import *
from system_check import check_system

# Check the system type to ensure correct paths
if check_system() == 'macOS':
    config_path = '/Users/macbook/Mirror/trading_algorithm/config/config_file.yml'

else:
    config_path = 'C:\\Users\\viren\\DSML projects\\trading_alg\\config\\config_file.yml'


def summarize_column(column: pd.Series) -> pd.Series:
    """
    Returns a statistical summary of a pandas Series (column from DataFrame).

    Parameters:
    column (pd.Series): A column from a pandas DataFrame

    Returns:
    pd.Series: Summary statistics
    """
    summary = {}

    # General info
    summary['Data Type'] = column.dtype
    summary['Non-Null Count'] = column.count()
    summary['Null Count'] = column.isnull().sum()
    summary['Unique Count'] = column.nunique()

    if pd.api.types.is_numeric_dtype(column):
        # Numeric statistics
        summary['Mean'] = column.mean()
        summary['Std Dev'] = column.std()
        summary['Min'] = column.min()
        # summary['25%'] = column.quantile(0.25)
        summary['50% (Median)'] = column.median()
        # summary['75%'] = column.quantile(0.75)
        summary['Max'] = column.max()
        # summary['Skewness'] = column.skew()
        # summary['Kurtosis'] = column.kurt()
    else:
        # Categorical/text statistics
        summary['Top (Most Frequent)'] = column.mode().iloc[0] if not column.mode().empty else None
        summary['Top Freq'] = column.value_counts().iloc[0] if not column.value_counts().empty else None
        summary['Top %'] = (column.value_counts(normalize=True).iloc[0] * 100) if not column.value_counts().empty else None

    return pd.Series(summary)


def summarize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a statistical summary for each column in the given DataFrame.

    Parameters:
    df (pd.DataFrame): The DataFrame to summarize

    Returns:
    pd.DataFrame: Summary statistics for each column
    """
    summaries = []

    for col in df.columns:
        column = df[col]
        summary = {}

        # General info
        summary['Column Name'] = col
        summary['Data Type'] = column.dtype
        summary['Non-Null Count'] = column.count()
        summary['Null Count'] = column.isnull().sum()
        summary['Unique Count'] = column.nunique()

        if pd.api.types.is_numeric_dtype(column):
            # Numeric statistics
            summary['Mean'] = column.mean()
            summary['Std Dev'] = column.std()
            summary['Min'] = column.min()
            summary['25%'] = column.quantile(0.25)
            summary['50% (Median)'] = column.median()
            summary['75%'] = column.quantile(0.75)
            summary['Max'] = column.max()
            summary['Skewness'] = column.skew()
            summary['Kurtosis'] = column.kurt()
        else:
            # Categorical/text statistics
            mode = column.mode()
            summary['Top (Most Frequent)'] = mode.iloc[0] if not mode.empty else None
            value_counts = column.value_counts()
            summary['Top Freq'] = value_counts.iloc[0] if not value_counts.empty else None
            summary['Top %'] = (value_counts.iloc[0] / len(column) * 100) if not value_counts.empty else None

        summaries.append(summary)

    return pd.DataFrame(summaries).set_index('Column Name')


def summarize_stock(portfolio_path, by_column: bool=False):
    portfolio_df = read_portfolio(portfolio_path)

    with open(config_path,'r') as file:
        config = yaml.safe_load(file)

    key_name = 'stock_key'
    # api_key = config['keys'][key_name]

    for i in portfolio_df['stock_name']:
        current_stock = portfolio_df[portfolio_df['stock_name']==i]

        current_url = construct_urls(config_path=config_path,
                                    key_name=key_name,
                                    data_freq=str((current_stock[config['columns']['freq']]).values[0]),
                                    fromdate=current_stock[config['columns']['from']].values[0],
                                    todate=current_stock[config['columns']['to']].values[0],
                                    symbol=current_stock[config['columns']['stock_symbol']].values[0])
        
        print('URL constructed for:',current_stock[config['columns']['stock_symbol']].values[0])
        
        try:
            json_data_output = get_jsonparsed_data(current_url)
            print('Data fetched for:', i)
            symbol, data = read_json_data(json_data_output)
            print('Current Stock:', symbol)
            print(data.head(10))
            print('Data Summary:')
            print('Total Rows:', len(data))
            print('Columns:', data.columns.tolist())
            print('Date Range:',data['date'].min(), 'to', data['date'].max())
            print()

            if by_column:
                for column in data.columns:
                    summary = summarize_column(data[column])
                    print(f"Summary for column '{column}':")
                    print(summary)
                    print()
            else:
                summary_df = summarize_dataframe(data)
                print('Data Summary DataFrame:')
                print(summary_df)
                print()

        except:
            print('Error fetching data for:',i)
            continue


if __name__ == '__main__':
    summarize_stock(portfolio_path='C:\\Users\\viren\\DSML projects\\trading_alg\\portfolio.csv')