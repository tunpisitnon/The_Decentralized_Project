from backend.contract.Contract_Wood import Wood_Contract
from backend.contract.Contract_Coin import Coin_Contract

from backend.app.app import app

from flask import jsonify, request

wood_contract = Wood_Contract()
coin_contract = Coin_Contract()


@app.route('/')
def hello_world():
    return jsonify({'status_code': 200, 'status': 'success'})


@app.route('/wood/total_supply', methods=['GET'])
def wood():
    return jsonify({'total wood supply': wood_contract.get_total_supply()})


@app.route('/wood/supply_left', methods=['GET'])
def wood_supply_left():
    return jsonify({'wood supply left': wood_contract.wood_supply_left()})


@app.route('/wood/balance/<address>', methods=['GET'])
def wood_balance(address):
    _address = address
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


@app.route('/wood/check_player_status/<address>', methods=['GET'])
def check_player_status(address):
    _address = address
    return jsonify(wood_contract.check_player_status(_address))


@app.route('/wood/cutting_wood', methods=['POST'])
def cutting_wood():
    request_data = request.get_json()
    _address = request_data['address']
    return jsonify({'cutting wood': wood_contract.cutting_wood(_address)})


@app.route('/wood/spending_wood/', methods=['POST'])
def spending_wood():
    request_data = request.get_json()
    _address, _value = request_data['address'], int(request_data['value'])
    result = wood_contract.Spending_Wood(_address, _value)
    if result['status'] == 'success':
        tx = coin_contract.transfer(_address, _value)
        return jsonify({'spending wood': str(_value) + ' woods',
                        'tx_hash': tx.hex(),
                        'Raindrops': coin_contract.get_balance(_address)
                        })
    else:
        return {"status": "you don't have enough wood"}


@app.route('/coin/raindrop/<address>', methods=['GET'])
def raindrop(address):
    _address = address
    raindrops = coin_contract.get_balance(_address)
    return jsonify({
        'raindrop': raindrops
    })


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


if __name__ == '__main__':
    app.run(debug=True)
