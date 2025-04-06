import certifi
import json
import yaml
from system_check import check_system
try:
    from urllib.request import urlopen
except ImportError:
    print('Error: Could not import urlopen from urllib.request')   

# Define parameters
fromdate = '2024-11-04'
todate = '2025-02-05'

# Check the system type to ensure correct paths
if check_system() == 'macOS':
    config_path = '/Users/macbook/Mirror/trading_algorithm/config/config_file.yml'

else:
    config_path = 'C:\\Users\\viren\\DSML projects\\trading_alg\\config\\config_file.yml'


def get_jsonparsed_data(url: str):
    '''
    Function that fetches the data from request url
    '''
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


def construct_url(config_path: str, key_name: str, data_freq: str, ticker_name: list, fromdate: str, todate: str):
    '''
    Constructs a URL for an api request from FMP
    '''
    with open(config_path,'r') as file:
        config = yaml.safe_load(file)

    final_urls = []

    api_key = config['keys'][key_name]
    base_url = config['requests'][data_freq]
    if type(ticker_name)==list:
        for i in ticker_name:
            symbol = config['tickers'][i]
            final_url = base_url.format(symbol=symbol,key=api_key,from_date=fromdate,to_date=todate)
            final_urls.append(final_url)

        if len(final_urls)==1:
            return final_urls[0]
        return final_urls


if __name__ == "__main__":

    final_url = construct_url(config_path=config_path, key_name='stock_key',data_freq='eod', ticker_name=['apple'], fromdate=fromdate, todate=todate)

    print(get_jsonparsed_data(final_url))
    