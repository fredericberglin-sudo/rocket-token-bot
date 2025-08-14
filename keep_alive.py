"""
Keep-alive server to prevent the bot from sleeping on Replit.
Runs a simple Flask server that responds to health checks.
"""

from flask import Flask
import threading
import logging

logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home():
    """Health check endpoint."""
    return "ROCKET Token Bot is running!"

@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "rocket-token-bot",
        "version": "1.0.0"
    }

def run():
    """Run the Flask server."""
    try:
        app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"Error running keep-alive server: {e}")

def keep_alive():
    """Start the keep-alive server in a separate thread."""
    try:
        logger.info("Keep-alive server started on port 5000")
        server_thread = threading.Thread(target=run)
        server_thread.daemon = True
        server_thread.start()
    except Exception as e:
        logger.error(f"Error starting keep-alive server: {e}")
