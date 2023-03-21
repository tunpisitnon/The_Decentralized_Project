from backend import app
from backend.app import web3


class Contract_Wood:
    def __init__(self):
        self.address = app.config['Tree_address']
        self.abi = app.config['Tree_abi']
        self.contract = web3.eth.contract(address=self.address, abi=self.abi)
        self.ownerAddress = "0x6AAEd57e79C25F5552DAe735f32e06D7bb7925c6"

    def get_total_logs(self):
        return self.contract.functions.balanceOf(self.ownerAddress).call()

    def get_player_data(self, address):
        return self.contract.functions.player(address).call()
