import pandas as pd

class Data_preparation:
    def preparation(raw_data_path):
        data = pd.read_csv(raw_data_path)

        if data is None:
            print("Raw data has a Problem")
            return

        data = data.rename(columns={
                                    "close" : "Close",
                                    "open" : "Open",
                                    "high" : "High",
                                    "low" : "Low",
                                    "volume" : "Volume"
                                    })

        data["datetime"] = pd.to_datetime(data["datetime"])

        data["Date"] = data["datetime"].dt.date
        data["Time"] = data["datetime"].dt.time

        data.drop(columns=["datetime"], inplace=True)

        data['EMA_14'] = data['Close'].ewm(span=14, adjust=False).mean()
        data['EMA_50'] = data['Close'].ewm(span=50, adjust=False).mean()

        data = data.dropna()

        # Signals
        data['Signal'] = 0
        data.loc[data['EMA_14'] > data['EMA_50'], 'Signal'] = 1
        data.loc[data['EMA_14'] < data['EMA_50'], 'Signal'] = -1

        data['Position'] = data['Signal'].diff()

        data.to_csv("data/normal_data/prep_data.csv",index = False)

        return "data/normal_data/prep_data.csv"
