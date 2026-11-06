from dataclasses import dataclass
from typing import List, Optional
import requests
from config import BotConfig

@dataclass
class MarketOpportunity:
    condition_id: str
    question: str
    yes_best_ask: float
    no_best_ask: float
    bundle_cost: float
    spread_edge_percent: float
    liquidity_usdc: float
    is_arbitrage_profitable: bool

class PolymarketScanner:
    def __init__(self, config: BotConfig):
        self.config = config
        self.base_url = "https://gamma-api.polymarket.com"

    def fetch_active_markets(self, limit: int = 15) -> List[dict]:
        try:
            url = f"{self.base_url}/markets"
            params = {
                "active": "true",
                "closed": "false",
                "limit": limit,
                "order": "volume24hr",
                "ascending": "false"
            }
            resp = requests.get(url, params=params, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            return []
        except Exception:
            return []

    def evaluate_arbitrage(self, market: dict) -> Optional[MarketOpportunity]:
        try:
            tokens = market.get("tokens", [])
            if len(tokens) < 2:
                return None

            yes_price = float(tokens[0].get("price", 0.50))
            no_price = float(tokens[1].get("price", 0.50))
            bundle_cost = yes_price + no_price

            # If YES + NO < $1.00 - spread
            # Guaranteed payout at resolution = $1.00
            edge_percent = ((1.00 - bundle_cost) / 1.00) * 100

            is_profitable = edge_percent >= self.config.min_spread_percent

            return MarketOpportunity(
                condition_id=market.get("conditionId", "unknown"),
                question=market.get("question", "N/A"),
                yes_best_ask=yes_price,
                no_best_ask=no_price,
                bundle_cost=bundle_cost,
                spread_edge_percent=round(edge_percent, 2),
                liquidity_usdc=float(market.get("volume24hr", 0.0)),
                is_arbitrage_profitable=is_profitable
            )
        except Exception:
            return None
