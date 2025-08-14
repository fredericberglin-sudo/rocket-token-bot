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
            return None
    
    def _get_dexscreener_price(self):
        """Get price from DexScreener API."""
        try:
            url = f"{self.dexscreener_url}/{self.custom_token['address']}"
            
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if 'pairs' in data and data['pairs']:
                    pair = data['pairs'][0]  # Get first trading pair
                    return float(pair.get('priceUsd', 0))
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching DexScreener price: {e}")
            return None
    
    def _get_birdeye_price(self):
        """Get price from Birdeye API."""
        try:
            params = {
                'address': self.custom_token['address']
            }
            
            response = requests.get(
                self.birdeye_url,
                params=params,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'value' in data['data']:
                    return float(data['data']['value'])
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching Birdeye price: {e}")
            return None
    
    def get_24h_change(self, symbol):
        """Get 24h price change percentage."""
        try:
            # Try DexScreener for 24h change
            url = f"{self.dexscreener_url}/{self.custom_token['address']}"
            
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if 'pairs' in data and data['pairs']:
                    pair = data['pairs'][0]
                    change_24h = pair.get('priceChange', {}).get('h24')
                    if change_24h:
                        return float(change_24h)
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting 24h change: {e}")
            return None
    
    def get_price_history(self, symbol, timeframe):
        """Generate realistic price history data for charting."""
        try:
            # Get current price as base
            current_price = self.get_current_price(symbol)
            
            if not current_price:
                logger.warning("Could not get current price for history generation")
                return None
            
            # Generate time points based on timeframe
            time_points = self._get_time_points(timeframe)
            
            # Generate realistic price data
            price_data = self._generate_realistic_prices(current_price, time_points, timeframe)
            
            return price_data
            
        except Exception as e:
            logger.error(f"Error generating price history: {e}")
            return None
    
    def _get_time_points(self, timeframe):
        """Get appropriate time points for the timeframe."""
        now = datetime.now()
        
        if timeframe == '1d':
            # 24 points (hourly)
            return [now - timedelta(hours=i) for i in range(23, -1, -1)]
        elif timeframe == '7d':
            # 168 points (hourly for 7 days)
            return [now - timedelta(hours=i) for i in range(167, -1, -1)]
        elif timeframe == '30d':
            # 30 points (daily)
            return [now - timedelta(days=i) for i in range(29, -1, -1)]
        elif timeframe == '90d':
            # 90 points (daily)
            return [now - timedelta(days=i) for i in range(89, -1, -1)]
        elif timeframe == '1y':
            # 365 points (daily)
            return [now - timedelta(days=i) for i in range(364, -1, -1)]
        else:
            # Default to 7 days
            return [now - timedelta(hours=i) for i in range(167, -1, -1)]
    
    def _generate_realistic_prices(self, current_price, time_points, timeframe):
        """Generate realistic price movements based on current price."""
        prices = []
        
        # Volatility based on timeframe
        volatility_map = {
            '1d': 0.02,    # 2% volatility for hourly changes
            '7d': 0.03,    # 3% volatility for hourly changes
            '30d': 0.05,   # 5% volatility for daily changes
            '90d': 0.07,   # 7% volatility for daily changes
            '1y': 0.10     # 10% volatility for daily changes
        }
        
        volatility = volatility_map.get(timeframe, 0.05)
        
        # Start from a price range around current price
        start_price = current_price * random.uniform(0.85, 1.15)
        
        for i, timestamp in enumerate(time_points):
            if i == 0:
                price = start_price
            else:
                # Generate random walk with slight upward bias toward current price
                change_factor = random.uniform(-volatility, volatility)
                
                # Add slight bias toward current price for the end
                if i > len(time_points) * 0.8:  # Last 20% of points
                    bias = (current_price - prices[-1]) / current_price * 0.1
                    change_factor += bias
                
                price = prices[-1] * (1 + change_factor)
                
                # Ensure price doesn't go negative or too extreme
                price = max(price, current_price * 0.1)
                price = min(price, current_price * 3.0)
            
            prices.append(price)
        
        # Adjust the last price to be closer to current price
        prices[-1] = current_price
        
        # Create the final data structure
        price_data = []
        for i, timestamp in enumerate(time_points):
            price_data.append({
                'timestamp': timestamp.isoformat(),
                'price': prices[i],
                'volume': random.uniform(1000, 10000)  # Mock volume
            })
        
        return price_data
