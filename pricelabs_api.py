"""
PriceLabs Customer API Client
Provides functions to interact with all PriceLabs API endpoints
"""

import requests
from typing import Optional, Dict, List, Any
from datetime import datetime

# Default API key from the appscript.js file
DEFAULT_API_KEY = 'i7wVYNZwf26GNqjtxwrEW3yDppK0h3nECXMRXFMS'
BASE_URL = 'https://api.pricelabs.co'

class PriceLabsAPI:
    def __init__(self, api_key: str = DEFAULT_API_KEY):
        self.api_key = api_key
        self.headers = {
            'X-API-Key': self.api_key,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
    def _make_request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                     json_data: Optional[Dict] = None) -> Dict:
        """Make HTTP request to PriceLabs API"""
        url = f"{BASE_URL}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=json_data,
                timeout=300  # 5 minutes timeout as recommended
            )
            
            # Return raw response data
            if response.status_code == 204:  # No content
                return {'status': 'success', 'message': 'Operation completed successfully'}
            
            try:
                return response.json()
            except:
                return {'raw_response': response.text, 'status_code': response.status_code}
                
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status': 'failed'}
    
    # ============= LISTINGS ENDPOINTS =============
    
    def get_all_listings(self, skip_hidden: Optional[bool] = False, 
                         only_syncing: Optional[bool] = False) -> Dict:
        """Get all listings in an account"""
        params = {}
        if skip_hidden:
            params['skip_hidden'] = 'true'
        if only_syncing:
            params['only_syncing_listings'] = 'true'
            
        return self._make_request('GET', '/v1/listings', params=params)
    
    def update_listings(self, listings: List[Dict]) -> Dict:
        """Update one or more listings in an account
        
        Args:
            listings: List of dicts with keys: id, pms, and optional min/base/max
        """
        return self._make_request('POST', '/v1/listings', json_data={'listings': listings})
    
    def get_listing(self, listing_id: str) -> Dict:
        """Get a specific listing in an account"""
        return self._make_request('GET', f'/v1/listings/{listing_id}')
    
    def add_listing_data(self, listing_id: str, pms_name: str = 'bookingsync') -> Dict:
        """Import newly added listings from PMS (BookingSync only)"""
        data = {
            'listing': listing_id,
            'pms_name': pms_name
        }
        return self._make_request('POST', '/v1/add_listing_data', json_data=data)
    
    # ============= DATE SPECIFIC OVERRIDES (DSO) ENDPOINTS =============
    
    def get_listing_overrides(self, listing_id: str, pms: str) -> Dict:
        """Fetch a listing's date specific overrides"""
        params = {'pms': pms}
        return self._make_request('GET', f'/v1/listings/{listing_id}/overrides', params=params)
    
    def update_listing_overrides(self, listing_id: str, pms: str, overrides: List[Dict], 
                                 update_children: bool = False) -> Dict:
        """Add/Update a listing's date specific override
        
        Args:
            listing_id: ID of the listing
            pms: PMS name
            overrides: List of override dicts with date, price, price_type, etc.
            update_children: Whether to update child listings
        """
        data = {
            'pms': pms,
            'update_children': update_children,
            'overrides': overrides
        }
        return self._make_request('POST', f'/v1/listings/{listing_id}/overrides', json_data=data)
    
    def delete_listing_overrides(self, listing_id: str, pms: str, dates: List[str], 
                                 update_children: bool = False) -> Dict:
        """Delete a listing's date specific override
        
        Args:
            listing_id: ID of the listing
            pms: PMS name
            dates: List of dates to delete overrides for
            update_children: Whether to delete from child listings
        """
        data = {
            'pms': pms,
            'update_children': update_children,
            'overrides': [{'date': date} for date in dates]
        }
        return self._make_request('DELETE', f'/v1/listings/{listing_id}/overrides', json_data=data)
    
    # ============= PRICES ENDPOINTS =============
    
    def get_listing_prices(self, listings: List[Dict]) -> Dict:
        """Get prices for listings
        
        Args:
            listings: List of dicts with keys: id, pms, and optional dateFrom/dateTo/reason
        """
        return self._make_request('POST', '/v1/listing_prices', json_data={'listings': listings})
    
    def fetch_rate_plans(self, listing_id: str, pms_name: str) -> Dict:
        """Fetch rate plan adjustments for listings"""
        params = {
            'listing_id': listing_id,
            'pms_name': pms_name
        }
        return self._make_request('GET', '/v1/fetch_rate_plans', params=params)
    
    # ============= NEIGHBORHOOD DATA ENDPOINT =============
    
    def get_neighborhood_data(self, listing_id: str, pms: str) -> Dict:
        """Get neighborhood data for a listing"""
        params = {
            'listing_id': listing_id,
            'pms': pms
        }
        return self._make_request('GET', '/v1/neighborhood_data', params=params)
    
    # ============= RESERVATIONS ENDPOINT =============
    
    def get_reservation_data(self, pms: Optional[str] = None, 
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None,
                            limit: int = 100,
                            offset: int = 0) -> Dict:
        """Get reservations received from PMS with rental revenue info
        
        Args:
            pms: PMS name
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            limit: Number of results per page (max 100)
            offset: Pagination offset
        """
        params = {
            'limit': str(limit),
            'offset': str(offset)
        }
        
        if pms:
            params['pms'] = pms
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
            
        return self._make_request('GET', '/v1/reservation_data', params=params)


# Convenience functions for quick testing
def quick_test():
    """Quick test of API connectivity"""
    api = PriceLabsAPI()
    print("Testing API connectivity...")
    result = api.get_all_listings(skip_hidden=True, only_syncing=True)
    if 'error' in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Success! Found {len(result.get('listings', []))} listings")
    return result


if __name__ == '__main__':
    # Quick test when run directly
    quick_test()