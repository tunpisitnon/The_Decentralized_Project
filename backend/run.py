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


@app.route('/wood/initial_player/<address>', methods=['GET'])
def initial_player(address):
    _address = address
    check_player_status = wood_contract.check_player_status(_address)
    print(check_player_status)
    if check_player_status['player_status']['mana'] == 0:
        init_result = wood_contract.initial_player(_address)

        return jsonify({'initial_player': 'Player created successfully',
                        'tx_hash': init_result})
    else:
        return jsonify({'initial_player': 'Player already exists'})


@app.route('/wood/check_player_status/<address>', methods=['GET'])
def check_player_status(address):
    _address = address
    return jsonify(wood_contract.check_player_status(_address))


@app.route('/wood/cutting_wood/<address>', methods=['GET'])
def cutting_wood(address):
    _address = address
    return jsonify({'cutting wood': wood_contract.cutting_wood(_address)})


@app.route('/wood/spending_wood/', methods=['GET'])
def spending_wood():
    _address, _value = request.args.get('address'), request.args.get('value')
    result = wood_contract.Spending_Wood(_address, _value)
    if result['status'] == 'success':
        tx = coin_contract.transfer(_address, _value)
        return jsonify({'spending wood': _value + ' woods',
                        'tx_hash': tx.hex(),
                        'Raindrops': coin_contract.get_balance(_address)
                        })
    else:
        return {"status": "you don't have enough wood"}


if __name__ == '__main__':
    app.run(debug=True)
