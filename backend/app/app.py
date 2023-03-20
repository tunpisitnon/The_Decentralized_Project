from flask import Flask
from web3 import Web3
from backend.config import config


app = Flask(__name__)
app.config.from_object(config)
web3 = Web3(Web3.HTTPProvider(app.config['GANACHE_URL']))
web3.eth.default_account = web3.eth.accounts[0]

# accounts = web3.eth.accounts
# address = "0x08347F4c07ae85E4A9ab31a02e962993a9a55930"
# print(accounts)
#
# with open('../contract_abi.json', 'r') as f:
#     abi = json.load(f)
#
# my_contract = web3.eth.contract(address=address, abi=abi)
#
# tx_hash = my_contract.functions.transfer(accounts[1], 100).transact({'from': accounts[0]})
# print(tx_hash.hex())
#
# tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
