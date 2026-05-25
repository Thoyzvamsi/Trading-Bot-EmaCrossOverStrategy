import pandas as pd

class Data_preparation:
    def preparation(raw_data_path):
        data = pd.read_csv(raw_data_path)

        # --- Check if data exits or Not ---
        if data is None:
            print("Raw data has a Problem")
            return
        # --- Renaming the colunms ---
        data = data.rename(columns={
                                    "close" : "Close",
                                    "open" : "Open",
                                    "high" : "High",
                                    "low" : "Low",
                                    "volume" : "Volume"
                                    })

        data["datetime"] = pd.to_datetime(data["datetime"])

        # --- Separate the date and time ---
        data["Date"] = data["datetime"].dt.date
        data["Time"] = data["datetime"].dt.time
        data.drop(columns=["datetime"], inplace=True)
        
        # --- Calculating EMA's 14 and 50 ---
        data['EMA_14'] = data['Close'].ewm(span=14, adjust=False).mean()
        data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

        data = data.dropna()

        # --- Genarating Signals ---
        data['Signal'] = 0
        data.loc[data['EMA_14'] > data['EMA_50'], 'Signal'] = 1
        data.loc[data['EMA_14'] < data['EMA_50'], 'Signal'] = -1

        data['Position'] = data['Signal'].diff()

        # --- Storing the prepared data ---
        data.to_csv("data/prep_data.csv",index = False)

        return "data/prep_data.csv"
