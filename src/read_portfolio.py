import pandas as pd


def read_portfolio(path: str):
    if path[-4:] != '.csv':
        raise ValueError
    else:
        portfolio_df = pd.read_csv(path)

    return portfolio_df
    

if __name__ == '__main__':
    test_path = 'C:\\Users\\viren\\DSML projects\\trading_alg\\portfolio.csv'

    portfolio_df = pd.read_csv(test_path)
    print(portfolio_df)

