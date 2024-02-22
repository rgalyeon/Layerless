import json

WALLET_DATA_PATH = 'wallet_data.xlsx'
SHEET_NAME = 'evm'
ENCRYPTED_DATA_PATH = 'encrypted_data.txt'
REALTIME_SETTINGS_PATH = 'realtime_settings.json'

with open('data/rpc.json') as file:
    RPC = json.load(file)

with open('data/abi/erc20_abi.json') as file:
    ERC20_ABI = json.load(file)

with open('data/abi/testnet_bridge/abi.json', "r") as file:
    TESTNET_BRIDGE_ABI = json.load(file)

with open('data/abi/geth/abi.json', "r") as file:
    LZ_GETH_ABI = json.load(file)

with open('data/abi/layerless/steth_abi.json', "r") as file:
    LAYERLESS_STETH_ABI = json.load(file)

TESTNET_BRIDGE_CONTRACT = "0x0A9f824C05A74F577A536A8A0c673183a872Dff4"
LZ_GETH_CONTRACT = "0xdD69DB25F6D620A7baD3023c5d32761D353D3De9"
STETH_CONTRACT = "0x1643E812aE58766192Cf7D2Cf9567dF2C37e9B7F"
LAYERLESS_STETH_CONTRACT = "0xFb6176F982F8fD5908574C5d21e8fe7D4653a236"
LAYERLESS_RETH_CONTRACT = "0xEaB574456eDbdd37712e49827f383Eb0cc05Ba14"

GOERLI_TOKENS = {
    "STETH": "0x1643E812aE58766192Cf7D2Cf9567dF2C37e9B7F",
    "RETH": "0x178E141a0E3b34152f73Ff610437A7bf9B83267A"
}


BUNGEE_CONTRACT = "0x7ee459d7fde8b4a3c22b9c8c7aa52abaddd9ffd5"

CHAINS_OKX = {
    'linea': 'Linea',
    'base': 'Base',
    'arbitrum': 'Arbitrum One',
    'optimism': 'Optimism',
    'zksync': 'zkSync Era'
}

LZ_CHAIN_ID = {
    "goerli": 154
}
