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


def summarize_stock(portfolio_path):
    portfolio_df = read_portfolio(portfolio_path)

    with open(config_path,'r') as file:
        config = yaml.safe_load(file)

    key_name = 'stock_key'
    api_key = config['keys'][key_name]

    for i in portfolio_df['stock_name']:
        current_stock = portfolio_df[portfolio_df['stock_name']==i]

        current_url = construct_urls(config_path=config_path,
                                     key_name=key_name,
                                     data_freq=str((current_stock[config['columns']['freq']]).values[0]),
                                     fromdate=current_stock[config['columns']['from']].values[0],
                                     todate=current_stock[config['columns']['to']].values[0],
                                     symbol=current_stock[config['columns']['stock_symbol']].values[0])
        
        print('URL constructed for:',current_stock[config['columns']['stock_symbol']].values[0])
        
        json_data_output = get_jsonparsed_data(current_url)
        print('Data fetched for:', current_stock[config['columns']['stock_symbol']].values[0])
        symbol, data = read_json_data(json_data_output)
        print(symbol)
        print(data)

if __name__ == '__main__':
    summarize_stock(portfolio_path='C:\\Users\\viren\\DSML projects\\trading_alg\\portfolio.csv')