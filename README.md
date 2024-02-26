![Layerless(2)](https://github.com/rgalyeon/Layerless/assets/28117274/e92b050b-301a-4248-8006-91b683e41f82)

# Layerless
Software for working with the Layerless project. Supports multiple OKX accounts, multithreading, encrypts sensitive data, after encryption wallets can be started using only the wallet address (no need to re-enter data).

## 🗂️ Description
With the program, you can perform all the steps required to pass the testnet with just one run. Any number of accounts, proxies and multithreading are supported.

**Modules**
1. `encrypt_privates_and_proxy` - module is necessary for the first launch of the software. Reads data from the table `wallet_data.xlsx`, encrypts and deletes sensitive data from the table. For repeated runs it is enough to specify only the wallet address, because the rest of the data is stored in encrypted form. If you want to add new data (add wallets or change proxies), you will need to use this module again.
2. `withdraw_okx` - module for withdrawing tokens from the OKX. Supports checking the balance on the wallet to avoid withdrawing money in case it is already in the chain
3. `testnet_bridge` - make swap from ETH (Arbitrum, Optimism) to Goerli ETH (LayerZero)
4. `get_steth` - make swap from Goerli ETH to stETH.
5. `stake_steth` - deposit stETH to Layerless protocol
6. `unstake_steth` - unstake stETH from Layerless protocol
7. `custom_routes` - module for customizing your own route. Use cases: [withdraw_okx, testnet_bridge, get_steth, stake_steth, unstake_eth] for first entry project, or [testnet_bridge, get_steth, automatic_routes] to run the script for many days ahead.
8. `automatic_routes` - module for automatic route building. You can customize the number of required transactions, you can add skipping some transactions (if you want to skip some day). You can configure delays between transactions. You can control the probability of making cheap transactions and expensive ones.
   
## ⚙️ Installation
```bash
git clone https://github.com/rgalyeon/Layerless.git
cd Layerless
python -m venv venv
source venv/bin/activate (on MacOs) or .\venv\Scripts\activate (on Windows)
pip install -r requirements.txt
```

## 🚀 How to run software
### 1. First, you must fill in the appropriate columns in the `wallet_data.xslx` table:
- `name` - name of wallet (optional field)
- `address` - wallet address
- `private` - private key 
- `proxy` - proxy, if used for wallet in the format `login:pass@ip:port` (optional field)
- `okx_api` - api okx account in the format `api;secret;password` (you can customize okx api for each wallet) (optional field)

### 2. Encrypt data
- Run script with `python main.py` command and choose `Encrypt private keys and proxies`
- Set up a password to access the data

### 3. Customize the modules and get them up and running. 
- Set up general settings in `settings.py` (thread_count, retry_count, etc...)
- Set up modules settings in `module_settings.py`
- Add the wallet addresses you want to run to the `wallet_data.xlsx` file (only wallet addresses are needed after encryption)
- Run script with `python main.py` command and choose necessary module.

## 🔗 Contacts
- [Author](https://t.me/rgalyeon) | [Tradium Community](https://t.me/tradium)
- Buy me a coffee: `rgalyeon.eth`
