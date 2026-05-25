import pandas as pd
import time
from src.source import data_side
import json

class Strategy:
    def strategy_execution(raw_data_path,quntity,credentials,client,symbol,symbol_token,capital):
        trade = {}
        trade_on = 0
        

        while True:
            data_path,client = data_side.check_latest(raw_data_path,client,symbol_token,credentials)
            data = pd.read_csv(data_path)

            if len(data) < 3:
                continue

            if quntity > 0:
                print("Waiting for a trade....")
                
                if data["Position"].iloc[-1] == 2 and trade_on == 0:
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
                    

                elif (data["Position"].iloc[-1] == -2 or (data["Close"] - entry) <= capital * -0.01) and trade_on == 1:
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

    def charges_calulation(entry, exit, qnt ,market_type):
        charges = 0
        brokerage = 5
        if market_type == 0:
            #Brokerage
            if brokerage > 0.1 * (entry*qnt):
                charges += 10
            elif (0.1 * (entry*qnt)) < 20:
                charges += (0.1 * (entry*qnt)) + (0.1 * (exit*qnt))
            else:
                charges += 40

            #Dp charges
            charges += 20 + (0.18*20)
            #STT (Gov tax)
            charges += (0.01*entry) + (0.01*exit)
            #Stamp duty
            charges += 0.00015*entry*qnt

            if (exit - entry)*0.0325 > 0:
                charges += (exit - entry)*0.0325
            
            return charges
        
        if market_type == 1:
            #Brokerage
            if brokerage > 0.1 * (entry*qnt):
                charges += 5*2 
            elif 0.1 * (entry*qnt) < 20:
                charges += 0.1 * (entry*qnt)
            else:
                charges += 20

            #STT
            #charges += 0.025*exit
            charges += 0.00003*entry*qnt
            if ((exit - entry)*qnt)*0.0325 > 0:
                ((exit - entry)*qnt)*0.0325

            return charges
         
    def load_data(file_name):
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return []