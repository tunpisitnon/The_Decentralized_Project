from backend.app.app import app, web3
from backend.config import config


class Wood_Contract:

    def __init__(self):
        self.wood_contract = web3.eth.contract(address=config.Tree_address, abi=config.Tree_abi)
        self.owner_wallet = "0x6AAEd57e79C25F5552DAe735f32e06D7bb7925c6"

    def get_total_supply(self):
        return self.wood_contract.functions.totalSupply().call()

    def get_balance(self, address):
        return self.wood_contract.functions.balanceOf(address).call()

    def wood_supply_left(self):
        return self.wood_contract.functions.balanceOf(self.owner_wallet).call()
