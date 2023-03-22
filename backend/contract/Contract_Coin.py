from backend.app.app import web3
from backend.config import config


class Coin_Contract:
    def __init__(self):
        self.coin_contract = web3.eth.contract(address=config.rain_address, abi=config.rain_abi)
        self.owner_wallet = "0x6AAEd57e79C25F5552DAe735f32e06D7bb7925c6"

    def get_total_supply(self):
        return self.coin_contract.functions.totalSupply().call()

    def get_balance(self, address):
        return self.coin_contract.functions.balanceOf(address).call()

    def wood_supply_left(self):
        return self.coin_contract.functions.balanceOf(self.owner_wallet).call()

    def transfer(self, address, value):
        tx_hash = self.coin_contract.functions.transfer(address, int(value)).transact({'from': self.owner_wallet})
        return tx_hash

    def spend(self, address, value):
        tx_hash = self.coin_contract.functions.spend(address, int(value)).transact({'from': self.owner_wallet})
        return tx_hash