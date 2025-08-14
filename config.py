"""
Configuration settings for the Telegram cryptocurrency bot.
Contains bot settings, supported symbols, and error messages.
"""

import os

class Config:
    """Configuration class for the Telegram bot."""
    
    # Bot settings
    BOT_NAME = "ROCKET Token Chart Bot"
    BOT_VERSION = "1.0.0"
    
    # Supported timeframes for charts
    SUPPORTED_TIMEFRAMES = ['1d', '7d', '30d', '90d', '1y']
    
    # Default timeframe
    DEFAULT_TIMEFRAME = '7d'
    
    # API settings
    API_TIMEOUT = 10  # seconds
    
    # Chart settings
    CHART_WIDTH = 12
    CHART_HEIGHT = 8
    CHART_DPI = 150
    
    # Error messages
    ERROR_MESSAGES = {
        'invalid_timeframe': "❌ Invalid timeframe. Use: 1d, 7d, 30d, 90d, 1y",
        'price_fetch_failed': "❌ Could not fetch price data. Please try again later.",
        'chart_generation_failed': "❌ Failed to generate chart. Please try again later.",
        'api_error': "❌ API error occurred. Please try again in a moment.",
        'unknown_command': "❌ Unknown command. Use /help to see available commands.",
        'general_error': "❌ An error occurred. Please try again later."
    }
    
    # Success messages
    SUCCESS_MESSAGES = {
        'chart_generating': "📊 Generating {} chart for {}...",
        'price_fetched': "💰 Current price fetched successfully",
        'bot_started': "🚀 Bot started successfully!"
    }
    
    # Command descriptions
    COMMAND_DESCRIPTIONS = {
        'start': 'Start the bot and show welcome message',
        'help': 'Show available commands and usage',
        'chart': 'Generate price chart for your token',
        'price': 'Get current price and market stats',
        'info': 'Get detailed token information'
    }
    
    @staticmethod
    def get_help_text(token_name="Your Token", token_symbol="TOKEN", token_address=""):
        """Generate help text with token information."""
        return f"""
🚀 *{token_name} Chart Bot*

*Your Token:*
• Name: {token_name}
• Symbol: {token_symbol}
• Network: Solana

*Available Commands:*
• `/chart` - Get 7-day price chart
• `/chart <timeframe>` - Get chart for specific timeframe
• `/price` - Get current price and stats
• `/info` - Get detailed token information
• `/help` - Show this help message

*Examples:*
• `/chart` - 7-day chart
• `/chart 30d` - 30-day chart
• `/price` - Current price

*Supported Timeframes:*
• {', '.join(Config.SUPPORTED_TIMEFRAMES)}

*Token Address:*
`{token_address}`
        """
