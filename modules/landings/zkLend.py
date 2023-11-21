import random

from modules import Landing
from settings import USE_PROXY
from utils.tools import gas_checker, repeater
from config import ZKLEND_CONTRACTS, TOKENS_PER_CHAIN


class ZkLend(Landing):
    def __init__(self, client):
        self.client = client

    @repeater
    @gas_checker
    async def deposit(self):
        try:
            await self.client.initialize_account()

            token_name, token_address, amount, amount_in_wei = await self.client.get_landing_data('zkLend', True)

            self.client.logger.info(f'{self.client.info} Deposit to zkLend: {amount} {token_name}')

            landing_contract = await self.client.get_contract(ZKLEND_CONTRACTS['landing'])

            approve_call = self.client.get_approve_call(token_address, ZKLEND_CONTRACTS['landing'],
                                                        amount_in_wei)

            deposit_call = landing_contract.functions["deposit"].prepare(
                token_address,
                amount_in_wei
            )

            return await self.client.send_transaction(approve_call, deposit_call)
        finally:
            if USE_PROXY:
                await self.client.session.close()

    @repeater
    @gas_checker
    async def withdraw(self):
        try:
            await self.client.initialize_account()

            token_name, token_contract = await self.client.get_landing_data(class_name='zkLend')

            self.client.logger.info(f'{self.client.info} Withdraw {token_name} from zkLend')

            landing_contract = await self.client.get_contract(ZKLEND_CONTRACTS['landing'])

            withdraw_call = landing_contract.functions["withdraw_all"].prepare(
                token_contract
            )

            return await self.client.send_transaction(withdraw_call)
        finally:
            if USE_PROXY:
                await self.client.session.close()

    @repeater
    @gas_checker
    async def enable_collateral(self):
        try:
            await self.client.initialize_account()

            token_name, token_address = random.choice(list(TOKENS_PER_CHAIN[self.client.network.name].items()))

            self.client.logger.info(f'{self.client.info} Enable {token_name} collateral on zkLend')

            landing_contract = await self.client.get_contract(ZKLEND_CONTRACTS['landing'])

            enable_collateral_call = landing_contract.functions["enable_collateral"].prepare(
                token_address
            )

            return await self.client.send_transaction(enable_collateral_call)
        finally:
            if USE_PROXY:
                await self.client.session.close()

    @repeater
    @gas_checker
    async def disable_collateral(self):
        try:
            await self.client.initialize_account()

            token_name, token_address = random.choice(list(TOKENS_PER_CHAIN[self.client.network.name].items()))

            self.client.logger.info(f'{self.client.info} Disable {token_name} collateral on zkLend')

            landing_contract = await self.client.get_contract(ZKLEND_CONTRACTS['landing'])

            disable_collateral_call = landing_contract.functions["disable_collateral"].prepare(
                token_address
            )

            return await self.client.send_transaction(disable_collateral_call)
        finally:
            if USE_PROXY:
                await self.client.session.close()
