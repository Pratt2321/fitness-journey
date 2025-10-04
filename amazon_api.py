"""
Amazon Product Advertising API (PA-API v5) Helper
Fetches product images and details using Amazon's Product Advertising API.

Author: Pratham Pradhan
"""

import os
import requests
import hashlib
import hmac
import base64
import time
from datetime import datetime
from typing import Optional, Dict, Any
import json
import pandas as pd

class AmazonProductAPI:
    """
    Amazon Product Advertising API v5 client for fetching product information.
    """
    
    def __init__(self):
        """Initialize the Amazon API client with credentials from environment variables."""
        self.access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.associate_tag = os.getenv('AMAZON_ASSOCIATE_TAG')
        self.region = os.getenv('AWS_REGION', 'us-east-1')
        
        if not all([self.access_key, self.secret_key, self.associate_tag]):
            raise ValueError(
                "Missing required environment variables. Please set:\n"
                "- AWS_ACCESS_KEY_ID\n"
                "- AWS_SECRET_ACCESS_KEY\n"
                "- AMAZON_ASSOCIATE_TAG"
            )
        
        # API endpoints for different regions
        self.endpoints = {
            'us-east-1': 'webservices.amazon.com',
            'us-west-2': 'webservices.amazon.com',
            'eu-west-1': 'webservices.amazon.co.uk',
            'ap-northeast-1': 'webservices.amazon.co.jp'
        }
        
        self.host = self.endpoints.get(self.region, 'webservices.amazon.com')
        self.uri = '/paapi5/searchitems'
        self.url = f'https://{self.host}{self.uri}'
    
    def _create_signature(self, method: str, uri: str, query_string: str, 
                         payload: str, timestamp: str) -> str:
        """Create AWS signature for API authentication."""
        # Create canonical request
        canonical_request = f"{method}\n{uri}\n{query_string}\nhost:{self.host}\nx-amz-date:{timestamp}\n\nhost;x-amz-date\n{hashlib.sha256(payload.encode('utf-8')).hexdigest()}"
        
        # Create string to sign
        string_to_sign = f"AWS4-HMAC-SHA256\n{timestamp}\n{self.region}/product-advertising-api/aws4_request\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
        
        # Create signing key
        def sign(key: bytes, msg: str) -> bytes:
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
        
        date_key = sign(f"AWS4{self.secret_key}".encode('utf-8'), datetime.utcnow().strftime('%Y%m%d'))
        region_key = sign(date_key, self.region)
        service_key = sign(region_key, 'product-advertising-api')
        signing_key = sign(service_key, 'aws4_request')
        
        # Create signature
        signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        
        return signature
    
    def _get_headers(self, payload: str) -> Dict[str, str]:
        """Generate headers for the API request."""
        timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        
        headers = {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Amz-Date': timestamp,
            'Authorization': f'AWS4-HMAC-SHA256 Credential={self.access_key}/{datetime.utcnow().strftime("%Y%m%d")}/{self.region}/product-advertising-api/aws4_request, SignedHeaders=host;x-amz-date, Signature={self._create_signature("POST", self.uri, "", payload, timestamp)}',
            'Host': self.host
        }
        
        return headers
    
    def search_products(self, keywords: str, search_index: str = "All", 
                       item_count: int = 10) -> Optional[Dict[str, Any]]:
        """
        Search for products using keywords.
        
        Args:
            keywords: Search keywords
            search_index: Amazon search index (e.g., "All", "HealthPersonalCare")
            item_count: Number of items to return (max 10)
        
        Returns:
            API response as dictionary or None if error
        """
        payload = {
            "PartnerTag": self.associate_tag,
            "PartnerType": "Associates",
            "Keywords": keywords,
            "SearchIndex": search_index,
            "ItemCount": min(item_count, 10),
            "Resources": [
                "Images.Primary.Large",
                "Images.Variants.Large",
                "ItemInfo.Title",
                "ItemInfo.ByLineInfo",
                "ItemInfo.Classifications",
                "Offers.Listings.Price"
            ]
        }
        
        try:
            response = requests.post(
                self.url,
                headers=self._get_headers(json.dumps(payload)),
                data=json.dumps(payload),
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None
    
    def get_product_by_asin(self, asin: str) -> Optional[Dict[str, Any]]:
        """
        Get product details by ASIN.
        
        Args:
            asin: Amazon Standard Identification Number
        
        Returns:
            Product details or None if not found
        """
        payload = {
            "PartnerTag": self.associate_tag,
            "PartnerType": "Associates",
            "ItemIds": [asin],
            "Resources": [
                "Images.Primary.Large",
                "Images.Variants.Large",
                "ItemInfo.Title",
                "ItemInfo.ByLineInfo",
                "ItemInfo.Classifications",
                "Offers.Listings.Price"
            ]
        }
        
        try:
            response = requests.post(
                self.url,
                headers=self._get_headers(json.dumps(payload)),
                data=json.dumps(payload),
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Request failed: {str(e)}")
            return None
    
    def get_product_image(self, asin: str) -> Optional[str]:
        """
        Get product image URL by ASIN.
        
        Args:
            asin: Amazon Standard Identification Number
        
        Returns:
            Image URL or None if not found
        """
        if not asin or pd.isna(asin):
            return None
        
        # Clean ASIN (remove any whitespace)
        asin = str(asin).strip()
        
        try:
            response = self.get_product_by_asin(asin)
            
            if response and 'SearchResult' in response:
                items = response['SearchResult'].get('Items', [])
                if items:
                    item = items[0]
                    images = item.get('Images', {})
                    
                    # Try primary large image first
                    primary = images.get('Primary', {})
                    if primary and 'Large' in primary:
                        return primary['Large']['URL']
                    
                    # Try variants
                    variants = images.get('Variants', [])
                    for variant in variants:
                        if 'Large' in variant:
                            return variant['Large']['URL']
            
            return None
            
        except Exception as e:
            print(f"Error fetching image for ASIN {asin}: {str(e)}")
            return None
    
    def search_product_image(self, product_name: str) -> Optional[str]:
        """
        Search for product image using product name.
        
        Args:
            product_name: Name of the product to search for
        
        Returns:
            Image URL or None if not found
        """
        try:
            # Search for the product
            response = self.search_products(product_name, search_index="HealthPersonalCare", item_count=1)
            
            if response and 'SearchResult' in response:
                items = response['SearchResult'].get('Items', [])
                if items:
                    item = items[0]
                    images = item.get('Images', {})
                    
                    # Try primary large image first
                    primary = images.get('Primary', {})
                    if primary and 'Large' in primary:
                        return primary['Large']['URL']
                    
                    # Try variants
                    variants = images.get('Variants', [])
                    for variant in variants:
                        if 'Large' in variant:
                            return variant['Large']['URL']
            
            return None
            
        except Exception as e:
            print(f"Error searching for image: {str(e)}")
            return None

# Example usage and testing
if __name__ == "__main__":
    # Test the API (requires environment variables to be set)
    try:
        api = AmazonProductAPI()
        
        # Test with a known ASIN
        test_asin = "B0143NQVQ6"  # RXBAR Protein Bars
        image_url = api.get_product_image(test_asin)
        
        if image_url:
            print(f"✅ Successfully fetched image: {image_url}")
        else:
            print("❌ No image found")
            
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")
