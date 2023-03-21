// Token contract code in Solidity
pragma solidity ^0.8.0;

contract WoodToken {
    address public ownerAddress = 0x6AAEd57e79C25F5552DAe735f32e06D7bb7925c6;
    string public name = "Gopher Wood";
    string public symbol = "GPW";
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    constructor(uint256 _initialSupply) {
        balanceOf[msg.sender] = _initialSupply;
        totalSupply = _initialSupply;
    }

    struct Player_struct {
        uint256 mana;
        uint256 current_Log;
        uint256 total_Log;
    }
    mapping(address => Player_struct) public player;

    Player_struct public defaultPlayer = Player_struct(5, 0, 0);

    function initial_player(address _address) public returns (bool) {
        if (player[_address].mana != 0) {
            return false;
        }
        player[_address] = defaultPlayer;
        return true;
    }

    function update_player_data(
        address _address,
        uint256 mana,
        uint256 log
    ) public returns (bool success) {
        uint256 current_mana = player[_address].mana;
        uint256 current_Log = balanceOf[_address];
        uint256 current_total_Log = player[_address].total_Log;

        current_mana -= mana;
        current_total_Log += log;

        player[_address] = Player_struct(
            current_mana,
            current_Log,
            current_total_Log
        );
        return true;
    }

    function Cutting_Wood(address _to) public returns (bool success) {
        require(player[_to].mana >= 1, "too tired");
        require(balanceOf[msg.sender] >= 1);
        balanceOf[msg.sender] -= 1;
        balanceOf[_to] += 1;
        emit cutting_wood(msg.sender, _to, 1);

        update_player_data(_to, 1, 1);

        return true;
    }

    event cutting_wood(
        address indexed _from,
        address indexed _to,
        uint256 _value
    );

    function spending_wood(address _from, uint256 _value)
        public
        returns (int256 newBalance)
    {
        uint256 current_mana = player[_from].mana;
        uint256 current_total_Log = player[_from].total_Log;

        require(
            balanceOf[_from] >= _value && _value != 0,
            "Not enough wood to spend"
        );

        balanceOf[_from] -= _value;
        balanceOf[ownerAddress] += _value;

        player[_from] = Player_struct(
            current_mana,
            balanceOf[_from],
            current_total_Log
        );

        return (int256(balanceOf[_from]));
    }

    function restore_mana(address _to, uint256 _value) public {
    
        uint256 current_mana = player[_to].mana;
        uint256 current_Log = balanceOf[_to];
        uint256 current_total_Log = player[_to].total_Log;

        current_mana += _value*2;

        player[_to] = Player_struct(
            current_mana,
            current_Log,
            current_total_Log
        );
    }
}
