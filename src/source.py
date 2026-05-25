import pandas as pd
from SmartApi import SmartConnect
import pyotp
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from data_pipeline.data_prep import Data_preparation

class Client_side:
    # --- Creates session and return client and refresh token ---
    def create_session(credentials):
        api_key = credentials[0]
        client_id = credentials[1]
        password = credentials[2]
        totp_secret = credentials[3]

        totp = pyotp.TOTP(totp_secret).now()

        client = SmartConnect(api_key=api_key)

        data = client.generateSession(client_id, password, totp)

        client.setAccessToken(data["data"]["jwtToken"])

        refreshToken = data["data"]["refreshToken"]

        return client,refreshToken
    
    # --- Reconnecting the session, if it was expired ---
    def refresh_session(client,refreshToken):
        data = client.generateSession(refreshToken)
        client.setAccessToken(data["data"]["jwtToken"])
        return client
    


class data_side:
    # --- loading 3 months data to calculate moving averages ---
    def data_loading(client,symbol,symbol_token,credentials,refreshToken):

        now = datetime.now()
        start = now - relativedelta(months=3)

        from_date = start.strftime("%Y-%m-%d %H:%M")
        to_date = now.strftime("%Y-%m-%d %H:%M")

        params = {
            "exchange": "NSE",
            "tradingsymbol": symbol,
            "symboltoken": symbol_token,
            "interval": "FIFTEEN_MINUTE",
            "fromdate": from_date,
            "todate": to_date
        }

        # --- Checking the reponse ---
        candles , client , refreshToken = data_side.check_API_reponse(params,client,refreshToken,credentials)

        df = pd.DataFrame(
            candles["data"],
            columns=["datetime", "open", "high", "low", "close", "volume"]
        )

        raw_data_path = "data/raw_data.csv"
        df.to_csv(raw_data_path)

        return raw_data_path, client, refreshToken
    

    
    # --- Checking if API response vaild or not---
    def check_API_reponse(params,client,refreshToken,credentials):
        try:
            candles = client.getCandleData(params)

            if not candles or not candles.get("data"):
                raise Exception("Invalid API response")

            return candles, client, refreshToken

        # --- if response is not vaild Refresh the session ---
        except Exception as e:
            print("API failed → trying refresh...")

            try:
                client, refreshToken = Client_side.refresh_session(client, refreshToken)

                candles = client.getCandleData(params)

                if not candles or not candles.get("data"):
                    raise Exception("Invalid after refresh")

                print("Session refreshed successfully")
                return candles, client, refreshToken

            # --- if Refresh doesn't solve the problem, Reloging again ---
            except Exception as e:
                print("Refresh failed → logging in again...")

                client, refreshToken = Client_side.create_session(credentials)

                candles = client.getCandleData(params)

                print("New session created")
                return candles, client, refreshToken
            

    # --- Load the new candle and concate it with Raw data ---
    def check_latest(raw_data_path,client,symbol_token,credentials,refreshToken):
        raw_data = pd.read_csv(raw_data_path)

        now = datetime.now()
        start = now - timedelta(minutes=60)

        params = {
                "exchange": "NSE",
                "symboltoken": symbol_token,
                "interval": "FIFTEEN_MINUTE",
                "fromdate": start.strftime("%Y-%m-%d %H:%M"),
                "todate": now.strftime("%Y-%m-%d %H:%M")
            }
        
        candles , client , refreshToken = data_side.check_API_reponse(params,client,refreshToken,credentials)
        last_candle = candles["data"][-1]

        new_row = pd.DataFrame(
            [last_candle],
            columns=["datetime", "open", "high", "low", "close", "volume"]
        )

        # --- Skip the concate if last candle matches ---
        if last_candle[0] == raw_data["datetime"].iloc[-1]:
            prep_data_path = "data/prep_data.csv"
            return prep_data_path,client
        
        else:
            raw_data = pd.concat([raw_data,new_row],ignore_index=True)
            raw_data.to_csv("data/raw_data.csv")
            prep_data_path = Data_preparation.preparation("data/raw_data.csv")
                
            return prep_data_path,client,refreshToken