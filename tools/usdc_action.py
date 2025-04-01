"""USDC action provider for Base Sepolia testnet."""

from typing import Any
from web3 import Web3, HTTPProvider
from eth_abi import encode
from pathlib import Path
import json
from coinbase_agentkit import create_action, WalletProvider
from coinbase_agentkit.action_providers.action_provider import ActionProvider
from coinbase_agentkit.network import Network
from coinbase_agentkit.wallet_providers import EvmWalletProvider
from pydantic import BaseModel, Field
from configs.rpc import RPC_URL

w3 = Web3(provider=HTTPProvider(endpoint_uri=RPC_URL))

SUPPORTED_NETWORKS = ["base-sepolia"]
USDC_ADDRESS = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"  # Base Sepolia USDC

# Load ERC20 ABI from file
with open(Path(__file__).parent.parent / "abi" / "erc20.json") as f:
    ERC20_ABI = json.load(f)

class USDCBalanceInput(BaseModel):
    """Input schema for USDC balance check action."""
    user_address: str = Field(
        ..., 
        description="The address of the user to get USDC balance for",
        pattern="^0x[a-fA-F0-9]{40}$"
    )

class USDCTransferInput(BaseModel):
    """Input schema for USDC transfer action."""
    to_address: str = Field(
        ..., 
        description="The address to transfer USDC to",
        pattern="^0x[a-fA-F0-9]{40}$"
    )
    amount: int = Field(
        ..., 
        description="The amount of USDC to transfer (in wei, 1 USDC = 1,000,000 wei)",
        gt=0
    )

def encode_transfer(to_address: str, amount: int) -> bytes:
    """Encode transfer function call manually."""
    function_selector = Web3.to_bytes(hexstr="0xa9059cbb")
    encoded_params = encode(
        ['address', 'uint256'],
        [Web3.to_checksum_address(to_address), amount]
    )
    return function_selector + encoded_params

class USDCActionProvider(ActionProvider[EvmWalletProvider]):
    """Provides actions for interacting with USDC on Base Sepolia."""

    def __init__(self):
        super().__init__("usdc-provider", [])

    @create_action(
        name="get_usdc_balance",
        description="""
            This tool gets the USDC balance of a user on Base Sepolia.
            It takes:
            - user_address: The address of the user to get USDC balance for (must be a valid Ethereum address)

            Example:
            ```
            user_address: 0x1234567890123456789012345678901234567890
            ```
        """,
        schema=USDCBalanceInput,
    )
    def get_balance(self, args: dict[str, Any]) -> str:
        """Get the USDC balance of a user."""
        try:
            # Create contract instance
            contract = w3.eth.contract(address=USDC_ADDRESS, abi=ERC20_ABI)
            
            # Get balance
            balance = contract.functions.balanceOf(args["user_address"]).call()
            
            # USDC has 6 decimals
            balance_formatted = balance / (10 ** 6)

            return f"User {args['user_address']} has {balance_formatted:,.2f} USDC"

        except Exception as e:
            return f"Error checking USDC balance: {str(e)}"

    @create_action(
        name="transfer_usdc",
        description="""
            This tool transfers USDC to another address on Base Sepolia.
            It takes:
            - to_address: The address to transfer USDC to (must be a valid Ethereum address)
            - amount: The amount of USDC to transfer (in wei, 1 USDC = 1,000,000 wei)

            Example:
            ```
            to_address: 0x1234567890123456789012345678901234567890
            amount: 1000000  # 1 USDC
            ```
            """,
        schema=USDCTransferInput,
    )
    def transfer(self, wallet_provider: EvmWalletProvider, args: dict[str, Any]) -> str:
        """Transfer USDC to another address."""
        try:
            # Encode transfer call manually for better control
            calldata = encode_transfer(args["to_address"], args["amount"])
            
            # Send transaction
            params = {
                "to": USDC_ADDRESS,
                "data": '0x' + calldata.hex(),
            }

            tx_hash = wallet_provider.send_transaction(params)
            wallet_provider.wait_for_transaction_receipt(tx_hash)

            return f"Successfully transferred {args['amount'] / 1e6:,.2f} USDC to {args['to_address']}. Transaction hash: {tx_hash}"

        except Exception as e:
            return f"Error transferring USDC: {str(e)}"

    def supports_network(self, network: Network) -> bool:
        """Check if the network is supported by this action provider."""
        return network.chain_id == "84532"


def usdc_action_provider() -> USDCActionProvider:
    """Create a new USDC action provider."""
    return USDCActionProvider()
