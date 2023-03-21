from backend.contract.Contract_Wood import Wood_Contract
from backend.contract.Contract_Coin import Coin_Contract

from backend.app.app import app

wood_contract = Wood_Contract()
coin_contract = Coin_Contract()


@app.route('/')
def hello_world():
    wood_hello = wood_contract.hello()
    coin_hello = coin_contract.hello()

    return f'{wood_hello} | {coin_hello}'


if __name__ == '__main__':
    app.run(debug=True)
