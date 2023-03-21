from backend.app.app import app, web3
from backend.config import config


class Wood_Contract:

    def __init__(self):
        self.wood_contract = web3.eth.contract(address=config.Tree_address, abi=config.Tree_abi)

    def hello(self):
        return 'yes? from Wood_Contract'
