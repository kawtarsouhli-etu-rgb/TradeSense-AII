"""
Moroccan Stock Price Scraper
Fetches IAM (Maroc Telecom) stock price from public finance websites
"""

import requests
from bs4 import BeautifulSoup
import re
from typing import Dict, Optional, Tuple
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MoroccanStockScraper:
    """Robust scraper for Moroccan stock prices"""
    
    def __init__(self):
        # Multiple source URLs as fallbacks
        self.urls = {
            'bourse_maroc': 'https://www.boursema.com/actualites-marocaines/',
            'maroc_telecom': 'https://www.iam.ma',
            'finance_marches': 'https://www.maroctelecommerce.ma',
            'general_finance': 'https://www.leconomiste.com/finances'
        }
        
        # Robust selectors for IAM stock with fallbacks
        self.selectors = [
            # Primary selectors - most likely to work
            {
                'tag': 'div',
                'attrs': {'class': re.compile(r'.*stock.*|.*price.*|.*cotation.*|.*valeur.*', re.IGNORECASE)},
                'text_pattern': r'IAM|IAM\s+\w+|Maroc\s+Telecom|Maroc\s+T[eé]l[eé]com'
            },
            # Secondary selectors
            {
                'tag': 'span',
                'attrs': {'class': re.compile(r'.*price.*|.*valeur.*|.*cours.*', re.IGNORECASE)}
            },
            # General price selectors
            {
                'tag': 'td',
                'attrs': {'class': re.compile(r'.*price.*|.*value.*|.*cotation.*', re.IGNORECASE)}
            },
            # Last resort - general search
            {
                'tag': 'div',
                'text_pattern': r'IAM.*[\d,.]+|Maroc\s+Telecom.*[\d,.]+'
            }
        ]
        
        # Price extraction patterns
        self.price_patterns = [
            r'(\d+[,.\d]*)\s*DH',
            r'(\d+[,.\d]*)\s*DHS?',
            r'(\d+[,.\d]*)\s*MAD',
            r'(\d+[,.\d]*)\s*([Mm]AD)?',
            r'valeur\s*[:=]\s*(\d+[,.\d]*)',
            r'cours\s*[:=]\s*(\d+[,.\d]*)'
        ]
        
        # Headers to mimic browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def clean_price(self, price_str: str) -> Optional[float]:
        """
        Clean and convert price string to float
        
        Args:
            price_str: Raw price string from website
            
        Returns:
            float: Clean price or None if invalid
        """
        if not price_str:
            return None
        
        try:
            # Remove extra whitespace and normalize
            cleaned = price_str.strip().replace(' ', '')
            
            # Remove common prefixes/suffixes
            cleaned = re.sub(r'^.*?(\d)', r'\1', cleaned)
            cleaned = re.sub(r'(\d).*$', r'\1', cleaned)
            
            # Handle different decimal separators
            cleaned = cleaned.replace(',', '.')
            
            # Extract numeric value
            numbers = re.findall(r'[\d.]+', cleaned)
            if numbers:
                price = float(numbers[0])
                # Validate reasonable price range (0.1 to 500 MAD)
                if 0.1 <= price <= 500:
                    return round(price, 2)
        except (ValueError, TypeError):
            logger.warning(f"Could not parse price: {price_str}")
        
        return None
    
    def scrape_iam_price(self) -> Dict:
        """
        Scrape IAM stock price from Moroccan finance websites
        
        Returns:
            Dict: Price data with metadata
        """
        start_time = datetime.now()
        
        for url_name, url in self.urls.items():
            try:
                logger.info(f"Attempting to scrape from {url_name}: {url}")
                
                # Make request with timeout
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                # Parse HTML
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Try each selector strategy
                for i, selector in enumerate(self.selectors):
                    try:
                        elements = []
                        
                        if 'text_pattern' in selector:
                            # Search for elements containing text pattern
                            if 'tag' in selector:
                                elements = soup.find_all(selector['tag'], selector.get('attrs', {}))
                                # Filter by text pattern
                                elements = [elem for elem in elements 
                                          if re.search(selector['text_pattern'], elem.get_text(), re.IGNORECASE)]
                            else:
                                # General text search
                                elements = soup.find_all(string=re.compile(selector['text_pattern']))
                        else:
                            # Standard tag search
                            elements = soup.find_all(selector['tag'], selector.get('attrs', {}))
                        
                        if elements:
                            logger.info(f"Found {len(elements)} elements with selector {i+1}")
                            
                            # Process each element found
                            for element in elements:
                                text_content = element.get_text() if hasattr(element, 'get_text') else str(element)
                                
                                # Try to extract price using patterns
                                for pattern in self.price_patterns:
                                    matches = re.findall(pattern, text_content, re.IGNORECASE)
                                    if matches:
                                        raw_price = matches[0] if isinstance(matches[0], str) else matches[0][0]
                                        clean_price = self.clean_price(raw_price)
                                        
                                        if clean_price:
                                            logger.info(f"Successfully extracted price: {clean_price}")
                                            return {
                                                'symbol': 'IAM',
                                                'current_price': clean_price,
                                                'source': url_name,
                                                'scraped_from': url,
                                                'raw_text': text_content.strip()[:200],  # First 200 chars
                                                'timestamp': datetime.now().isoformat(),
                                                'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000
                                            }
                                
                                # Alternative: Look for adjacent price elements
                                siblings = []
                                if hasattr(element, 'find_next_sibling'):
                                    siblings.extend(element.find_next_siblings(limit=5))
                                if hasattr(element, 'find_previous_sibling'):
                                    siblings.extend(element.find_previous_siblings(limit=5))
                                
                                for sibling in siblings:
                                    sibling_text = sibling.get_text() if hasattr(sibling, 'get_text') else str(sibling)
                                    for pattern in self.price_patterns:
                                        matches = re.findall(pattern, sibling_text, re.IGNORECASE)
                                        if matches:
                                            raw_price = matches[0] if isinstance(matches[0], str) else matches[0][0]
                                            clean_price = self.clean_price(raw_price)
                                            
                                            if clean_price:
                                                logger.info(f"Successfully extracted price from sibling: {clean_price}")
                                                return {
                                                    'symbol': 'IAM',
                                                    'current_price': clean_price,
                                                    'source': url_name,
                                                    'scraped_from': url,
                                                    'raw_text': f"{text_content[:100]} ... {sibling_text[:100]}",
                                                    'timestamp': datetime.now().isoformat(),
                                                    'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000
                                                }
                    
                    except Exception as e:
                        logger.warning(f"Selector {i+1} failed: {e}")
                        continue
                
                # If we got here, this URL didn't work, try next one
                logger.info(f"No data found on {url_name}, trying next source...")
                
            except requests.RequestException as e:
                logger.error(f"Request failed for {url}: {e}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error scraping {url}: {e}")
                continue
        
        # If all sources failed
        logger.error("All scraping attempts failed")
        return {
            'error': 'Could not fetch IAM stock price from any source',
            'timestamp': datetime.now().isoformat(),
            'processing_time_ms': (datetime.now() - start_time).total_seconds() * 1000
        }
    
    def get_iam_price_with_fallback(self) -> Dict:
        """
        Get IAM price with fallback to demo data if scraping fails
        
        Returns:
            Dict: Price data (real or demo)
        """
        result = self.scrape_iam_price()
        
        if 'error' in result:
            # Fallback to demo data with realistic price movement
            import random
            base_price = 55.0  # Typical IAM price range
            variation = random.uniform(-1.0, 1.5)  # Small daily variation
            demo_price = round(base_price + variation, 2)
            
            logger.warning(f"Using demo data: {demo_price}")
            return {
                'symbol': 'IAM',
                'current_price': demo_price,
                'source': 'demo_fallback',
                'is_demo': True,
                'demo_note': 'Live data not available, showing realistic demo price',
                'timestamp': datetime.now().isoformat()
            }
        
        return result


# Global instance
scraper = MoroccanStockScraper()
