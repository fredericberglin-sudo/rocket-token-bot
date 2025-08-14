"""
Main entry point for the Telegram cryptocurrency bot.
This file initializes and starts the bot on Replit.
"""

import os
import logging
from keep_alive import keep_alive
from bot import CryptoBotHandler

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot and keep-alive server."""
    try:
        # Start the keep-alive server in a separate thread
        keep_alive()
        
        # Initialize and start the Telegram bot
        bot_handler = CryptoBotHandler()
        logger.info("Starting Telegram crypto bot...")
        bot_handler.start_bot()
        
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        raise

if __name__ == "__main__":
    main()
