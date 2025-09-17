"""
Portfolio Manager for PriceLabs API
Maps API keys to portfolio names and manages listing associations
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pricelabs_api import PriceLabsAPI

# Portfolio configuration from appscript.js
PORTFOLIO_CONFIG = {
    'utah': {
        'api_key': 'iJO6RszXvTHxNVfeVLbot1oYhUyPye8bZbyp5apV',
        'name': 'Utah Portfolio',
        'description': 'Utah properties'
    },
    'california': {
        'api_key': 'PGNkidBKeuOW2G6DQL91VRdPM2wTaid5w64EzrVE',
        'name': 'California Portfolio', 
        'description': 'California properties'
    },
    'default': {
        'api_key': 'i7wVYNZwf26GNqjtxwrEW3yDppK0h3nECXMRXFMS',
        'name': 'Main Portfolio',
        'description': 'Main/default portfolio'
    },
    'special': {
        'api_key': 'enCAf5AYjn2lzIgQuiBi4L489DcIoCA0j5wCou6J',
        'name': 'Special Account',
        'description': 'Special account portfolio'
    }
}

class PortfolioManager:
    def __init__(self):
        self.portfolios = PORTFOLIO_CONFIG
        self.listing_cache = {}  # Cache for listing data
        self.portfolio_listing_map = {}  # Maps listing_id -> portfolio_key
        self.listing_name_map = {}  # Maps listing_id -> listing_name
        self.last_refresh = None
        
    def refresh_all_listings(self, skip_hidden: bool = False, only_syncing: bool = False) -> Dict:
        """
        Fetch all listings from all portfolios and build mapping
        
        Returns:
            Dict with portfolio data and listings
        """
        print(f"Refreshing all portfolio listings...")
        all_portfolio_data = {}
        
        for portfolio_key, portfolio_info in self.portfolios.items():
            print(f"\nFetching listings from {portfolio_info['name']}...")
            
            api = PriceLabsAPI(api_key=portfolio_info['api_key'])
            
            try:
                response = api.get_all_listings(
                    skip_hidden=skip_hidden,
                    only_syncing=only_syncing
                )
                
                if 'listings' in response:
                    listings = response['listings']
                    print(f"  Found {len(listings)} listings")
                    
                    # Store portfolio data
                    all_portfolio_data[portfolio_key] = {
                        'portfolio_name': portfolio_info['name'],
                        'portfolio_description': portfolio_info['description'],
                        'listing_count': len(listings),
                        'listings': listings
                    }
                    
                    # Build mapping for each listing
                    for listing in listings:
                        listing_id = listing.get('id')
                        listing_name = listing.get('name', '')
                        
                        # Map listing to portfolio
                        self.portfolio_listing_map[listing_id] = portfolio_key
                        self.listing_name_map[listing_id] = listing_name
                        
                        # Cache full listing data
                        self.listing_cache[listing_id] = {
                            **listing,
                            'portfolio_key': portfolio_key,
                            'portfolio_name': portfolio_info['name']
                        }
                else:
                    print(f"  No listings found or error: {response}")
                    all_portfolio_data[portfolio_key] = {
                        'portfolio_name': portfolio_info['name'],
                        'portfolio_description': portfolio_info['description'],
                        'listing_count': 0,
                        'listings': [],
                        'error': response.get('error', 'Unknown error')
                    }
                    
            except Exception as e:
                print(f"  Error fetching from {portfolio_info['name']}: {e}")
                all_portfolio_data[portfolio_key] = {
                    'portfolio_name': portfolio_info['name'],
                    'portfolio_description': portfolio_info['description'],
                    'listing_count': 0,
                    'listings': [],
                    'error': str(e)
                }
        
        self.last_refresh = datetime.now().isoformat()
        
        # Print summary
        print("\n" + "="*60)
        print("PORTFOLIO SUMMARY")
        print("="*60)
        total_listings = 0
        for portfolio_key, data in all_portfolio_data.items():
            count = data['listing_count']
            total_listings += count
            print(f"{data['portfolio_name']:25} {count:5} listings")
        print("-"*60)
        print(f"{'TOTAL':25} {total_listings:5} listings")
        
        return all_portfolio_data
    
    def get_listing_portfolio(self, listing_id: str) -> Optional[Dict]:
        """
        Get portfolio information for a specific listing
        
        Args:
            listing_id: The listing ID to lookup
            
        Returns:
            Dict with portfolio info or None if not found
        """
        portfolio_key = self.portfolio_listing_map.get(listing_id)
        
        if portfolio_key:
            return {
                'portfolio_key': portfolio_key,
                'portfolio_name': self.portfolios[portfolio_key]['name'],
                'api_key': self.portfolios[portfolio_key]['api_key'],
                'listing_name': self.listing_name_map.get(listing_id, 'Unknown')
            }
        return None
    
    def get_api_key_for_listing(self, listing_id: str) -> Optional[str]:
        """
        Get the API key for a specific listing
        
        Args:
            listing_id: The listing ID
            
        Returns:
            API key string or None if not found
        """
        portfolio_info = self.get_listing_portfolio(listing_id)
        return portfolio_info['api_key'] if portfolio_info else None
    
    def search_listing_by_name(self, search_term: str) -> List[Dict]:
        """
        Search for listings by name (partial match)
        
        Args:
            search_term: Search string (case-insensitive)
            
        Returns:
            List of matching listings with portfolio info
        """
        matches = []
        search_lower = search_term.lower()
        
        for listing_id, listing_name in self.listing_name_map.items():
            if search_lower in listing_name.lower():
                portfolio_key = self.portfolio_listing_map[listing_id]
                matches.append({
                    'listing_id': listing_id,
                    'listing_name': listing_name,
                    'portfolio_key': portfolio_key,
                    'portfolio_name': self.portfolios[portfolio_key]['name'],
                    'full_data': self.listing_cache.get(listing_id, {})
                })
        
        return matches
    
    def get_portfolio_listings(self, portfolio_key: str) -> List[Dict]:
        """
        Get all listings for a specific portfolio
        
        Args:
            portfolio_key: Key of the portfolio (utah, california, default, special)
            
        Returns:
            List of listings in that portfolio
        """
        listings = []
        for listing_id, p_key in self.portfolio_listing_map.items():
            if p_key == portfolio_key:
                listings.append({
                    'listing_id': listing_id,
                    'listing_name': self.listing_name_map[listing_id],
                    'full_data': self.listing_cache.get(listing_id, {})
                })
        return listings
    
    def save_mapping_to_file(self, filename: str = 'portfolio_mapping.json'):
        """Save the current mapping to a JSON file for reference"""
        data = {
            'last_refresh': self.last_refresh,
            'portfolios': {}
        }
        
        for portfolio_key in self.portfolios.keys():
            listings = self.get_portfolio_listings(portfolio_key)
            data['portfolios'][portfolio_key] = {
                'name': self.portfolios[portfolio_key]['name'],
                'description': self.portfolios[portfolio_key]['description'],
                'listing_count': len(listings),
                'listings': [
                    {
                        'id': l['listing_id'],
                        'name': l['listing_name'],
                        'pms': l['full_data'].get('pms', ''),
                        'city': l['full_data'].get('city_name', ''),
                        'state': l['full_data'].get('state', ''),
                        'bedrooms': l['full_data'].get('no_of_bedrooms', 0)
                    }
                    for l in listings
                ]
            }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Portfolio mapping saved to {filename}")
        return filename
    
    def get_api_client_for_listing(self, listing_id: str) -> Optional[PriceLabsAPI]:
        """
        Get a configured API client for a specific listing
        
        Args:
            listing_id: The listing ID
            
        Returns:
            Configured PriceLabsAPI instance or None
        """
        api_key = self.get_api_key_for_listing(listing_id)
        if api_key:
            return PriceLabsAPI(api_key=api_key)
        return None
    
    def get_all_active_listings(self) -> List[Dict]:
        """Get all active (push_enabled=true) listings across all portfolios"""
        active_listings = []
        for listing_id, listing_data in self.listing_cache.items():
            if listing_data.get('push_enabled', False):
                active_listings.append({
                    'listing_id': listing_id,
                    'listing_name': self.listing_name_map[listing_id],
                    'portfolio': listing_data['portfolio_name'],
                    'data': listing_data
                })
        return active_listings


# Convenience functions
def get_portfolio_manager() -> PortfolioManager:
    """Get or create a portfolio manager instance"""
    manager = PortfolioManager()
    manager.refresh_all_listings()
    return manager


def quick_listing_lookup(listing_id: str) -> Tuple[str, str]:
    """
    Quick lookup of API key and portfolio name for a listing
    
    Returns:
        Tuple of (api_key, portfolio_name) or (None, None) if not found
    """
    manager = PortfolioManager()
    manager.refresh_all_listings(skip_hidden=False, only_syncing=False)
    
    info = manager.get_listing_portfolio(listing_id)
    if info:
        return info['api_key'], info['portfolio_name']
    return None, None


if __name__ == '__main__':
    # Test the portfolio manager
    print("Initializing Portfolio Manager...")
    print("="*60)
    
    manager = get_portfolio_manager()
    
    # Save mapping to file
    manager.save_mapping_to_file()
    
    # Example: Search for a listing
    print("\n" + "="*60)
    print("EXAMPLE: Searching for listings with 'Mountain' in name...")
    results = manager.search_listing_by_name('Mountain')
    for r in results[:3]:  # Show first 3 results
        print(f"  {r['listing_id']}: {r['listing_name'][:50]}... ({r['portfolio_name']})")
    
    # Example: Get active listings count
    active = manager.get_all_active_listings()
    print(f"\nTotal active listings (push_enabled=true): {len(active)}")