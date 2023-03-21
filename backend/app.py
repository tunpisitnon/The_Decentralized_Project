from flask import Flask
from web3 import Web3
from backend.config import config

from backend.contract.Contract_Wood import Contract_Wood


app = Flask(__name__)
app.config.from_object(config)


web3 = Web3(Web3.HTTPProvider(config['GANACHE_URL']))
web3.eth.defaultAccount = web3.eth.accounts[0]


contract_wood = Contract_Wood()


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/get_total_logs', methods=['GET'])
def get_total_logs():
    return contract_wood.get_total_logs()


if __name__ == "__main__":
    app.run(debug=True)

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
