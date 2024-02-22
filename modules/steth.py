from loguru import logger
from .account import Account
from config import STETH_CONTRACT, ERC20_ABI
from utils.sleeping import sleep
from utils.helpers import retry
from web3.exceptions import ContractLogicError


class StETH(Account):
    def __init__(self, wallet_info):
        super(StETH, self).__init__(wallet_info=wallet_info, chain="goerli")

    @retry
    async def get_steth(self,
                        min_amount: float,
                        max_amount: float,
                        decimal: int,
                        all_amount: bool,
                        min_percent: int,
                        max_percent: int):

        amount_wei, amount, balance = await self.get_amount(
            'ETH',
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        logger.info(f"[{self.account_id}][{self.address}] Start swap ETH -> stETH")

        contract = self.get_contract(STETH_CONTRACT, ERC20_ABI)
        prev_balance = await contract.functions.balanceOf(self.address).call()
        tx_data = await self.get_tx_data(amount_wei)
        tx_data.update({"to": self.w3.to_checksum_address(STETH_CONTRACT)})

        n_attempts = 10
        while n_attempts:
            try:
                signed_txn = await self.sign(tx_data)
                txn_hash = await self.send_raw_transaction(signed_txn)
                await self.wait_until_tx_finished(txn_hash.hex())
                break
            except ContractLogicError:
                logger.error(f"[{self.account_id}][{self.address}] STAKE LIMIT. Try to reduce the amount or wait...")
                await sleep(30, 60)
            n_attempts -= 1

        logger.info(f"[{self.account_id}][{self.address}] Wait stETH...")
        while (await contract.functions.balanceOf(self.address).call()) == prev_balance:
            await sleep(20, 20)

        logger.success(f"[{self.account_id}][{self.address}] Successfully swapped")
