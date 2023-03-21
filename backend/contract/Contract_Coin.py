from backend.app.app import app, web3
from backend.config import config


class Coin_Contract:
    def __init__(self):
        self.coin_contract = web3.eth.contract(address=config.rain_address, abi=config.rain_abi)

    def hello(self):
        return 'yes? from Coin_Contract'
