from backend.app import app


class Contract_Coin:
    def __init__(self):
        self.address = app.config['rain_address']
        self.abi = app.config['rain_abi']
        self.contract = web3.eth.contract(address=self.address, abi=self.abi)
        self.ownerAddress = "0x6AAEd57e79C25F5552DAe735f32e06D7bb7925c6"

    def getBalance(self):
        return self.contract.functions.balanceOf(self.ownerAddress).call()
