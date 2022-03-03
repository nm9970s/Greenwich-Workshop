
from web3 import Web3
import json
from pathlib import Path
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/4fea577001cb41a587bb36a7af0c6fdc"))
from web3.middleware import construct_sign_and_send_raw_middleware
from web3.middleware import geth_poa_middleware
from eth_account import Account
import asyncio

private_key = '0x88377bf767328b73cba996ee72fa81bc0f083fe243f03b56191e5dc46de46b1e'

acct = Account.from_key(private_key)
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.default_account = acct.address
abi_path = 'solidity/Greeter.abi'
abi = Path(abi_path).read_text()
contract_address = "0x8BA729A7F72D307966EC50273a81e316756C4437"
greeter = w3.eth.contract(
    address=contract_address,
    abi=abi)

# define function to handle events and print to the console
def handle_event(event):
    e = Web3.toJSON(event)
    print(e)
    d = json.loads(e)
    print(f"{d['args']['name']}: {d['args']['message']}")

    # and whatever


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "MessageReceived" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for MessageReceived in event_filter.get_new_entries():
            handle_event(MessageReceived)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = greeter.events.MessageReceived.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 1)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()


if __name__ == "__main__":
    main()
    
