import certifi
import json
import yaml
try:
    from urllib.request import urlopen
except ImportError:
    print('Error: Could not import urlopen from urllib.request')   

key_path = '/Users/macbook/Mirror/trading_algorithm/config/api_key.yml'
requests_path = '/Users/macbook/Mirror/trading_algorithm/config/request_urls.yml'

test_url = 'https://financialmodelingprep.com/stable/historical-chart?symbol=AAPL&apikey={key}'

test_url2 = "https://financialmodelingprep.com/stable/historical-price-eod/light?symbol=AAPL&from=2024-11-04&apikey={key}"


def get_jsonparsed_data(url):
    '''Function that fetches the data from request url'''
    response = urlopen(url, cafile=certifi.where())
    data = response.read().decode("utf-8")
    return json.loads(data)


if __name__ == "__main__":

    fromdate = '2024-11-04'
    todate = '2025-02-05'
    
    with open(key_path,'r') as file:
        api_key = yaml.safe_load(file)
        api_key = api_key['key']

    with open(requests_path,'r') as file:
        urls = yaml.safe_load(file)

    base_url = urls['requests']['5min']
    final_url = base_url.format(symbol = 'AAPL',key = api_key)

    print(get_jsonparsed_data(test_url2.format(key = api_key, 
                                               fromdate = fromdate, 
                                               todate = todate, 
                                               symbol = 'AAPL')))
    