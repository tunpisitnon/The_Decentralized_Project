from app.app import web3
from config import config
from eth_utils import to_checksum_address


class Coin_Contract:
    def __init__(self):
        self.coin_contract = web3.eth.contract(address=config.rain_address, abi=config.rain_abi)
        self.owner_wallet = "0x6AAEd57e79C25F5552DAe735f32e06D7bb7925c6"

    def get_total_supply(self):
        return self.coin_contract.functions.totalSupply().call()

    def get_balance(self, address):
        address_checked = to_checksum_address(address)
        return self.coin_contract.functions.balanceOf(address_checked).call()

    def coin_supply_left(self):
        return self.coin_contract.functions.balanceOf(self.owner_wallet).call()

    def transfer(self, address, value):
        address_checked = to_checksum_address(address)
        tx_hash = self.coin_contract.functions.transfer(address_checked, int(value)).transact({'from': self.owner_wallet})
        return tx_hash

    def spend(self, address, value):
        address_checked = to_checksum_address(address)
        tx_hash = self.coin_contract.functions.spend(address_checked, int(value)).transact({'from': self.owner_wallet})
        return tx_hash

    def get_token_symbol(self):
        symbol = self.coin_contract.functions.symbol().call()
        name = self.coin_contract.functions.name().call()
        return {
            'symbol': symbol,
            'name': name
        }
