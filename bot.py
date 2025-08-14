"""
Telegram bot handler for cryptocurrency price charts and data.
Handles all bot commands and user interactions.
"""

import os
import logging
import telebot
from telebot import types
from chart_generator import ChartGenerator
from crypto_api import CryptoAPI
from config import Config

logger = logging.getLogger(__name__)

class CryptoBotHandler:
    def __init__(self):
        """Initialize the bot with token from environment variables."""
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not self.bot_token:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")
        
        self.bot = telebot.TeleBot(self.bot_token)
        self.crypto_api = CryptoAPI()
        self.chart_generator = ChartGenerator()
        
        # Register handlers
        self._register_handlers()
    
    def send_safe_reply(self, message, text, **kwargs):
        """Send reply with error handling for deleted messages."""
        try:
            self.bot.reply_to(message, text, **kwargs)
        except Exception as e:
            # If reply fails, try sending as regular message
            try:
                self.bot.send_message(message.chat.id, text, **kwargs)
            except Exception as e2:
                logger.error(f"Failed to send message: {e2}")
    
    def _register_handlers(self):
        """Register all
