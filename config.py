import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class BotConfig:
    polygon_private_key: str = os.getenv("POLYGON_PRIVATE_KEY", "")
    polygon_rpc_url: str = os.getenv("POLYGON_RPC_URL", "https://polygon-rpc.com")
    clob_host: str = os.getenv("POLYMARKET_HOST", "https://clob.polymarket.com")
    api_key: str = os.getenv("POLY_API_KEY", "")
    api_secret: str = os.getenv("POLY_API_SECRET", "")
    api_passphrase: str = os.getenv("POLY_API_PASSPHRASE", "")
    min_spread_percent: float = float(os.getenv("MIN_ARBITRAGE_SPREAD_PERCENT", "1.5"))
    trade_size_usdc: float = float(os.getenv("TRADE_SIZE_USDC", "50.0"))
    max_positions: int = int(os.getenv("MAX_OPEN_POSITIONS", "5"))
    simulation_mode: bool = os.getenv("SIMULATION_MODE", "true").lower() != "false"
    enable_5min_btc: bool = os.getenv("ENABLE_5MIN_BTC_MARKETS", "true").lower() == "true"
    slippage_percent: float = float(os.getenv("SLIPPAGE_TOLERANCE_PERCENT", "1.0"))

def get_config() -> BotConfig:
    return BotConfig()
