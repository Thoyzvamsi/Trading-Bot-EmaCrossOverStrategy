from data_pipeline.strategy import Strategy
from src.source import Client_side


symbol = ""
symbol_token = ""
credentials = []
quntity = 1

client, refreshToken = Client_side.create_session(credentials)

raw_data_path,client,refreshToken = Client_side.data_loading(client,symbol ,symbol_token ,credentials ,refreshToken )
Strategy.strategy_execution(raw_data_path,quntity ,credentials ,client ,symbol ,symbol_token ,refreshToken )