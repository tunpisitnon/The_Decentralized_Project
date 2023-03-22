import json


class config:
    GANACHE_URL = 'HTTP://127.0.0.1:7545'

    ABI_FILE = json.load(open('contract_abi.json', 'r'))

    Tree_abi = ABI_FILE['tree']['abi']
    rain_abi = ABI_FILE['rainCoins']['abi']

    Tree_address = ABI_FILE['tree']['address']
    rain_address = ABI_FILE['rainCoins']['address']
