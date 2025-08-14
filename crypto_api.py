"""
Cryptocurrency API handler for fetching price data and market information.
Specialized for Solana token data using Jupiter, DexScreener, and Birdeye APIs.
"""

import requests
import logging
from datetime import datetime, timedelta
import time
import random

logger = logging.getLogger(__name__)

class CryptoAPI:
    def __init__(self):
        """Initialize the API handler with Solana token configuration."""
        self.custom_token = {
            'symbol': 'ROCKET',
            'name': 'CRYPTOROCKET', 
            'address': '79V4Gu6UetViCNwHd8hRHpUxwkanxk2L5VVowB5AJRXz',
            'network': 'solana'
        }
        
        # API endpoints
        self.jupiter_price_url = "https://price.jup.ag/v6/price"
        self.dexscreener_url = "https://api.dexscreener.com/latest/dex/tokens"
        self.birdeye_url = "https://public-api.birdeye.so/defi/price"
        
        # Request timeout
        self.timeout = 10
    
    def get_token_info(self):
        """Get basic token information."""
        return self.custom_token.copy()
    
    def get_current_price(self, symbol):
        """Get current price from Jupiter API with fallbacks."""
        try:
            # Try Jupiter API first
            price = self._get_jupiter_price()
            if price:
                return price
            
            # Try DexScreener API
            price = self._get_dexscreener_price()
            if price:
                return price
            
            # Try Birdeye API
            price = self._get_birdeye_price()
            if price:
                return price
            
            logger.warning("All price APIs failed")
            return None
            
        except Exception as e:
            logger.error(f"Error getting current price: {e}")
            return None
    
    def _get_jupiter_price(self):
        """Get price from Jupiter API."""
        try:
            params = {
                'ids': self.custom_token['address']
            }
            
            response = requests.get(
                self.jupiter_price_url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and self.custom_token['address'] in data['data']:
                    price_info = data['data'][self.custom_token['address']]
                    return float(price_info.get('price', 0))
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching Jupiter current price: {e}")
