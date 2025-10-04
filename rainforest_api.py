"""
Rainforest API Helper for Product Images
Simple API to fetch product images using ASINs.

Author: Pratham Pradhan
"""

import requests
import os
from typing import Optional, Dict
from dotenv import load_dotenv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Load environment variables from .env file
load_dotenv()

class RainforestAPI:
    """
    Rainforest API client for fetching product images.
    Much simpler than Amazon PA-API!
    """
    
    def __init__(self):
        """Initialize the Rainforest API client."""
        # Try to load from .env file first
        load_dotenv()
        self.api_key = os.getenv('RAINFOREST_API_KEY')
        
        # If not found, use the hardcoded key for now
        if not self.api_key:
            self.api_key = '967A30D6573646428C3C29138EEF131B'
            print("Using hardcoded API key for testing")
        
        self.base_url = 'https://api.rainforestapi.com/request'
        
        # Cache for storing image URLs
        self.cache_file = 'image_cache.json'
        self.image_cache = self._load_cache()
        
        # Rate limiting (1 request per second to be safe)
        self.last_request_time = 0
        self.min_request_interval = 1.0
    
    def _load_cache(self) -> Dict[str, str]:
        """Load image cache from file."""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def _save_cache(self):
        """Save image cache to file."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(self.image_cache, f)
        except:
            pass
    
    def _rate_limit(self):
        """Ensure we don't exceed rate limits."""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_request_interval:
            time.sleep(self.min_request_interval - time_since_last)
        self.last_request_time = time.time()
    
    def get_product_image(self, asin: str) -> Optional[str]:
        """
        Get product image URL by ASIN (with caching).
        
        Args:
            asin: Amazon Standard Identification Number
        
        Returns:
            Image URL or None if not found
        """
        if not asin or asin == 'No ASIN':
            return None
        
        # Check cache first
        if asin in self.image_cache:
            return self.image_cache[asin]
        
        try:
            # Rate limiting
            self._rate_limit()
            
            params = {
                'api_key': self.api_key,
                'amazon_domain': 'amazon.com',
                'asin': asin,
                'type': 'product'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract main image URL
            image_url = None
            if 'product' in data and 'main_image' in data['product']:
                image_url = data['product']['main_image']['link']
            
            # Cache the result
            self.image_cache[asin] = image_url
            self._save_cache()
            
            return image_url
            
        except Exception as e:
            print(f"Error fetching image for ASIN {asin}: {str(e)}")
            # Cache the error (None) to avoid retrying
            self.image_cache[asin] = None
            self._save_cache()
            return None
    
    def get_multiple_product_images(self, asins: list) -> Dict[str, str]:
        """
        Get multiple product images in parallel (with caching).
        
        Args:
            asins: List of ASINs
        
        Returns:
            Dictionary mapping ASIN to image URL
        """
        results = {}
        
        # Check cache first
        uncached_asins = []
        for asin in asins:
            if asin in self.image_cache:
                results[asin] = self.image_cache[asin]
            else:
                uncached_asins.append(asin)
        
        if not uncached_asins:
            return results
        
        # Fetch uncached images in parallel
        def fetch_single_image(asin):
            return asin, self.get_product_image(asin)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            future_to_asin = {executor.submit(fetch_single_image, asin): asin for asin in uncached_asins}
            
            for future in as_completed(future_to_asin):
                asin, image_url = future.result()
                results[asin] = image_url
        
        return results
    
    def get_product_info(self, asin: str) -> Optional[dict]:
        """
        Get full product information by ASIN.
        
        Args:
            asin: Amazon Standard Identification Number
        
        Returns:
            Product data dictionary or None if not found
        """
        if not asin or asin == 'No ASIN':
            return None
        
        try:
            params = {
                'api_key': self.api_key,
                'amazon_domain': 'amazon.com',
                'asin': asin,
                'type': 'product'
            }
            
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            print(f"Error fetching product info for ASIN {asin}: {str(e)}")
            return None

# Example usage
if __name__ == "__main__":
    # Test the API
    try:
        api = RainforestAPI()
        
        # Test with AirPods Pro ASIN
        test_asin = "B09JQMJHXY"
        image_url = api.get_product_image(test_asin)
        
        if image_url:
            print(f"✅ Success! Image URL: {image_url}")
        else:
            print("❌ No image found")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set RAINFOREST_API_KEY in your .env file")
    except Exception as e:
        print(f"❌ Error: {e}")
