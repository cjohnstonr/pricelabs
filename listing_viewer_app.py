"""
Flask web application for viewing PriceLabs listing information
Automatically detects the correct API key using portfolio mapping
"""

from flask import Flask, render_template_string, request, jsonify, send_from_directory
from flask_cors import CORS
from portfolio_manager import PortfolioManager
from pricelabs_api import PriceLabsAPI
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize portfolio manager globally
portfolio_manager = PortfolioManager()
portfolio_manager.refresh_all_listings()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PriceLabs Listing Viewer</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
        }
        
        .sidebar {
            width: 400px;
            background: white;
            box-shadow: 2px 0 20px rgba(0,0,0,0.1);
            overflow-y: auto;
            transition: transform 0.3s ease;
        }
        
        .sidebar.collapsed {
            transform: translateX(-350px);
        }
        
        .toggle-btn {
            position: absolute;
            right: -40px;
            top: 20px;
            background: white;
            border: none;
            padding: 10px;
            cursor: pointer;
            border-radius: 0 5px 5px 0;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
        }
        
        .sidebar-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        
        .sidebar-header h1 {
            font-size: 24px;
            margin-bottom: 10px;
        }
        
        .listing-id-display {
            font-size: 14px;
            opacity: 0.9;
            word-break: break-all;
        }
        
        .portfolio-badge {
            display: inline-block;
            background: rgba(255,255,255,0.2);
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            margin-top: 10px;
        }
        
        .sidebar-content {
            padding: 20px;
        }
        
        .info-section {
            margin-bottom: 25px;
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }
        
        .info-section h3 {
            color: #333;
            font-size: 16px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
        }
        
        .info-section h3::before {
            content: '';
            display: inline-block;
            width: 4px;
            height: 16px;
            background: #764ba2;
            margin-right: 8px;
        }
        
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .info-item:last-child {
            border-bottom: none;
        }
        
        .info-label {
            color: #666;
            font-size: 14px;
        }
        
        .info-value {
            color: #333;
            font-size: 14px;
            font-weight: 500;
            text-align: right;
            max-width: 60%;
            word-break: break-word;
        }
        
        .main-content {
            flex: 1;
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        
        .welcome-card {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            max-width: 600px;
            text-align: center;
        }
        
        .welcome-card h2 {
            color: #333;
            margin-bottom: 20px;
        }
        
        .welcome-card p {
            color: #666;
            margin-bottom: 30px;
            line-height: 1.6;
        }
        
        .listing-input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .listing-input {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 16px;
            transition: border-color 0.3s;
        }
        
        .listing-input:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .load-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: transform 0.2s;
        }
        
        .load-btn:hover {
            transform: translateY(-2px);
        }
        
        .load-btn:active {
            transform: translateY(0);
        }
        
        .error-message {
            background: #fee;
            color: #c33;
            padding: 10px 15px;
            border-radius: 5px;
            margin-top: 10px;
            display: none;
        }
        
        .loading {
            display: none;
            color: #667eea;
            margin-top: 20px;
        }
        
        .spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-right: 10px;
            vertical-align: middle;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            margin-top: 10px;
        }
        
        .stat-item {
            background: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
        }
        
        .stat-value {
            font-size: 20px;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }
        
        .no-data {
            color: #999;
            font-style: italic;
        }
        
        @media (max-width: 768px) {
            .sidebar {
                width: 100%;
                position: absolute;
                z-index: 100;
            }
            
            .main-content {
                padding: 20px;
            }
            
            .welcome-card {
                padding: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="sidebar" id="sidebar">
        <button class="toggle-btn" onclick="toggleSidebar()">☰</button>
        <div class="sidebar-header">
            <h1>Listing Details</h1>
            <div class="listing-id-display" id="listing-id-display">No listing loaded</div>
            <div class="portfolio-badge" id="portfolio-badge" style="display: none;"></div>
        </div>
        <div class="sidebar-content" id="sidebar-content">
            <div style="color: #999; text-align: center; padding: 40px;">
                Load a listing to view details
            </div>
        </div>
    </div>
    
    <div class="main-content">
        <div class="welcome-card">
            <h2>PriceLabs Listing Viewer</h2>
            <p>Enter a listing ID to view its details. The system will automatically detect the correct portfolio and API key.</p>
            
            <div class="listing-input-group">
                <input type="text" 
                       class="listing-input" 
                       id="listing-id-input" 
                       placeholder="Enter Listing ID (e.g., 634197676956646902)"
                       value="{{ listing_id }}">
                <button class="load-btn" onclick="loadListing()">Load Listing</button>
            </div>
            
            <div class="error-message" id="error-message"></div>
            <div class="loading" id="loading">
                <span class="spinner"></span>
                <span>Loading listing data...</span>
            </div>
        </div>
    </div>
    
    <script>
        // Check for listing ID in URL on page load
        window.addEventListener('DOMContentLoaded', (event) => {
            const urlParams = new URLSearchParams(window.location.search);
            const listingId = urlParams.get('listing_id');
            
            if (listingId) {
                document.getElementById('listing-id-input').value = listingId;
                loadListing();
            }
        });
        
        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('collapsed');
        }
        
        function loadListing() {
            const listingId = document.getElementById('listing-id-input').value.trim();
            
            if (!listingId) {
                showError('Please enter a listing ID');
                return;
            }
            
            // Update URL without reloading page
            const url = new URL(window.location);
            url.searchParams.set('listing_id', listingId);
            window.history.pushState({}, '', url);
            
            // Show loading state
            document.getElementById('loading').style.display = 'block';
            document.getElementById('error-message').style.display = 'none';
            
            // Fetch listing data
            fetch(`/api/listing/${listingId}`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById('loading').style.display = 'none';
                    
                    if (data.error) {
                        showError(data.error);
                        return;
                    }
                    
                    displayListingData(data);
                })
                .catch(error => {
                    document.getElementById('loading').style.display = 'none';
                    showError('Failed to load listing: ' + error.message);
                });
        }
        
        function showError(message) {
            const errorDiv = document.getElementById('error-message');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
        
        function displayListingData(data) {
            // Update header
            document.getElementById('listing-id-display').textContent = `ID: ${data.listing_id}`;
            
            const portfolioBadge = document.getElementById('portfolio-badge');
            portfolioBadge.textContent = data.portfolio_name;
            portfolioBadge.style.display = 'inline-block';
            
            // Build content sections
            let contentHTML = '';
            
            // Basic Information
            contentHTML += `
                <div class="info-section">
                    <h3>Basic Information</h3>
                    <div class="info-item">
                        <span class="info-label">Name</span>
                        <span class="info-value">${data.listing_data.name || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">PMS</span>
                        <span class="info-value">${data.listing_data.pms || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Bedrooms</span>
                        <span class="info-value">${data.listing_data.no_of_bedrooms || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Sync Enabled</span>
                        <span class="info-value">${data.listing_data.push_enabled ? '✅ Yes' : '❌ No'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Hidden</span>
                        <span class="info-value">${data.listing_data.isHidden ? 'Yes' : 'No'}</span>
                    </div>
                </div>
            `;
            
            // Location
            contentHTML += `
                <div class="info-section">
                    <h3>Location</h3>
                    <div class="info-item">
                        <span class="info-label">City</span>
                        <span class="info-value">${data.listing_data.city_name || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">State</span>
                        <span class="info-value">${data.listing_data.state || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Country</span>
                        <span class="info-value">${data.listing_data.country || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Coordinates</span>
                        <span class="info-value">${data.listing_data.latitude || 'N/A'}, ${data.listing_data.longitude || 'N/A'}</span>
                    </div>
                </div>
            `;
            
            // Pricing
            contentHTML += `
                <div class="info-section">
                    <h3>Pricing</h3>
                    <div class="info-item">
                        <span class="info-label">Min Price</span>
                        <span class="info-value">$${data.listing_data.min || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Base Price</span>
                        <span class="info-value">$${data.listing_data.base || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Max Price</span>
                        <span class="info-value">$${data.listing_data.max || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Recommended Base</span>
                        <span class="info-value">$${data.listing_data.recommended_base_price || 'N/A'}</span>
                    </div>
                </div>
            `;
            
            // Performance Metrics
            contentHTML += `
                <div class="info-section">
                    <h3>Occupancy Metrics</h3>
                    <div class="stat-grid">
                        <div class="stat-item">
                            <div class="stat-value">${data.listing_data.occupancy_next_7 || 'N/A'}</div>
                            <div class="stat-label">Next 7 Days</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${data.listing_data.occupancy_next_30 || 'N/A'}</div>
                            <div class="stat-label">Next 30 Days</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${data.listing_data.occupancy_next_60 || 'N/A'}</div>
                            <div class="stat-label">Next 60 Days</div>
                        </div>
                        <div class="stat-item">
                            <div class="stat-value">${data.listing_data.occupancy_past_90 || 'N/A'}</div>
                            <div class="stat-label">Past 90 Days</div>
                        </div>
                    </div>
                </div>
            `;
            
            // Market Comparison
            contentHTML += `
                <div class="info-section">
                    <h3>Market Comparison</h3>
                    <div class="info-item">
                        <span class="info-label">Market Occ. Next 7</span>
                        <span class="info-value">${data.listing_data.market_occupancy_next_7 || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Market Occ. Next 30</span>
                        <span class="info-value">${data.listing_data.market_occupancy_next_30 || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">MPI Next 30</span>
                        <span class="info-value">${data.listing_data.mpi_next_30 || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">MPI Next 60</span>
                        <span class="info-value">${data.listing_data.mpi_next_60 || 'N/A'}</span>
                    </div>
                </div>
            `;
            
            // Revenue
            contentHTML += `
                <div class="info-section">
                    <h3>Revenue</h3>
                    <div class="info-item">
                        <span class="info-label">Past 30 Days</span>
                        <span class="info-value">$${data.listing_data.revenue_past_30 || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Next 30 Days</span>
                        <span class="info-value">$${data.listing_data.revenue_next_30 || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Next 180 Days</span>
                        <span class="info-value">$${data.listing_data.revenue_next_180 || 'N/A'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">ADR Past 90</span>
                        <span class="info-value">$${data.listing_data.adr_past_90 || 'N/A'}</span>
                    </div>
                </div>
            `;
            
            // Metadata
            contentHTML += `
                <div class="info-section">
                    <h3>Metadata</h3>
                    <div class="info-item">
                        <span class="info-label">Group</span>
                        <span class="info-value">${data.listing_data.group || 'None'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Tags</span>
                        <span class="info-value">${data.listing_data.tags || 'None'}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Last Booked</span>
                        <span class="info-value">${formatDate(data.listing_data.last_booked_date)}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Last Pushed</span>
                        <span class="info-value">${formatDate(data.listing_data.last_date_pushed)}</span>
                    </div>
                    <div class="info-item">
                        <span class="info-label">Last Refreshed</span>
                        <span class="info-value">${formatDate(data.listing_data.last_refreshed_at)}</span>
                    </div>
                </div>
            `;
            
            document.getElementById('sidebar-content').innerHTML = contentHTML;
        }
        
        function formatDate(dateString) {
            if (!dateString) return 'N/A';
            try {
                const date = new Date(dateString);
                return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
            } catch {
                return dateString;
            }
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    """Main page with optional listing_id parameter"""
    listing_id = request.args.get('listing_id', '')
    return render_template_string(HTML_TEMPLATE, listing_id=listing_id)

@app.route('/listingv5.html')
def listingv5():
    """Serve the v5 listing viewer HTML file"""
    return send_from_directory('.', 'listingv5.html')

@app.route('/booking_window_viewer.html')
def booking_window_viewer():
    """Serve the booking window visualization HTML file"""
    return send_from_directory('.', 'booking_window_viewer.html')

@app.route('/test_tooltip.html')
def test_tooltip():
    """Serve the tooltip test HTML file"""
    return send_from_directory('.', 'test_tooltip.html')

@app.route('/api/listing/<listing_id>')
def get_listing_data(listing_id):
    """API endpoint to fetch listing data using portfolio mapping"""
    try:
        # Get portfolio info for the listing
        portfolio_info = portfolio_manager.get_listing_portfolio(listing_id)
        
        if not portfolio_info:
            # Refresh and try again
            portfolio_manager.refresh_all_listings()
            portfolio_info = portfolio_manager.get_listing_portfolio(listing_id)
            
            if not portfolio_info:
                return jsonify({'error': f'Listing {listing_id} not found in any portfolio'}), 404
        
        # Get the correct API client (automatically uses correct API key)
        api_client = portfolio_manager.get_api_client_for_listing(listing_id)
        
        # Fetch listing data using the correct API key
        listing_data = api_client.get_listing(listing_id)
        
        # Handle response format (could be single listing or array)
        if isinstance(listing_data, dict) and 'listings' in listing_data:
            # Response contains array of listings
            if listing_data['listings']:
                listing_info = listing_data['listings'][0]
            else:
                return jsonify({'error': 'No listing data returned'}), 404
        elif isinstance(listing_data, dict):
            # Direct listing object
            listing_info = listing_data
        else:
            return jsonify({'error': 'Unexpected response format'}), 500
        
        # Return combined data
        return jsonify({
            'listing_id': listing_id,
            'portfolio_name': portfolio_info['portfolio_name'],
            'portfolio_key': portfolio_info['portfolio_key'],
            'listing_name': portfolio_info['listing_name'],
            'listing_data': listing_info
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh')
def refresh_portfolios():
    """Refresh portfolio mapping"""
    try:
        portfolio_manager.refresh_all_listings()
        return jsonify({'success': True, 'message': 'Portfolio data refreshed'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/listing_prices/<listing_id>')
def get_listing_prices(listing_id):
    """API endpoint to fetch listing price data"""
    try:
        # Get portfolio info for the listing
        portfolio_info = portfolio_manager.get_listing_portfolio(listing_id)
        
        if not portfolio_info:
            # Refresh and try again
            portfolio_manager.refresh_all_listings()
            portfolio_info = portfolio_manager.get_listing_portfolio(listing_id)
            
            if not portfolio_info:
                return jsonify({'error': f'Listing {listing_id} not found in any portfolio'}), 404
        
        # Get the correct API client
        api_client = portfolio_manager.get_api_client_for_listing(listing_id)
        
        # Get PMS from listing data
        listing_data = api_client.get_listing(listing_id)
        pms = 'airbnb'  # Default PMS
        if isinstance(listing_data, dict):
            if 'listings' in listing_data and listing_data['listings']:
                pms = listing_data['listings'][0].get('pms', 'airbnb')
            elif 'pms' in listing_data:
                pms = listing_data.get('pms', 'airbnb')
        
        # Prepare request for pricing API
        listings_request = [{'id': listing_id, 'pms': pms}]
        
        # Fetch pricing data
        pricing_data = api_client.get_listing_prices(listings_request)
        
        return jsonify(pricing_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/neighborhood/<listing_id>')
def get_neighborhood_data(listing_id):
    """API endpoint to fetch neighborhood market data"""
    try:
        # Get portfolio info for the listing
        portfolio_info = portfolio_manager.get_listing_portfolio(listing_id)
        
        if not portfolio_info:
            # Refresh and try again
            portfolio_manager.refresh_all_listings()
            portfolio_info = portfolio_manager.get_listing_portfolio(listing_id)
            
            if not portfolio_info:
                return jsonify({'error': f'Listing {listing_id} not found in any portfolio'}), 404
        
        # Get the correct API client
        api_client = portfolio_manager.get_api_client_for_listing(listing_id)
        
        # Get PMS from listing data
        listing_data = api_client.get_listing(listing_id)
        pms = 'airbnb'  # Default PMS
        if isinstance(listing_data, dict):
            if 'listings' in listing_data and listing_data['listings']:
                pms = listing_data['listings'][0].get('pms', 'airbnb')
            elif 'pms' in listing_data:
                pms = listing_data.get('pms', 'airbnb')
        
        # Fetch neighborhood data with PMS parameter
        neighborhood_data = api_client.get_neighborhood_data(listing_id, pms)
        
        return jsonify(neighborhood_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/reservation_data/<listing_id>')
def get_reservation_data(listing_id):
    """
    API endpoint to fetch reservation/booking data for a listing

    Note: The reservation_data endpoint is not available for all API keys,
    so we use a workaround by extracting booking data from the listing itself,
    similar to what appscript.js does.

    Query Parameters:
        start_date: Start date (YYYY-MM-DD format) - currently ignored
        end_date: End date (YYYY-MM-DD format) - currently ignored

    Returns:
        JSON with reservation data formatted to match PriceLabs API structure
    """
    try:
        # Get portfolio info for the listing
        portfolio_info = portfolio_manager.get_listing_portfolio(listing_id)

        if not portfolio_info:
            # Refresh and try again
            portfolio_manager.refresh_all_listings()
            portfolio_info = portfolio_manager.get_listing_portfolio(listing_id)

            if not portfolio_info:
                return jsonify({'error': f'Listing {listing_id} not found in any portfolio'}), 404

        # Get the correct API client for this listing
        api_client = portfolio_manager.get_api_client_for_listing(listing_id)

        # First, try the actual reservation_data endpoint
        start_date = request.args.get('start_date', '2025-10-24')  # Start from market data range
        end_date = request.args.get('end_date', '2026-12-31')

        # Get the PMS from the portfolio
        listing_info = portfolio_manager.listing_cache.get(listing_id)
        pms_name = listing_info.get('pms') if listing_info else None

        reservation_data = api_client.get_reservation_data(
            pms=pms_name,
            start_date=start_date,
            end_date=end_date,
            limit=100,
            offset=0
        )

        # If the API endpoint works, filter and return the data
        if 'data' in reservation_data and not ('error' in reservation_data):
            # Filter reservations to only include this listing
            filtered_data = [
                booking for booking in reservation_data['data']
                if str(booking.get('listing_id')) == str(listing_id)
            ]

            return jsonify({
                'data': filtered_data,
                'pms_name': reservation_data.get('pms_name'),
                'next_page': reservation_data.get('next_page', False)
            })

        # Fallback: Extract booking data from listing (like appscript.js does)
        # This is needed because the reservation_data endpoint requires special access
        listing_data = api_client.get_listing(listing_id)

        # Handle response format
        if isinstance(listing_data, dict):
            if 'listings' in listing_data and listing_data['listings']:
                listing = listing_data['listings'][0]
            else:
                listing = listing_data
        else:
            return jsonify({'error': 'Unexpected listing data format'}), 500

        # Format reservation data from listing fields
        formatted_reservations = []

        # Create a reservation entry if we have last_booked_date
        if listing.get('last_booked_date'):
            formatted_reservations.append({
                'listing_id': listing_id,
                'check_in': listing.get('last_booked_date'),
                'check_out': None,  # Not available in listing data
                'no_of_days': 1,    # Estimate
                'rental_revenue': listing.get('revenue_past_30', 0) / 30 if listing.get('revenue_past_30') else 0,
                'booking_status': 'booked',
                'reservation_id': f"estimated_{listing_id}",
                'pms': listing.get('pms', 'airbnb')
            })

        # Return in PriceLabs API format
        return jsonify({
            'pms_name': listing.get('pms', 'airbnb'),
            'next_page': False,
            'data': formatted_reservations,
            'note': 'Data extracted from listing fields (reservation endpoint not available)'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting PriceLabs Listing Viewer...")
    print("Open http://localhost:5050 in your browser")
    print("Or use http://localhost:5050?listing_id=YOUR_LISTING_ID")
    print("\nPress Ctrl+C to stop the server")
    
    app.run(debug=True, port=5050)