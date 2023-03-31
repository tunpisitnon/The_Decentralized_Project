from contract.Contract_Wood import Wood_Contract
from contract.Contract_Coin import Coin_Contract

from app.app import app

from flask import jsonify, request

wood_contract = Wood_Contract()
coin_contract = Coin_Contract()


@app.route('/')
def hello_world():
    return jsonify({'status_code': 200, 'status': 'success'})


@app.route('/wood/total_supply', methods=['GET'])
def wood():
    return jsonify({'total_wood_supply': wood_contract.get_total_supply()})


@app.route('/wood/supply_left', methods=['GET'])
def wood_supply_left():
    return jsonify({'wood_supply_left': wood_contract.wood_supply_left()})


@app.route('/wood/balance', methods=['POST'])
def wood_balance():
    request_data = request.get_json()
    _address = request_data['address']
    return jsonify({'wood balance': wood_contract.get_balance(_address)})


@app.route('/wood/initial_player', methods=['POST'])
def initial_player():
    request_data = request.get_json()
    _address = request_data['address']
    result = wood_contract.check_player_status(_address)
    if result['player_status']['mana'] == 0:
        init_result = wood_contract.initial_player(_address)
        return jsonify({'initial_player': 'Player created successfully',
                        'tx_hash': init_result})
    else:
        return jsonify({'initial_player': 'Player already exists'})


@app.route('/wood/check_player_status/', methods=['POST'])
def check_player_status():
    request_data = request.get_json()
    _address = request_data['address']
    return jsonify(wood_contract.check_player_status(_address))


@app.route('/wood/cutting_wood', methods=['POST'])
def cutting_wood():
    request_data = request.get_json()
    _address = request_data['address']
    return jsonify({'cutting wood': wood_contract.cutting_wood(_address)})


@app.route('/wood/spending_wood/', methods=['POST'])
def spending_wood():
    request_data = request.get_json()
    wood_total_supply = wood_contract.get_total_supply()
    wood_supply_left = wood_contract.wood_supply_left()

    _address, _value = request_data['address'], int(request_data['value'])

    wood_left_percentage = round(100 - ((wood_supply_left / wood_total_supply) * 100), 4)
    wood_left_percentage = round((wood_left_percentage * 100) + 1)

    result = wood_contract.Spending_Wood(_address, _value)

    if result['status'] == 'success':

        new_value = wood_left_percentage * _value
        tx = coin_contract.transfer(_address, new_value)

        return jsonify({'spending wood': str(_value) + ' woods',
                        'Raindrops': new_value,
                        'tx_hash': tx.hex(),
                        'Raindrops_from_contract': coin_contract.get_balance(_address)
                        })
    else:
        return {"status": "you don't have enough wood"}


@app.route('/coin/raindrop/', methods=['POST'])
def raindrop():
    request_data = request.get_json()
    _address = request_data['address']
    raindrops = coin_contract.get_balance(_address)
    return jsonify({
        'raindrop': raindrops
    })


@app.route('/coin/total_supply', methods=['GET'])
def raindrop_total_supply():
    return jsonify({'total raindrop supply': coin_contract.get_total_supply()})


@app.route('/coin/supply_left', methods=['GET'])
def raindrop_supply_left():
    return jsonify({'raindrop supply left': coin_contract.coin_supply_left()})


@app.route('/coin/balance', methods=['POST'])
def raindrop_balance():
    request_data = request.get_json()
    _address = request_data['address']
    return jsonify({'raindrop balance': coin_contract.get_balance(_address)})


@app.route('/coin/restore_mana', methods=['POST'])
def restore_mana():
    request_data = request.get_json()
    _address = request_data['address']
    _value = int(request_data['value'])
    raindrops = coin_contract.get_balance(_address)
    if raindrops < int(_value):
        return jsonify({'status': 'You do not have enough raindrops'})
    else:
        tx_spend = coin_contract.spend(_address, _value)
        tx_restore_mana = wood_contract.restore_mana(_address, _value)

        raindrops_after_spend = coin_contract.get_balance(_address)
        player_status = wood_contract.check_player_status(_address)

    return jsonify({'raindrop_left': raindrops_after_spend,
                    'tx_spend_hash': tx_spend.hex(),
                    'tx_restore_mana_hash': tx_restore_mana,
                    'player_status': player_status['player_status'],
                    })


@app.route('/check_price_token', methods=['GET'])
def check_price_token():
    wood_total_supply = wood_contract.get_total_supply()
    wood_supply_left = wood_contract.wood_supply_left()

    wood_left_percentage = round(100 - ((wood_supply_left / wood_total_supply) * 100), 4)
    wood_left_percentage = round((wood_left_percentage * 100) + 1)
    return jsonify({'1 wood': str(wood_left_percentage) + " raindrops"})


@app.route('/wood/check_token_symbol', methods=['GET'])
def check_token_symbol():
    return jsonify({'token_symbol': wood_contract.get_token_symbol()})


@app.route('/coin/check_token_symbol', methods=['GET'])
def check_coin_symbol():
    return jsonify({'token_symbol': coin_contract.get_token_symbol()})


if __name__ == '__main__':
    app.run(debug=True)
