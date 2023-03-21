from backend.contract.Contract_Wood import Wood_Contract
from backend.contract.Contract_Coin import Coin_Contract

from backend.app.app import app

from flask import jsonify, request

wood_contract = Wood_Contract()
coin_contract = Coin_Contract()


@app.route('/')
def hello_world():
    return jsonify({
        'status_code': 200,
        'status': 'success',
    })


@app.route('/wood/total_supply', methods=['GET', 'POST'])
def wood():
    return jsonify({'total wood supply': wood_contract.get_total_supply()})


@app.route('/wood/supply_left', methods=['GET', 'POST'])
def wood_supply_left():
    return jsonify({'wood supply left': wood_contract.wood_supply_left()})


@app.route('/wood/balance', methods=['POST'])
def wood_balance():
    _address = request.get_json()['address']
    return jsonify({
        'wood balance': wood_contract.get_balance(_address)
    })


if __name__ == '__main__':
    app.run(debug=True)
