import random
from utils.sleeping import sleep
from utils.helpers import retry
from loguru import logger
from .account import Account
from config import LAYERLESS_STETH_CONTRACT, LAYERLESS_STETH_ABI, STETH_CONTRACT


class Layerless(Account):
    def __init__(self, wallet_info):
        super(Layerless, self).__init__(wallet_info, chain="goerli")
        self.contract = self.get_contract(LAYERLESS_STETH_CONTRACT, LAYERLESS_STETH_ABI)

    @retry
    async def stake(self, min_amount, max_amount, decimal,
                    all_amount, min_percent, max_percent,
                    withdraw=False, sleep_from=100, sleep_to=200):

        amount_wei, amount, balance = await self.get_amount('STETH',
                                                            min_amount,
                                                            max_amount,
                                                            decimal,
                                                            all_amount,
                                                            min_percent,
                                                            max_percent
                                                            )

        logger.info(f"[{self.account_id}][{self.address}] Start stake stETH")

        await self.approve(amount_wei, STETH_CONTRACT, LAYERLESS_STETH_CONTRACT)

        tx_data = await self.get_tx_data()
        transaction = await self.contract.functions.restake(self.address, amount_wei).build_transaction(tx_data)
        signed_tx = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(txn_hash.hex())

        if withdraw:
            await sleep(sleep_from, sleep_to)
            await self.unstake(100, 100)

    @retry
    async def unstake(self, min_percent, max_percent):
        logger.info(f"[{self.account_id}][{self.address}] Start unstake stETH")

        percent = random.randint(min_percent, max_percent)
        balance_wei = await self.contract.functions.balanceOf(self.address).call()

        amount_wei = balance_wei * percent // 100

        tx_data = await self.get_tx_data()
        transaction = await self.contract.functions.unstake((amount_wei,)).build_transaction(tx_data)
        signed_tx = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(txn_hash.hex())
