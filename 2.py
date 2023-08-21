from web3 import Web3
import json
import ssl
import time
import requests

ssl._create_default_https_context = ssl._create_unverified_context

w3 = Web3(
    Web3.HTTPProvider(
        "https://necessary-virulent-isle.base-mainnet.discover.quiknode.pro/7e53022d7b6cc80f2cfca23bb4291c32ab029d47/"
    )
)
abi_string = """[{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"trader","type":"address"},{"indexed":false,"internalType":"address","name":"subject","type":"address"},{"indexed":false,"internalType":"bool","name":"isBuy","type":"bool"},{"indexed":false,"internalType":"uint256","name":"shareAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"ethAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"protocolEthAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"subjectEthAmount","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"supply","type":"uint256"}],"name":"Trade","type":"event"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"buyShares","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getBuyPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getBuyPriceAfterFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"supply","type":"uint256"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getSellPrice","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"getSellPriceAfterFee","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolFeeDestination","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"protocolFeePercent","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sharesSubject","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"sellShares","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"_feeDestination","type":"address"}],"name":"setFeeDestination","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_feePercent","type":"uint256"}],"name":"setProtocolFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"_feePercent","type":"uint256"}],"name":"setSubjectFeePercent","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"},{"internalType":"address","name":"","type":"address"}],"name":"sharesBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"sharesSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"subjectFeePercent","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"}]"""
abi = json.loads(abi_string)
contract_address = Web3.to_checksum_address(
    "0xcf205808ed36593aa40a44f10c7f7c2f67d4a4d4"
)
contract = w3.eth.contract(address=contract_address, abi=abi)

api_endpoint = "https://prod-api.kosetto.com/users/"


def format_trades(event, social_data):
    is_buy = 'Buy' if event['args']['isBuy'] else 'Sell'
    action = is_buy
    format_output = """
    Trade Event:
    -----------
    Trader: {trader}
    Subject: {subject}
    Action: {action}
    Share Amount: {share_amount}
    ETH Amount: {eth_amount} eth
    Protocol ETH Amount: {protocol_eth_amount} eth
    Subject ETH Amount: {subject_eth_amount} eth
    Supply: {supply}
    
    Transaction Details:
    --------------------
    Transaction Hash: {tx_hash}
    Block Number: {block_number}
    Block Hash: {block_hash}
    Log Index: {log_index}
    Transaction Index: {tx_index}
    Contract Address: {address}
    
    Subject Twitter Details:
    -------------------------
    Twitter Username: {twitter_username}
    Twitter Name: {twitter_name}
    Twitter Profile Picture URL: {twitter_pfp_url}
    """.format(
        trader=event['args']['trader'],
        subject=event['args']['subject'],
        share_amount=event['args']['shareAmount'],
        eth_amount=event['args']['ethAmount']/10**18,
        protocol_eth_amount=event['args']['protocolEthAmount']/10**18,
        subject_eth_amount=event['args']['subjectEthAmount']/10**18,
        supply=event['args']['supply'],
        tx_hash=event['transactionHash'].hex(),
        action = action,
        block_number=event['blockNumber'],
        block_hash=event['blockHash'].hex(),
        log_index=event['logIndex'],
        tx_index=event['transactionIndex'],
        address=event['address'],
        twitter_username=social_data['twitterUsername'] if social_data else 'N/A',
        twitter_name=social_data['twitterName'] if social_data else 'N/A',
        twitter_pfp_url=social_data['twitterPfpUrl'] if social_data else 'N/A'
    )    
    return format_output



def get_social_data(address):
    response = requests.get(api_endpoint + address)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None


def trade_event(event):
    subject_address = event['args']['subject']
    social_data = get_social_data(subject_address)
    
    formatted_output = format_trades(event, social_data)
    print(formatted_output)


trade_event_filter = contract.events.Trade.create_filter(fromBlock="latest")

while True:
    for event in trade_event_filter.get_new_entries():
        trade_event(event)
        time.sleep(5)
