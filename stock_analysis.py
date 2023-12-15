import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def download_stock_data(symbol, period, interval):
    try:
        data = yf.download(tickers=symbol, period=period, interval=interval)
        return data
    except Exception as e:
        logging.error(f"Error downloading data for {symbol}: {e}")
        return None

def calculate_stock_metrics(data):
    if data is not None and not data.empty:
        maximum_close = data['Close'].max()
        minimum_close = data['Close'].min()
        current_close = data['Close'].iloc[-1]

        max_min_percent = ((maximum_close - minimum_close) / maximum_close) * 100
        current_max_percent = ((current_close - maximum_close) / current_close) * 100
        current_min_percent = ((current_close - minimum_close) / current_close) * 100

        return maximum_close, minimum_close, current_close, max_min_percent, current_max_percent, current_min_percent
    else:
        return None, None, None, None, None, None

def process_stock(symbol, period, interval):
    data = download_stock_data(symbol, period, interval)
    return calculate_stock_metrics(data)

def main():
    readStockCSV = pd.read_csv('allStocks.csv')
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")

    results_df = pd.DataFrame(columns=['Symbol', 'Maximum Close', 'Minimum Close', 'Current Close', 'Max-Min %', 'Current-Max %', 'Current-Min %', 'Date'])

    for symbol in readStockCSV['Symbol']:
        max_close, min_close, cur_close, mm_percent, cm_percent, cmin_percent = process_stock(symbol, '1y', '1d')

        if max_close is not None:
            new_row = {
                'Symbol': symbol, 
                'Maximum Close': max_close, 
                'Minimum Close': min_close, 
                'Current Close': cur_close, 
                'Max-Min %': mm_percent, 
                'Current-Max %': cm_percent, 
                'Current-Min %': cmin_percent, 
                'Date': current_date
            }
            results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)

        else:
            logging.info(f"No data for {symbol}")

    results_df.to_csv(f'stockMarketResults_{current_date}.csv', index=False)

if __name__ == "__main__":
    main()
