// Token contract code in Solidity
pragma solidity ^0.8.0;

contract RainToken {

    address public ownerAddress = 0x6AAEd57e79C25F5552DAe735f32e06D7bb7925c6;
    string public name = "Raindrops";
    string public symbol = "RDP";
    uint256 public totalSupply;

    mapping(address => uint256) public balanceOf;

    constructor(uint256 _initialSupply) {
        balanceOf[msg.sender] = _initialSupply;
        totalSupply = _initialSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balanceOf[msg.sender] >= _value);
        balanceOf[msg.sender] -= _value;
        balanceOf[_to] += _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
 
    event Transfer(address indexed _from, address indexed _to, uint256 _value);


    function spend(address _from, uint256 _value) public returns (bool success) {
        require(balanceOf[_from] >= _value);
        balanceOf[msg.sender] += _value;
        balanceOf[_from] -= _value;
    }
}

