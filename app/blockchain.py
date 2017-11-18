import json
import web3
from flask import Flask

import eth_utils
from eth_utils import address
from web3 import Web3, HTTPProvider, TestRPCProvider
from web3.contract import ConciseContract

app = Flask(__name__)
w3 = Web3(HTTPProvider('http://localhost:8545'))

abi_string = '''
[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"balances","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"sender","type":"address"},{"name":"amount","type":"uint256"}],"name":"set","outputs":[{"name":"accepted","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"getNum","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"sender","type":"address"},{"name":"receiver","type":"address"},{"name":"amount","type":"uint256"}],"name":"sendFromTo","outputs":[{"name":"sufficient","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"addr","type":"address"}],"name":"getBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]
'''

abi = json.loads(abi_string)
HTH = w3.eth.contract(address='0xc70e4aebc6eba0096888e9c57ef42bd4211ab6f5', abi=abi)

def getBalance(addr):
    hash_address = address._normalize_32byte_address(addr)
    normalized_address = address.to_normalized_address(hash_address)

    return int(HTH.call().getBalance(normalized_address))

def setBalance(addr, amount):
    hash_address = address._normalize_32byte_address(addr)
    normalized_address = address.to_normalized_address(hash_address)

    HTH.transact(transaction={"from":w3.eth.accounts[0],"gas" : 3000000}).set(normalized_address, amount)

def processTransaction(sender, receiver, amount):
    sender_hash_address = address._normalize_32byte_address(sender)
    sender_normalized_address = address.to_normalized_address(sender_hash_address)

    receiver_hash_address = address._normalize_32byte_address(receiver)
    receiver_normalized_address = address.to_normalized_address(receiver_hash_address)

    HTH.transact(transaction={"from":w3.eth.accounts[0],"gas" : 3000000}).sendFromTo(sender_normalized_address, receiver_normalized_address, amount)

if __name__ == '__main__':
    name = 'example'
    addr = w3.sha3(text=name)
    
    setBalance(addr, 1000)
    print(name + ' ' + str(getBalance(addr)))

    receiver_name = 'receiver'
    receiver_addr = w3.sha3(text=receiver_name)

    setBalance(receiver_addr, 1900)
    print(receiver_name + ' ' + str(getBalance(receiver_addr)))

    processTransaction(addr, receiver_addr, 800)
    print(name + ': ' + str(getBalance(addr)))
    print(receiver_name + ': ' + str(getBalance(receiver_addr)))
