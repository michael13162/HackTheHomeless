pragma solidity ^0.4.4;

import "./ConvertLib.sol";

contract HTH {
	mapping (address => uint) public balances;
	
	function getNum() returns(uint){
		return 1123;
	}

	function set(address sender, uint amount) returns(bool accepted) {
		balances[sender] = amount;
		return true;
	}

	function HTH() {
		
	}

	function sendFromTo(address sender, address receiver, uint amount) returns(bool sufficient) {
		balances[sender] -= amount;
		balances[receiver] += amount;
		return true;
	}

	function getBalance(address addr) returns(uint) {
		return balances[addr];
	}
}
