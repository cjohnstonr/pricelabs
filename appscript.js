// Updated Google Apps Script with Auto API Key Detection
// Replace your existing appscriptwebapp.js with this version

// Configuration - Your three API keys
const API_KEYS = {
    utah: 'iJO6RszXvTHxNVfeVLbot1oYhUyPye8bZbyp5apV',
    california: 'PGNkidBKeuOW2G6DQL91VRdPM2wTaid5w64EzrVE', 
    default: 'i7wVYNZwf26GNqjtxwrEW3yDppK0h3nECXMRXFMS',
    special: 'enCAf5AYjn2lzIgQuiBi4L489DcIoCA0j5wCou6J' 
  };
  
  // Cache for listing ID to API key mapping (improves performance)
  const LISTING_CACHE = {};
  
  /**
   * Auto-detect which API key owns a specific listing ID
   */
  function getApiKeyForListing(listingId) {
    // Check cache first
    if (LISTING_CACHE[listingId]) {
      console.log(`Cache hit for listing ${listingId}: ${LISTING_CACHE[listingId]}`);
      return LISTING_CACHE[listingId];
    }
    
    console.log(`Looking up API key for listing: ${listingId}`);
    
    // Try each API key
    for (const [accountName, apiKey] of Object.entries(API_KEYS)) {
      try {
        console.log(`Trying ${accountName} account...`);
        
        // Try direct listing fetch first (faster)
        const directResult = fetchListing(listingId, apiKey, false); // Don't throw on 404
        if (directResult && !directResult.error) {
          console.log(`Found listing ${listingId} in ${accountName} account via direct fetch`);
          LISTING_CACHE[listingId] = apiKey;
          return apiKey;
        }
        
        // If direct fetch fails, check listings array
        const allListings = fetchAllListings(false, false, apiKey);
        if (allListings && allListings.listings) {
          const found = allListings.listings.some(listing => listing.id === listingId);
          if (found) {
            console.log(`Found listing ${listingId} in ${accountName} account via listings array`);
            LISTING_CACHE[listingId] = apiKey;
            return apiKey;
          }
        }
      } catch (error) {
        console.log(`Error checking ${accountName} account: ${error.toString()}`);
        continue;
      }
    }
    
    throw new Error(`Listing ${listingId} not found in any account (Utah, California, Default)`);
  }
  
  /**
   * Get all listings from all accounts with portfolio labels
   */
  function fetchAllListingsFromAllAccounts() {
    const combinedListings = [];
    const portfolios = {
      'utah': 'Utah Portfolio',
      'california': 'California Portfolio', 
      'default': 'Main Portfolio',
      'special': 'Special Account' 
    };
    
    for (const [accountName, apiKey] of Object.entries(API_KEYS)) {
      try {
        console.log(`Fetching listings from ${accountName} account...`);
        const result = fetchAllListings(false, false, apiKey);
        
        if (result && result.listings) {
          // Filter out inactive listings (push_enabled: false) and add portfolio information
          const labeledListings = result.listings
            .filter(listing => listing.push_enabled === true) // Only include active listings
            .map(listing => ({
              ...listing,
              portfolio: portfolios[accountName],
              portfolioKey: accountName,
              apiKey: apiKey // Store for frontend reference
            }));
          
          combinedListings.push(...labeledListings);
          console.log(`Added ${labeledListings.length} listings from ${accountName}`);
        }
      } catch (error) {
        console.error(`Failed to fetch from ${accountName}: ${error.toString()}`);
      }
    }
    
    console.log(`Total combined listings: ${combinedListings.length}`);
    return { listings: combinedListings };
  }
  
  /**
   * Enhanced fetchListing that handles 404s gracefully
   */
  function fetchListing(listingId, apiKey, throwOnError = true) {
    const url = `https://api.pricelabs.co/v1/listing/${listingId}`;
    
    try {
      const response = UrlFetchApp.fetch(url, {
        headers: {
          'X-API-Key': apiKey,
          'Accept': 'application/json'
        },
        muteHttpExceptions: true
      });
      
      const responseCode = response.getResponseCode();
      const responseText = response.getContentText();
      
      if (responseCode === 200) {
        return JSON.parse(responseText);
      } else if (responseCode === 404) {
        if (throwOnError) {
          // Try fallback to listings array
          console.log(`Individual endpoint returned 404 for listing ${listingId}, trying bulk endpoint...`);
          const bulkResult = fetchAllListings(false, false, apiKey);
          if (bulkResult && bulkResult.listings) {
            const listing = bulkResult.listings.find(l => l.id === listingId);
            if (listing) {
              return listing;
            }
          }
          throw new Error(`Listing ${listingId} not found`);
        } else {
          return { error: 'Not found', responseCode: 404 };
        }
      } else {
        const error = `API Error (${responseCode}): ${responseText.substring(0, 200)}`;
        if (throwOnError) {
          throw new Error(error);
        } else {
          return { error: error, responseCode: responseCode };
        }
      }
    } catch (error) {
      if (throwOnError) {
        throw error;
      } else {
        return { error: error.toString() };
      }
    }
  }
  
  /**
   * Keep existing fetchAllListings function
   */
  function fetchAllListings(skipHidden = true, onlySyncing = true, apiKey) {
    let url = 'https://api.pricelabs.co/v1/listings';
    const params = [];
    
    if (skipHidden) params.push('skip_hidden=true');
    if (onlySyncing) params.push('only_syncing=true');
    
    if (params.length > 0) {
      url += '?' + params.join('&');
    }
    
    const response = UrlFetchApp.fetch(url, {
      headers: {
        'X-API-Key': apiKey,
        'Accept': 'application/json'
      }
    });
    
    return JSON.parse(response.getContentText());
  }
  
  /**
   * Main entry point - Updated to handle auto-detection
   */
  function doGet(e) {
    try {
      const action = e.parameter.action;
      let result;
      
      switch(action) {
        case 'fetchListing':
          const listingId = e.parameter.listingId;
          if (!listingId) {
            throw new Error('listingId parameter is required');
          }
          
          // Auto-detect API key for this listing
          const apiKey = getApiKeyForListing(listingId);
          result = fetchListing(listingId, apiKey);
          break;
          
        case 'fetchAllListings':
          // Legacy support - use provided API key or default
          const legacyApiKey = e.parameter.apiKey || API_KEYS.default;
          const skipHidden = e.parameter.skipHidden === 'true';
          const onlySyncing = e.parameter.onlySyncing === 'true';
          result = fetchAllListings(skipHidden, onlySyncing, legacyApiKey);
          break;
          
        case 'fetchAllListingsFromAllAccounts':
          // New action - get listings from all accounts
          result = fetchAllListingsFromAllAccounts();
          break;
          
        case 'fetchPrices':
          const priceListingId = e.parameter.listingId;
          const priceApiKey = getApiKeyForListing(priceListingId);
          result = fetchPrices(priceListingId, priceApiKey);
          break;
          
        case 'fetchReservations':
          const resListingId = e.parameter.listingId; 
          const resApiKey = getApiKeyForListing(resListingId);
          const pms = e.parameter.pms || 'airbnb';
          result = fetchReservations(resListingId, pms, resApiKey);
          break;
          
        case 'fetchNeighborhood':
          const neighListingId = e.parameter.listingId;
          const neighApiKey = getApiKeyForListing(neighListingId);
          result = fetchNeighborhood(neighListingId, neighApiKey);
          break;
          
        default:
          throw new Error(`Invalid action: ${action}`);
      }
      
      return ContentService.createTextOutput(JSON.stringify(result))
        .setMimeType(ContentService.MimeType.JSON);
        
    } catch (error) {
      console.error('Error in doGet:', error.toString());
      const errorResponse = {
        error: true,
        message: error.toString(),
        timestamp: new Date().toISOString()
      };
      
      return ContentService.createTextOutput(JSON.stringify(errorResponse))
        .setMimeType(ContentService.MimeType.JSON);
    }
  }
  
  // Keep your existing helper functions (fetchPrices, fetchReservations, fetchNeighborhood)
  // They will automatically use the detected API key
  
  function fetchPrices(listingId, apiKey) {
    // Get listing data from bulk endpoint since /v1/prices/{id} returns 404
    const allListings = fetchAllListings(false, false, apiKey);
    const listing = allListings.listings.find(l => l.id === listingId);
    
    if (!listing) {
      throw new Error(`Listing ${listingId} not found`);
    }
    
    // Extract available pricing data and format for frontend
    return formatPricingData(listing);
  }
  
  function fetchReservations(listingId, pms, apiKey) {
    // Extract booking data from listing since reservations endpoint returns 404
    const allListings = fetchAllListings(false, false, apiKey);
    const listing = allListings.listings.find(l => l.id === listingId);
    
    if (!listing) {
      throw new Error(`Listing ${listingId} not found`);
    }
    
    return formatReservationData(listing);
  }
  
  function fetchNeighborhood(listingId, apiKey) {
    // Extract market data since neighborhood endpoint returns 404
    const allListings = fetchAllListings(false, false, apiKey);
    const listing = allListings.listings.find(l => l.id === listingId);
    
    if (!listing) {
      throw new Error(`Listing ${listingId} not found`);
    }
    
    return formatNeighborhoodData(listing);
  }
  
  /**
   * Data formatting functions to convert bulk listing data to expected API response format
   */
  function formatPricingData(listing) {
    // Format bulk listing data to match expected pricing response
    const currentDate = new Date().toISOString().split('T')[0];
    
    return [{
      date: currentDate,
      price: listing.base || 0,
      user_price: listing.base || 0,
      min_stay: 1,
      booking_status: "",
      demand_color: "#c0f1958c",
      demand_desc: "Market Rate"
    }];
  }
  
  function formatReservationData(listing) {
    // Format booking data from listing
    const reservationData = [];
    
    // If we have last booked date, create a reservation entry
    if (listing.last_booked_date) {
      reservationData.push({
        listing_id: listing.id,
        check_in: listing.last_booked_date,
        booking_status: "booked",
        rental_revenue: listing.revenue_past_30 || 0
      });
    }
    
    return {
      pms_name: listing.pms || "airbnb",
      next_page: false,
      data: reservationData
    };
  }
  
  function formatNeighborhoodData(listing) {
    // Format market data from listing
    return {
      market_data: {
        occupancy: listing.market_occupancy_next_7 || listing.market_occupancy_next_30 || "0%",
        adr: listing.adr_past_90 || 0,
        revenue: listing.revenue_past_30 || 0
      },
      listing_data: {
        occupancy: listing.occupancy_next_7 || listing.occupancy_next_30 || "0%",
        base_price: listing.base || 0,
        min_price: listing.min || 0,
        max_price: listing.max || 0
      }
    };
  }