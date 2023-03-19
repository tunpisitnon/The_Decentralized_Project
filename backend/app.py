# Flask code to interact with the token contract using Web3
from flask import Flask, jsonify
from web3 import Web3
from web3.middleware import geth_poa_middleware

app = Flask(__name__)

# Connect to the local Ethereum node
w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))

# Add the POA middleware if using the POA network
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Load the contract ABI
with open('Mytoken.json', 'r') as f:
    abi = f.read()

# Create a contract instance

owner_account = w3.eth.accounts[0]

contract_address = '0x24D81555Fe8F7BF4f1ED9793bD26ca6511CBfc52'  # Replace with your actual contract address
contract = w3.eth.contract(address=contract_address, abi=abi)


# Define a function to get the balance of an address
@app.route('/balance/<address>')
def get_balance(address):
    balance = contract.functions.balanceOf(address).call()
    return jsonify({'balance': balance})


@app.route('/total_supply')
def get_total_supply():
    total_supply = contract.functions.totalSupply().call()
    return jsonify({'total_supply': total_supply})


@app.route('/balance/all')
def get_all_balances():
    addresses = ['0xE3f7f4Ee2c9CBA9eCEAC2d77EA1A85cF714451AF',
                 '0x4E0F94488c9b06aa2365c52Fc15BFCFc9813a728',
                 '0x564bF71166c364B5159FF7419a40A3016A8ea1bD',
                 '0x68fF3d7610b33Ea0E35A187A49AEF952b6a9AaA6',
                 '0xcA541f386fE006898b42EbBFEeb70DC673DF44CC']  # Replace with actual addresses
    balances = {}
    for address in addresses:
        balance = contract.functions.balanceOf(address).call()
        balances[address] = balance
    return jsonify(balances)


@app.route('/transfer/<to>/<amount>')
def transfer(to, amount):
    tx_hash = contract.functions.transfer(to, amount).transact({'from': owner_account})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    return jsonify({'tx_receipt': tx_receipt})


if __name__ == '__main__':
    app.run(debug=True)
