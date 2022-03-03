
from web3 import Web3
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
bin_path = 'solidity/Greeter.bin'

print(f"Connection Status: {w3.isConnected()}")

abi = Path(abi_path).read_text()
bin = Path(bin_path).read_text()

Greeter = w3.eth.contract(abi=abi, bytecode=bin)
tx_hash = Greeter.constructor("Hello").transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
contract_address = tx_receipt.contractAddress

print(contract_address)