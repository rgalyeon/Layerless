from loguru import logger
from config import TESTNET_BRIDGE_CONTRACT, LZ_GETH_CONTRACT, TESTNET_BRIDGE_ABI, LZ_GETH_ABI, LZ_CHAIN_ID
from .transfer import Transfer
from utils.sleeping import sleep


class TestnetBridge(Transfer):
    def __init__(self, wallet_info):
        super().__init__(wallet_info=wallet_info)

    async def bridge_logic(self, source_chain, destination_chain, amount_wei, amount, balance, slippage=0.05):
        logger.info(f"[{self.account_id}][{self.address}] Start testnet bridge {amount} ETH: "
                    f"{source_chain.capitalize()} -> {destination_chain.capitalize()}")

        dst_balance = await self.check_native_balance(destination_chain)

        oft_contract = self.get_contract(LZ_GETH_CONTRACT, LZ_GETH_ABI)
        bridge_contract = self.get_contract(TESTNET_BRIDGE_CONTRACT, TESTNET_BRIDGE_ABI)

        fee = (await oft_contract.functions.estimateSendFee(LZ_CHAIN_ID[destination_chain], self.address,
                                                            amount_wei, False, '0x').call())[0]

        amount_out_min = amount_wei - (amount_wei * slippage // 100)
        zro_payments_address = '0x0000000000000000000000000000000000000000'

        tx_data = await self.get_tx_data(amount_wei + fee)
        transaction = await bridge_contract.functions.swapAndBridge(amount_wei,
                                                                    amount_out_min,
                                                                    LZ_CHAIN_ID[destination_chain],
                                                                    self.address,
                                                                    self.address,
                                                                    zro_payments_address,
                                                                    "0x",
                                                                    ).build_transaction(tx_data)

        signed_tx = await self.sign(transaction)
        txn_hash = await self.send_raw_transaction(signed_tx)
        await self.wait_until_tx_finished(txn_hash.hex())

        while (await self.check_native_balance(destination_chain)) == dst_balance:
            logger.info(f"[{self.account_id}][{self.address}] Waiting money on {destination_chain}...")
            await sleep(60, 120)

        logger.success(f"[{self.account_id}][{self.address}] Successfully bridged")
