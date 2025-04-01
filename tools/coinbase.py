import os
from dotenv import load_dotenv
from coinbase_agentkit import AgentKit
from coinbase_agentkit_langchain import get_langchain_tools
from eth_account import Account
from coinbase_agentkit import (
    AgentKit, 
    AgentKitConfig, 
    EthAccountWalletProvider, 
    EthAccountWalletProviderConfig
)

from coinbase_agentkit import (
    pyth_action_provider,
    wallet_action_provider
)
from tools.usdc_action import usdc_action_provider
from configs.rpc import RPC_URL
# Load environment variables
load_dotenv()

# Get private key from .env
private_key = os.getenv("PRIVATE_KEY")

assert private_key is not None, "You must set PRIVATE_KEY environment variable"
assert private_key.startswith("0x"), "Private key must start with 0x hex prefix"

account = Account.from_key(private_key)

def get_coinbase_tools():
    """Initialize and return Coinbase AgentKit tools."""
    wallet_provider = EthAccountWalletProvider(
        config=EthAccountWalletProviderConfig(
            account=account,
            chain_id="84532",
            rpc_url=RPC_URL
        )
    )

    agent_kit = AgentKit(AgentKitConfig(
        wallet_provider=wallet_provider,
        action_providers=[
            wallet_action_provider(),
            pyth_action_provider(),
            usdc_action_provider()
        ]
    ))
    return get_langchain_tools(agent_kit) 