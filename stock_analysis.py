import numpy as np
import pandas as pd
import yfinance as yf
import datetime
import logging
import os
import csv

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
    try:
        # Try with .NS suffix
        data = download_stock_data(symbol + '.NS', period, interval)
        if data is None or data.empty:
            # If no data, try with -SM.NS suffix
            data = download_stock_data(symbol + '-SM.NS', period, interval)
        return calculate_stock_metrics(data)
    except Exception as e:
        logging.error(f"Error processing data for {symbol}: {e}")
        return None, None, None, None, None, None



def main():
    readStockCSV = pd.read_csv('allStocks.csv')
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    output_file = f'stockMarketResults_{current_date}.csv'

    # Check if the file already exists
    file_exists = os.path.isfile(output_file)

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
            # Append the new row to the CSV file
            with open(output_file, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=new_row.keys())
                
                # Write header only if the file is being created for the first time
                if not file_exists:
                    writer.writeheader()
                    file_exists = True
                
                writer.writerow(new_row)
        else:
            logging.info(f"No data for {symbol}")

if __name__ == "__main__":
    main()
