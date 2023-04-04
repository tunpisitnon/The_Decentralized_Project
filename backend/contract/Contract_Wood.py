from app.app import web3
from config import config
from eth_utils import (
    to_checksum_address
)


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

    def initial_player(self, address):
        address_checked = to_checksum_address(address)
        tx_hash = self.wood_contract.functions.initial_player(address_checked).transact({'from': self.owner_wallet})
        return tx_hash.hex()

    def check_player_status(self, address):
        address_checked = to_checksum_address(address)
        result = self.wood_contract.functions.player(address_checked).call()
        raindrop_balance = self.get_balance(address_checked)

        object = {
            'player_status': {
                'mana': result[0],
                'wood': result[1],
                'total': result[2],
                'is_created': result[3],
            }
        }
        return object

    def cutting_wood(self, address):
        address_checked = to_checksum_address(address)
        check_player_status = self.check_player_status(address_checked)
        print(check_player_status['player_status'])
        if check_player_status['player_status']['mana'] <= 0:
            return {'status': 'You need to rest for a while'}
        else:
            results = self.wood_contract.functions.Cutting_Wood(address_checked).transact({'from': self.owner_wallet})
            return results.hex()

    def Spending_Wood(self, address, value):
        address_checked = to_checksum_address(address)
        player_status = self.check_player_status(address_checked)
        if player_status['player_status']['wood'] < int(value) or player_status['player_status']['wood'] == 0:
            return {'status': 'You do not have enough wood'}
        else:
            results = self.wood_contract.functions.spending_wood(address_checked, int(value)).transact(
                {'from': self.owner_wallet})
            object = {
                'status': 'success',
                "tx_hash": results.hex(),
            }
            return object

    def restore_mana(self, address, _value):
        address_checked = to_checksum_address(address)
        tx = self.wood_contract.functions.restore_mana(address_checked, int(_value)).transact(
            {'from': self.owner_wallet})
        return tx.hex()

    def get_token_symbol(self):
        symbol = self.wood_contract.functions.symbol().call()
        name = self.wood_contract.functions.name().call()
        return {
            'symbol': symbol,
            'name': name
        }
