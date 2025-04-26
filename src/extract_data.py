import certifi
import json
import yaml
from system_check import check_system
import pandas as pd

try:
    from urllib.request import urlopen
except ImportError:
    print('Error: Could not import urlopen from urllib.request')   

def get_jsonparsed_data(url: str):
    '''
    Function that fetches the data from request url
    '''
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


def read_json_data(json_data):

    if isinstance(json_data, dict):
        symbol = json_data['symbol']
        data_frame = pd.DataFrame(json_data['historical'])
        return symbol, data_frame
    
    if isinstance(json_data,list):
        return '', pd.DataFrame(json_data)


def construct_urls(config_path: str=None, key_name: str=None, data_freq: str=None, ticker_name: list=None, fromdate: str=None, todate: str=None, currency: str = None):
    '''
    Constructs a URL for an api request from FMP
    '''
    with open(config_path,'r') as file:
        config = yaml.safe_load(file)

    final_urls = []
    api_key = config['keys'][key_name]

    base_url = config['requests'][data_freq]

    if data_freq == 'forex_list':
        # base_url = config['requests'][data_freq]
        final_url = base_url.format(key=api_key)

    elif data_freq == 'forex':
        # base_url = config['requests'][data_freq]
        final_url = base_url.format(currencies=currency, key=api_key)

    elif data_freq == 'forex_light':
        # base_url = config['requests'][data_freq]
        final_url = base_url.format(currencies=currency, from_date=fromdate, to_date=todate, key=api_key)

    else:
        if type(ticker_name)==list:
            for i in ticker_name:
                symbol = config['tickers'][i]
                final_url = base_url.format(symbol=symbol,key=api_key,from_date=fromdate,to_date=todate)
                final_urls.append(final_url)

    final_urls.append(final_url)

    if len(final_urls)==1:
        return final_urls[0]
    return final_urls


if __name__ == "__main__":

    # Define parameters
    fromdate = '2024-11-04'
    todate = '2025-02-05'

    # Check the system type to ensure correct paths
    if check_system() == 'macOS':
        config_path = '/Users/macbook/Mirror/trading_algorithm/config/config_file.yml'

    else:
        config_path = 'C:\\Users\\viren\\DSML projects\\trading_alg\\config\\config_file.yml'

    final_url = construct_urls(config_path=config_path, key_name='stock_key',data_freq='forex_light', ticker_name=['apple'], fromdate=fromdate, todate=todate, currency='EURUSD')

    json_data_output = get_jsonparsed_data(final_url)

    symbol, data = read_json_data(json_data_output)

    print('Symbol: ', symbol)
    print('Data\n', data)

    # print(get_jsonparsed_data(final_url))
    