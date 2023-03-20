import json


class config:
    GANACHE_URL = 'HTTP://127.0.0.1:7545'

    ABI_FILE = json.load(open('contract_abi.json'))

    Tree_abi = ABI_FILE['tree']['abi']
    rain_abi = ABI_FILE['rainCoins']['abi']
    player_abi = ABI_FILE['player']['abi']

    Tree_address = ABI_FILE['tree']['address']
    rain_address = ABI_FILE['rainCoins']['address']
    player_address = ABI_FILE['player']['address']
