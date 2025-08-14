"""
Chart generator for creating cryptocurrency price charts using matplotlib.
Generates professional-looking charts with price data and technical indicators.
"""

import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for server environments

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import os
import logging
import tempfile

logger = logging.getLogger(__name__)

class ChartGenerator:
    def __init__(self):
        """Initialize the chart generator with styling options."""
        # Set up the style
        plt.style.use('dark_background')
        
        # Color scheme
        self.colors = {
            'background': '#1e1e1e',
            'grid': '#333333',
            'text': '#ffffff',
            'price_line': '#00ff88',
            'volume_bars': '#444444',
            'positive': '#00ff88',
            'negative': '#ff4444'
        }
    
    def create_price_chart(self, price_data, symbol, timeframe):
        """Create a price chart from the given data."""
        try:
            if not price_data:
                logger.error("No price data provided for chart generation")
                return None
            
            # Parse timestamps and prices
            timestamps = []
            prices = []
            volumes = []
            
            for point in price_data:
                try:
                    timestamp = datetime.fromisoformat(point['timestamp'].replace('Z', '+00:00'))
                    timestamps.append(timestamp)
                    prices.append(float(point['price']))
                    volumes.append(float(point.get('volume', 0)))
                except Exception as e:
                    logger.warning(f"Error parsing data point: {e}")
                    continue
            
            if len(timestamps) < 2:
                logger.error("Not enough valid data points for chart")
                return None
            
            # Create the figure with subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), 
                                         gridspec_kw={'height_ratios': [3, 1]},
                                         facecolor=self.colors['background'])
            
            # Price chart (main)
            ax1.plot(timestamps, prices, color=self.colors['price_line'], 
                    linewidth=2, label=f'{symbol} Price')
            
            # Fill area under the curve
            ax1.fill_between(timestamps, prices, alpha=0.1, 
                           color=self.colors['price_line'])
            
            # Styling for price chart
            ax1.set_facecolor(self.colors['background'])
            ax1.grid(True, color=self.colors['grid'], alpha=0.3)
            ax1.set_ylabel('Price (USD)', color=self.colors['text'])
            ax1.tick_params(colors=self.colors['text'])
            
            # Format price on y-axis
            if max(prices) < 1:
                ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.6f}'))
            else:
                ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
            
            # Volume chart (bottom)
            ax2.bar(timestamps, volumes, color=self.colors['volume_bars'], 
                   alpha=0.6, width=0.8)
            
            # Styling for volume chart
            ax2.set_facecolor(self.colors['background'])
            ax2.grid(True, color=self.colors['grid'], alpha=0.3)
            ax2.set_ylabel('Volume', color=self.colors['text'])
            ax2.tick_params(colors=self.colors['text'])
            ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x:,.0f}'))
            
            # Format x-axis based on timeframe
            if timeframe in ['1d', '7d']:
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
                ax2.xaxis.set_major_locator(mdates.HourLocator(interval=4))
            else:
                ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                ax2.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(timestamps)//10)))
            
            # Rotate x-axis labels
            plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)
            
            # Add title and legend
            price_change = ((prices[-1] - prices[0]) / prices[0]) * 100
            change_color = self.colors['positive'] if price_change >= 0 else self.colors['negative']
            change_symbol = '+' if price_change >= 0 else ''
            
            title = f'{symbol} Price Chart ({timeframe.upper()}) - {change_symbol}{price_change:.2f}%'
            ax1.set_title(title, color=self.colors['text'], fontsize=14, fontweight='bold')
            
            # Add current price annotation
            ax1.annotate(f'${prices[-1]:.6f}', 
                        xy=(timestamps[-1], prices[-1]),
                        xytext=(10, 10), textcoords='offset points',
                        bbox=dict(boxstyle='round,pad=0.3', facecolor=change_color, alpha=0.7),
                        color='white', fontweight='bold')
            
            # Tight layout
            plt.tight_layout()
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
            plt.savefig(temp_file.name, facecolor=self.colors['background'], 
                       dpi=150, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Chart generated successfully: {temp_file.name}")
            return temp_file.name
            
        except Exception as e:
            logger.error(f"Error creating price chart: {e}")
            return None
