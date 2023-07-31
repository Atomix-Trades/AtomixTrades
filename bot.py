import time
import traceback
import pandas as pd
import ccxt
import mysql.connector
import numpy as np

# MySQL connection details
db_host = 'localhost'
db_database = 'form'
db_user = 'root'  # Update with your MySQL username
db_password = ''  # Update with your MySQL password

# Fetch user information from the database
db_connection = mysql.connector.connect(
    host=db_host,
    database=db_database,
    user=db_user,
    password=db_password
)
db_cursor = db_connection.cursor()
select_query = "SELECT exchange_id, api_key, secret, password_app, asset_name, trade_type, trade_size, timeframe, indicator FROM newusers"
db_cursor.execute(select_query)
user_data = db_cursor.fetchone()
db_cursor.close()
db_connection.close()

# User information
if user_data:
    exchange_id, api_key, secret, password, asset_name, trade_type, trade_size, timeframe, indicator = user_data
else:
    print("No user information found in the database.")
    exit()

# Exchange configuration
exchange_class = getattr(ccxt, exchange_id, None)
exchange = exchange_class({
    'apiKey': api_key,
    'secret': secret,
    'password': password,
    'enableRateLimit': True,
})



# Trading parameters
ASSET_NAME = asset_name
TRADE_TYPE = trade_type
TRADE_SIZE_CONTRACTS = trade_size
FETCHING_LIMIT = 100
TRADE_INTERVAL = 10

# Indicator parameters
selected_indicator = indicator

# Global variables
last_execution_time = 0
trade_started = False



# def calculate_rsi(close_prices, window=14):
#     price_diff = close_prices.diff()
#     up_prices = price_diff.where(price_diff > 0, 0)
#     down_prices = -price_diff.where(price_diff < 0, 0)
#     avg_gain = up_prices.rolling(window=window).mean()
#     avg_loss = down_prices.rolling(window=window).mean()

#     # Add protection to avoid division by zero
#     rs = avg_gain / avg_loss
#     rs = rs.replace([np.inf, -np.inf], np.nan).fillna(1.0)

#     rsi = 100 - (100 / (1 + rs))
#     return rsi

def calculate_macd(close_prices, fast_period=12, slow_period=26, signal_period=9):
    macd = close_prices.ewm(span=fast_period, adjust=False).mean() - close_prices.ewm(span=slow_period, adjust=False).mean()
    signal = macd.ewm(span=signal_period, adjust=False).mean()
    histogram = macd - signal
    return macd, signal, histogram

def calculate_bb_upper(close_prices, window=20, num_std=2):
    sma = close_prices.rolling(window=window).mean()
    std = close_prices.rolling(window=window).std()
    bb_upper = sma + num_std * std
    return bb_upper

def calculate_sma(close_prices, window=20):
    sma = close_prices.rolling(window=window).mean()
    return sma

def calculate_ema(close_prices, window=20):
    ema = close_prices.ewm(span=window, adjust=False).mean()
    return ema


def fetch_historical_prices(asset_name, timeframe, limit):
    # Fetch historical OHLCV data
    ohlcv = exchange.fetch_ohlcv(asset_name, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


def execute_buy_spot():
    try:
        market_price = exchange.fetch_ticker(ASSET_NAME)['close']
        buy_price = market_price

        # Check account balance
        account_balance = exchange.fetch_balance()
        assets = ASSET_NAME.split('/')
        asset_base = assets[0]
        asset_quote = assets[1]

        base_balance = account_balance['total'].get(asset_base, 0)
        quote_balance = account_balance['total'].get(asset_quote, 0)

        order = exchange.create_order(
            symbol=ASSET_NAME,
            side='buy',
            type='limit',
            amount=TRADE_SIZE_CONTRACTS,
            price=buy_price
        )

        print(ASSET_NAME + ' bought at ' + str(buy_price) + ' in the ' + TRADE_TYPE + ' market.')
        print('Order details:', order)
        return True

    except Exception as e:
        print('Error occurred during buying: ' + str(e))
        traceback.print_exc()
        return False

def execute_sell_spot():
    try:
        market_price = exchange.fetch_ticker(ASSET_NAME)['close']
        sell_price = market_price

        order = exchange.create_order(
            symbol=ASSET_NAME,
            side='sell',
            type='limit',
            amount=TRADE_SIZE_CONTRACTS,
            price=sell_price
        )

        print(ASSET_NAME + ' sold at ' + str(sell_price) + ' in the ' + TRADE_TYPE + ' market.')
        print('Order details:', order)
        return True

    except Exception as e:
        print('Error occurred during selling: ' + str(e))
        traceback.print_exc()
        return False


def execute_buy_futures():
    try:
        market_price = exchange.fetch_ticker(ASSET_NAME)['close']
        buy_price = market_price

        # Check account balance
        account_balance = exchange.fetch_balance()
        assets = ASSET_NAME.split('/')
        asset_base = assets[0]
        asset_quote = assets[1]

        base_balance = account_balance['total'].get(asset_base, 0)
        quote_balance = account_balance['total'].get(asset_quote, 0)

        # if base_balance < TRADE_SIZE_CONTRACTS:
        #     print('Insufficient balance for buying ' + asset_base + ' in ' + TRADE_TYPE)
        #     return False

        # if quote_balance < TRADE_SIZE_CONTRACTS * buy_price:
        #     print('Insufficient balance for buying ' + asset_quote + ' in ' + TRADE_TYPE)
        #     return False

        order = exchange.create_order(
            symbol=ASSET_NAME,
            side='buy',
            type='limit',
            amount=TRADE_SIZE_CONTRACTS,
            price=buy_price
        )

        print(ASSET_NAME + ' bought at ' + str(buy_price) + ' in the ' + TRADE_TYPE + ' market.')
        print('Order details:', order)
        return True

    except Exception as e:
        print('Error occurred during buying: ' + str(e))
        traceback.print_exc()
        return False


def execute_sell_futures():
    try:
        market_price = exchange.fetch_ticker(ASSET_NAME)['close']
        sell_price = market_price

        order = exchange.create_order(
            symbol=ASSET_NAME,
            side='sell',
            type='limit',
            amount=TRADE_SIZE_CONTRACTS,
            price=sell_price
             
        )

        print(ASSET_NAME + ' sold at ' + str(sell_price) + ' in the ' + TRADE_TYPE + ' market.')
        print('Order details:', order)
        return True

    except Exception as e:
        print('Error occurred during selling: ' + str(e))
        traceback.print_exc()
        return False
def calculate_pnl():
    global total_pnl
    
    # Get account balance
    account_balance = exchange.fetch_balance()
    assets = ASSET_NAME.split('/')
    asset_base = assets[0]
    asset_quote = assets[1]

    base_balance = account_balance['total'].get(asset_base, 0)
    quote_balance = account_balance['total'].get(asset_quote, 0)

    # Get open positions
    open_positions = exchange.fetch_open_positions(ASSET_NAME)

    # Calculate PNL for each open position
    pnl_data = []
    for position in open_positions:
        if position['side'] == 'buy':
            entry_price = position['entry']
            current_price = exchange.fetch_ticker(ASSET_NAME)['close']
            pnl = (current_price - entry_price) * position['amount']
            pnl_data.append(pnl)
        elif position['side'] == 'sell':
            exit_price = position['entry']
            current_price = exchange.fetch_ticker(ASSET_NAME)['close']
            pnl = (exit_price - current_price) * position['amount']
            pnl_data.append(pnl)

    # Calculate total PNL by summing the pnl_data list
    total_pnl = sum(pnl_data)


def main():
    global last_execution_time, trade_started

    while True:
        try:
             # Fetch account balance
            account_balance = exchange.fetch_balance()
            assets = ASSET_NAME
            asset_base = assets[0]
            asset_quote = assets[1]

            base_balance = account_balance['total'].get(asset_base, 0)

            if base_balance > TRADE_SIZE_CONTRACTS:  # Check if the asset is already bought
                print('Asset already bought, checking for sell condition.')
                # Fetch historical prices
                historical_prices = fetch_historical_prices(ASSET_NAME, '1m', FETCHING_LIMIT)
            # Fetch historical prices
            historical_prices = fetch_historical_prices(ASSET_NAME, '1h', FETCHING_LIMIT)
            close_prices = historical_prices['close']

            # Calculate indicators
            # rsi = calculate_rsi(close_prices)
            macd, signal, histogram = calculate_macd(close_prices)
            bb_upper = calculate_bb_upper(close_prices)
            sma = calculate_sma(close_prices)
            ema = calculate_ema(close_prices)

            # Get the last indicator values
            # if not rsi.empty and len(rsi) >= 2:  # Check if the rsi DataFrame is not empty and has at least 2 elements
            #     last_rsi = rsi.iloc[-1]
            #     second_last_rsi = rsi.iloc[-2]
            # else:
            #     last_rsi = None
            #     second_last_rsi = None
            # Get the last indicator values
            rsi_data = exchange.fetch_ohlcv(ASSET_NAME, timeframe='1d', limit=14)
            rsi = pd.Series([data[-1] for data in rsi_data])
            last_rsi = rsi.iloc[-1]
            last_macd = macd.iloc[-1]
            last_bb_upper = bb_upper.iloc[-1]
            last_sma = sma.iloc[-1]
            last_ema = ema.iloc[-1]
                        
            print(last_rsi)
            # Check RSI for buy and sell conditions
            if selected_indicator== 'rsi' and not trade_started and last_rsi <= 30:    
                print(last_rsi)          
                if TRADE_TYPE == 'spot':
                    execute_buy_spot()
                elif TRADE_TYPE == 'futures':
                    execute_buy_futures()
                trade_started = True
            elif selected_indicator=='rsi' and not trade_started and last_rsi >= 70:
                print(last_rsi)
                # Execute sell order
                if TRADE_TYPE == 'spot':
                    execute_sell_spot()
                    trade_started = False
                elif TRADE_TYPE == 'futures':
                    execute_sell_futures()
                trade_started = False

            # # Check MACD for buy and sell conditions
            if selected_indicator== 'macd' and macd[-1] > signal[-1] and macd[-2] <= signal[-2]:
                if not trade_started:
                    print('MACD crossover occurred. Opening trade...')
                    trade_started = True
                    last_execution_time = time.time()

                    if TRADE_TYPE == 'spot':
                        execute_buy_spot()
                    elif TRADE_TYPE == 'futures':
                        execute_buy_futures()

            elif selected_indicator == 'macd' and macd[-1] < signal[-1] and macd[-2] >= signal[-2]:
                if trade_started:
                    print('MACD crossunder occurred. Closing trade...')
                    trade_started = False
                    last_execution_time = time.time()

                    if TRADE_TYPE == 'spot':
                        execute_sell_spot()
                    elif TRADE_TYPE == 'futures':
                        execute_sell_futures()

            # Wait for the next interval
            elapsed_time = time.time() - last_execution_time
            if elapsed_time < 900:  
                time.sleep(900 - elapsed_time)



            # Check Bollinger Bands upper for buy and sell conditions
            if selected_indicator == 'bb_upper' and not trade_started and close_prices.iloc[-1] > last_bb_upper:
                # Execute buy order
                if TRADE_TYPE == 'spot':
                    execute_buy_spot()
                elif TRADE_TYPE == 'futures':
                    execute_buy_futures()
                trade_started = True
            elif selected_indicator == 'bb_upper' and trade_started and close_prices.iloc[-1] < last_bb_upper:
                # Execute sell order
                if TRADE_TYPE == 'spot':
                    execute_sell_spot()
                elif TRADE_TYPE == 'futures':
                    execute_sell_futures()
                trade_started = False

            # # Check SMA for buy and sell conditions
            if selected_indicator == 'sma' and not trade_started and close_prices.iloc[-1] > last_sma:
                # Execute buy order
                if TRADE_TYPE == 'spot':
                    execute_buy_spot()
                elif TRADE_TYPE == 'futures':
                    execute_buy_futures()
                trade_started = True
            elif selected_indicator == 'sma' and trade_started and close_prices.iloc[-1] < last_sma:
                # Execute sell order
                if TRADE_TYPE == 'spot':
                    execute_sell_spot()
                elif TRADE_TYPE == 'futures':
                    execute_sell_futures()
                trade_started = False

            # # Check EMA for buy and sell conditions
            if selected_indicator == 'ema' and not trade_started and close_prices.iloc[-1] > last_ema:
                # Execute buy order
                if TRADE_TYPE == 'spot':
                    execute_buy_spot()
                elif TRADE_TYPE == 'futures':
                    execute_buy_futures()
                trade_started = True
            elif selected_indicator == 'ema' and trade_started and close_prices.iloc[-1] < last_ema:
                # Execute sell order
                if TRADE_TYPE == 'spot':
                    execute_sell_spot()
                elif TRADE_TYPE == 'futures':
                    execute_sell_futures()
                trade_started = False

            # Sleep for trade interval
            time.sleep(TRADE_INTERVAL)
        except Exception as e:
            print('An error occurred:', str(e))
            traceback.print_exc()
            break
if __name__ == "__main__":
    main()