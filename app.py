from web3 import Web3
import json
from pathlib import Path
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/4fea577001cb41a587bb36a7af0c6fdc"))
from web3.middleware import construct_sign_and_send_raw_middleware
from web3.middleware import geth_poa_middleware
from eth_account import Account

private_key = '0x88377bf767328b73cba996ee72fa81bc0f083fe243f03b56191e5dc46de46b1e'

acct = Account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.default_account = acct.address
abi_path = 'solidity/Greeter.abi'
abi = Path(abi_path).read_text()
contract_address = "0xbed63d024C33ce5DAC1d842c3F31BbcbE9C93cf3"
greeter = w3.eth.contract(
    address=contract_address,
    abi=abi)


greeter.functions.greet("0x8BA729A7F72D307966EC50273a81e316756C4437","Hi There").transact()