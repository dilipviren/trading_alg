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


def construct_urls(config_path: str=None, key_name: str=None, data_freq: str=None, fromdate: str=None, todate: str=None, symbol: str = None):
    """
    Constructs API request URLs based on the provided configuration and parameters.
    This function reads a YAML configuration file to retrieve API keys, base URLs, and ticker symbols.
    It then formats and constructs one or more URLs for data extraction, depending on the specified
    data frequency and other parameters.
    Parameters:
        config_path (str): Path to the YAML configuration file.
        key_name (str): The key in the config file to retrieve the API key.
        data_freq (str): The type of data to request (e.g., 'forex', 'forex_list', 'forex_light', or others).
        ticker_name (list, optional): List of ticker names to construct URLs for (used for non-forex data).
        fromdate (str, optional): Start date for data extraction (format depends on API).
        todate (str, optional): End date for data extraction (format depends on API).
        currency (str, optional): Currency pair or code (used for forex data).
    Returns:
        str or list: A single URL string if only one URL is constructed, or a list of URL strings if multiple URLs are constructed.
    Raises:
        FileNotFoundError: If the configuration file does not exist.
        KeyError: If required keys are missing in the configuration file.
        yaml.YAMLError: If the configuration file is not a valid YAML file.
    Example:
        url = construct_urls(
            config_path='config.yaml',
            key_name='my_api_key',
            data_freq='forex',
            currency='USD/EUR'
        )
    """

    with open(config_path,'r') as file:
        config = yaml.safe_load(file)

    final_urls = []
    api_key = config['keys'][key_name]

    print(config['requests']['5min'])

    base_url = config['requests'][data_freq]


    if data_freq == 'forex_list':
        # base_url = config['requests'][data_freq]
        final_url = base_url.format(key=api_key)

    elif data_freq == 'forex':
        # base_url = config['requests'][data_freq]
        final_url = base_url.format(currencies=symbol, key=api_key)

    elif data_freq == 'forex_light':
        # base_url = config['requests'][data_freq]
        final_url = base_url.format(currencies=symbol, from_date=fromdate, to_date=todate, key=api_key)

    else:
        final_url = base_url.format(symbol=symbol,key=api_key,from_date=fromdate,to_date=todate)

        # if type(ticker_name)==list:
        #     for i in ticker_name:
        #         # symbol = config['tickers'][i]
        #         final_url = base_url.format(symbol=symbol,key=api_key,from_date=fromdate,to_date=todate)
        #         final_urls.append(final_url)

    final_urls.append(final_url)

    if len(final_urls)==1:
        return final_urls[0]
    return final_urls


if __name__ == "__main__":

    # Check the system type to ensure correct paths
    if check_system() == 'macOS':
        config_path = '/Users/macbook/Mirror/trading_algorithm/config/config_file.yml'

    else:
        config_path = 'C:\\Users\\viren\\DSML projects\\trading_alg\\config\\config_file.yml'

    # Define parameters
    fromdate = '2024-11-04'
    todate = '2025-02-05'

    final_url = construct_urls(config_path=config_path, key_name='stock_key',data_freq='forex_light', ticker_name=['apple'], fromdate=fromdate, todate=todate, symbol='EURUSD')

    json_data_output = get_jsonparsed_data(final_url)

    symbol, data = read_json_data(json_data_output)

    print('Symbol: ', symbol)
    print('Data\n', data)

    # print(get_jsonparsed_data(final_url))
    