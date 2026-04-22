from data_pipeline.strategy import Strategy
from src.source import Get_data


symbol = ""
symbol_token = ""
credentials = []
quntity = 1

client, refreshToken = Get_data.create_session(credentials)

raw_data_path,client,refreshToken = Get_data.data_loading(client,symbol ,symbol_token ,credentials ,refreshToken )
Strategy.strategy_execution(raw_data_path,quntity ,credentials ,client ,symbol ,symbol_token ,refreshToken )