"""
Example usage of the Portfolio Manager
Shows how other Python functions can easily use the portfolio system
"""

from portfolio_manager import PortfolioManager, get_portfolio_manager
from pricelabs_api import PriceLabsAPI

def example_get_listing_prices(listing_id: str):
    """
    Example: Get prices for a specific listing using the correct API key
    """
    print(f"\n=== Getting prices for listing {listing_id} ===")
    
    # Initialize portfolio manager
    manager = PortfolioManager()
    manager.refresh_all_listings()
    
    # Get the correct API client for this listing
    api_client = manager.get_api_client_for_listing(listing_id)
    
    if api_client:
        portfolio_info = manager.get_listing_portfolio(listing_id)
        print(f"Found listing in: {portfolio_info['portfolio_name']}")
        print(f"Listing name: {portfolio_info['listing_name']}")
        
        # Make API call with the correct key
        from datetime import datetime, timedelta
        today = datetime.now().strftime('%Y-%m-%d')
        next_week = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        price_request = [{
            'id': listing_id,
            'pms': manager.listing_cache[listing_id].get('pms', 'airbnb'),
            'dateFrom': today,
            'dateTo': next_week
        }]
        
        result = api_client.get_listing_prices(price_request)
        print(f"Price API Response: {result}")
    else:
        print(f"Listing {listing_id} not found in any portfolio!")


def example_bulk_operations_by_portfolio(portfolio_key: str):
    """
    Example: Perform bulk operations on all listings in a portfolio
    """
    print(f"\n=== Bulk operations for {portfolio_key} portfolio ===")
    
    manager = PortfolioManager()
    manager.refresh_all_listings()
    
    # Get all listings in this portfolio
    listings = manager.get_portfolio_listings(portfolio_key)
    print(f"Found {len(listings)} listings in {portfolio_key}")
    
    if listings:
        # Get API client for this portfolio
        api = PriceLabsAPI(api_key=manager.portfolios[portfolio_key]['api_key'])
        
        # Example: Update min price for first 3 listings
        update_batch = []
        for listing in listings[:3]:
            update_batch.append({
                'id': listing['listing_id'],
                'pms': listing['full_data'].get('pms', 'airbnb'),
                'min': 150  # Example new minimum price
            })
        
        if update_batch:
            print(f"Updating {len(update_batch)} listings...")
            # Uncomment to actually update:
            # result = api.update_listings(update_batch)
            # print(f"Update result: {result}")
            print("(Update skipped in test mode)")


def example_search_and_operate(search_term: str):
    """
    Example: Search for listings by name and perform operations
    """
    print(f"\n=== Searching for '{search_term}' ===")
    
    manager = PortfolioManager()
    manager.refresh_all_listings()
    
    # Search for listings
    results = manager.search_listing_by_name(search_term)
    print(f"Found {len(results)} matching listings")
    
    for result in results[:5]:  # Show first 5
        print(f"\nListing: {result['listing_name'][:60]}...")
        print(f"  ID: {result['listing_id']}")
        print(f"  Portfolio: {result['portfolio_name']}")
        print(f"  City: {result['full_data'].get('city_name', 'N/A')}")
        print(f"  Bedrooms: {result['full_data'].get('no_of_bedrooms', 'N/A')}")
        print(f"  Base Price: ${result['full_data'].get('base', 'N/A')}")


def example_cross_portfolio_summary():
    """
    Example: Generate summary across all portfolios
    """
    print("\n=== Cross-Portfolio Summary ===")
    
    manager = PortfolioManager()
    manager.refresh_all_listings()
    
    # Get active listings across all portfolios
    active_listings = manager.get_all_active_listings()
    
    # Group by portfolio
    portfolio_summary = {}
    for listing in active_listings:
        portfolio = listing['portfolio']
        if portfolio not in portfolio_summary:
            portfolio_summary[portfolio] = {
                'count': 0,
                'total_base_price': 0,
                'cities': set()
            }
        
        portfolio_summary[portfolio]['count'] += 1
        base_price = listing['data'].get('base', 0)
        if base_price:
            portfolio_summary[portfolio]['total_base_price'] += base_price
        
        city = listing['data'].get('city_name')
        if city:
            portfolio_summary[portfolio]['cities'].add(city)
    
    # Print summary
    for portfolio, stats in portfolio_summary.items():
        avg_base = stats['total_base_price'] / stats['count'] if stats['count'] > 0 else 0
        print(f"\n{portfolio}:")
        print(f"  Active Listings: {stats['count']}")
        print(f"  Average Base Price: ${avg_base:.2f}")
        print(f"  Cities: {', '.join(sorted(stats['cities']))}")


if __name__ == '__main__':
    print("Portfolio Manager Usage Examples")
    print("="*60)
    
    # Example 1: Get listing prices with auto API key detection
    # Using a listing from the Main Portfolio as example
    example_get_listing_prices('634197676956646902')
    
    # Example 2: Bulk operations on a portfolio
    example_bulk_operations_by_portfolio('utah')
    
    # Example 3: Search for listings
    example_search_and_operate('Eden')
    
    # Example 4: Cross-portfolio summary
    example_cross_portfolio_summary()
    
    print("\n" + "="*60)
    print("Examples completed!")