from flask import Flask
from web3 import Web3
from config import config


app = Flask(__name__)
app.config.from_object(config)

web3 = Web3(Web3.HTTPProvider(config.GANACHE_URL))
web3.eth.defaultAccount = web3.eth.accounts[0]
