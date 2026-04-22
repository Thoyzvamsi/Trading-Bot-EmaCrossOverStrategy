import pandas as pd
import time
from src.source import Get_data
from datetime import datetime,timedelta
from data_pipeline.data_prep import Data_preparation
import json

class Strategy:
    def strategy_execution(raw_data_path,quntity,credentials,client,symbol,symbol_token):
        trade = {}
        trade_on = 0

        while True:
            data_path,client = Strategy.check_latest(raw_data_path,client,symbol_token,credentials)
            data = pd.read_csv(data_path)

            if len(data) < 3:
                continue

            if quntity > 0:
                print("Waiting for a trade....")
                
                if data["Position"].iloc[-1] == 2 and data["Position"].iloc[-2] == -2 and trade_on == 0:
                    entry = data["Close"].iloc[-1]
                    Entry_Date = data["Date"].iloc[-1]
                    trade_on = 1

                    orderparams = {
                            "variety": "NORMAL",
                            "tradingsymbol": symbol,
                            "symboltoken": symbol_token,
                            "transactiontype": "BUY",
                            "exchange": "NSE",
                            "ordertype": "MARKET",
                            "producttype": "DELIVERY",
                            "duration": "DAY",
                            "price": "0",
                            "quantity": quntity
                        }
                    client.placeOrder(orderparams)
                    

                elif data["Position"].iloc[-1] == -2 and trade_on == 1:
                    Exit_Date = data["Date"].iloc[-1]
                    exit = data["Close"].iloc[-1]
                    trade_on = 0

                    orderparams = {
                            "variety": "NORMAL",
                            "tradingsymbol": symbol,
                            "symboltoken": symbol_token,
                            "transactiontype": "SELL",
                            "exchange": "NSE",
                            "ordertype": "MARKET",
                            "producttype": "DELIVERY",
                            "duration": "DAY",
                            "price": "0",
                            "quantity": quntity
                        }
                    client.placeOrder(orderparams)

                    trade = {
                        "Stock" : symbol,
                        "Entry_Date" : Entry_Date,
                        "Exit_Date" : Exit_Date,                        
                        "Entry" : entry ,
                        "Exit" : exit ,
                        "Quantity" : quntity
                    }

                    trade_data = Strategy.load_data("trade_data.json")
                    trade_data.append(trade)

                    with open("trade_data.json","w") as f:
                        json.dump(trade_data ,f, indent=4)
                    

            time.sleep(60)

    def get_latest_candle(client, symbol_token,credentials,refreshToken):
        
        now = datetime.now()
        start = now - timedelta(minutes=60)

        params = {
                "exchange": "NSE",
                "symboltoken": symbol_token,
                "interval": "FIFTEEN_MINUTE",
                "fromdate": start.strftime("%Y-%m-%d %H:%M"),
                "todate": now.strftime("%Y-%m-%d %H:%M")
            }
        try:
            candles = client.getCandleData(params)

            if not candles or not candles.get("data"):
                raise Exception("Invalid API response")

            return candles["data"][-1], client, refreshToken

        # 🔥 LEVEL 2: Refresh token
        except Exception as e:
            print("⚠️ API failed → trying refresh...")

            try:
                client, refreshToken = Get_data.refresh_session(client, refreshToken)

                candles = client.getCandleData(params)

                if not candles or not candles.get("data"):
                    raise Exception("Invalid after refresh")

                print("✅ Session refreshed successfully")
                return candles["data"][-1], client, refreshToken

            # 🔥 LEVEL 3: Full login
            except Exception as e:
                print("⚠️ Refresh failed → logging in again...")

                client, refreshToken = Get_data.create_session(credentials)

                candles = client.getCandleData(params)

                print("✅ New session created")
                return candles["data"][-1], client, refreshToken
        
    
    def check_latest(raw_data_path,client,symbol_token,credentials,refreshToken):
        raw_data = pd.read_csv(raw_data_path)

        last_candle,client,refreshToken = Strategy.get_latest_candle(client,symbol_token,credentials,refreshToken)

        new_row = pd.DataFrame(
            [last_candle],
            columns=["datetime", "open", "high", "low", "close", "volume"]
        )

        if last_candle[0] == raw_data["datetime"].iloc[-1]:
            prep_data_path = "data/normal_data/prep_data.csv"
            return prep_data_path,client
        else:
            raw_data = pd.concat([raw_data,new_row],ignore_index=True)
            raw_data.to_csv("data/normal_data/raw_data.csv")
            prep_data_path = Data_preparation.preparation("data/normal_data/raw_data.csv")
                
            return prep_data_path,client,refreshToken

        
    def load_data(file_name):
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []