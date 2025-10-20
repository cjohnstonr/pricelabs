"""
Dashboard Server for PriceLabs Listing Overview
Serves aggregated listing data from all portfolios
"""

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from portfolio_manager import PortfolioManager
import os

app = Flask(__name__)
CORS(app)

# Store manager instance
manager = None

def get_manager():
    """Get or create portfolio manager instance"""
    global manager
    if manager is None:
        manager = PortfolioManager()
    return manager

@app.route('/')
def index():
    """Serve the dashboard HTML"""
    return send_from_directory('.', 'listingDashboard.html')

@app.route('/api/listings/dashboard')
def get_dashboard_data():
    """
    Get all listings from all portfolios with key metrics

    Returns:
        JSON array of listings with portfolio info and metrics
    """
    try:
        mgr = get_manager()

        # Refresh all portfolio data
        all_portfolio_data = mgr.refresh_all_listings(skip_hidden=False, only_syncing=False)

        # Transform into dashboard format
        dashboard_listings = []

        for portfolio_key, portfolio_data in all_portfolio_data.items():
            portfolio_name = portfolio_data['portfolio_name']
            api_key = mgr.portfolios[portfolio_key]['api_key']

            # Mask API key (show last 4 characters only)
            masked_key = '***' + api_key[-4:] if len(api_key) > 4 else '***'

            for listing in portfolio_data.get('listings', []):
                dashboard_listings.append({
                    # Identity
                    'id': listing.get('id'),
                    'name': listing.get('name', 'Unnamed'),
                    'portfolio': portfolio_name,
                    'portfolio_key': portfolio_key,
                    'api_key': masked_key,

                    # Location
                    'city': listing.get('city_name', 'N/A'),
                    'state': listing.get('state', 'N/A'),
                    'bedrooms': listing.get('no_of_bedrooms', 0),
                    'latitude': listing.get('latitude', ''),
                    'longitude': listing.get('longitude', ''),
                    'pms': listing.get('pms', 'N/A'),

                    # MPI Metrics
                    'mpi_30': listing.get('mpi_next_30', 0),
                    'mpi_60': listing.get('mpi_next_60', 0),
                    'mpi_90': listing.get('mpi_next_90', 0),
                    'mpi_120': listing.get('mpi_next_120', 0),
                    'mpi_180': listing.get('mpi_next_180', 0),

                    # Occupancy Metrics
                    'occ_7': listing.get('occupancy_next_7', '0 %'),
                    'occ_30': listing.get('occupancy_next_30', '0 %'),
                    'occ_60': listing.get('occupancy_next_60', '0 %'),
                    'market_occ_7': listing.get('market_occupancy_next_7', '0 %'),
                    'market_occ_30': listing.get('market_occupancy_next_30', '0 %'),
                    'market_occ_60': listing.get('market_occupancy_next_60', '0 %'),

                    # Revenue Metrics
                    'revenue_past_30': listing.get('revenue_past_30', 0),
                    'revenue_next_30': listing.get('revenue_next_30', 0),
                    'revenue_next_180': listing.get('revenue_next_180', 0),

                    # ADR Metrics
                    'adr_past_90': listing.get('adr_past_90', 0),
                    'adr_next_180': listing.get('adr_next_180', 0),

                    # Status
                    'push_enabled': listing.get('push_enabled', False),
                    'last_pushed': listing.get('last_date_pushed', 'Never'),
                    'last_booked': listing.get('last_booked_date', 'N/A'),
                    'is_hidden': listing.get('isHidden', False),

                    # Sync Status - determines if actively syncing with PMS
                    'sync_status': 'Syncing' if listing.get('push_enabled', False) else 'Not Syncing'
                })

        return jsonify({
            'success': True,
            'count': len(dashboard_listings),
            'listings': dashboard_listings,
            'portfolios': [
                {'key': k, 'name': v['name']}
                for k, v in mgr.portfolios.items()
            ]
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/refresh')
def refresh_data():
    """Force refresh of all portfolio data"""
    try:
        global manager
        manager = None  # Force recreation
        return jsonify({'success': True, 'message': 'Data refreshed'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("PriceLabs Listing Dashboard Server")
    print("=" * 60)
    print("\nStarting server on http://localhost:5051")
    print("Dashboard will be available at: http://localhost:5051/")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 60)

    app.run(debug=True, port=5051, host='0.0.0.0')
