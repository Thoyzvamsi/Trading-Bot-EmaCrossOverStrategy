import pandas as pd
from SmartApi import SmartConnect
import pyotp
from datetime import datetime
from dateutil.relativedelta import relativedelta

class Get_data:
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
    
    def refresh_session(client,refreshToken):
        
        data = client.generateSession(refreshToken)
        client.setAccessToken(data["data"]["jwtToken"])
        return client

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

        try:
            candles = client.getCandleData(params)
        except Exception as e:
            print("Refreshing session")
            try:
                client = Get_data.refresh_session(client,refreshToken)
                candles = client.getCandleData(params)
            except:
                client,refreshToken = Get_data.create_session(credentials)
                candles = client.getCandleData(params)


        df = pd.DataFrame(
            candles["data"],
            columns=["datetime", "open", "high", "low", "close", "volume"]
        )

        df.to_csv("data/normal_data/raw_data.csv")

        return "data/normal_data/raw_data.csv", client,refreshToken