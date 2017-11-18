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
HTH = w3.eth.contract(address='0x280e4c062addee30d06e3c81a47df8f1730a1df1', abi=abi)

def getBalance(address):
    hash_address = address._normalize_32byte_address(address)
    normalized_address = address.to_normalized_address(hash_address)

    return int(HTH.call().getBalance(normalized_address))

def setBalance(address, amount):
    hash_address = address._normalize_32byte_address(address)
    normalized_address = address.to_normalized_address(hash_address)

    HTH.transact(transaction={"from":w3.eth.accounts[0],"gas" : 3000}).set(normalized_address, amount)

def processTransaction(sender, receiver, amount):
    sender_hash_address = address._normalize_32byte_address(sender)
    sender_normalized_address = address.to_normalized_address(sender_hash_address)

    receiver_hash_address = address._normalize_32byte_address(sender)
    receiver_normalized_address = address.to_normalized_address(receiver_hash_address)

    return HTH.transact(transaction={"from":w3.eth.account[0],"gas" : 3000}).sendFromTo(sender_normalized_address, receiver_normalized_address, amount)
