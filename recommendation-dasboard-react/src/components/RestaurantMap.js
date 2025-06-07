import React, { useState, useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import { TextField, Button, Box, Paper, Typography, Select, MenuItem, FormControl, InputLabel, Container, Grid } from '@mui/material';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icons in Leaflet with React
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

// City boundaries
const CITY_BOUNDS = {
  'ISTANBUL': {
    north: 41.2,
    south: 40.9,
    east: 29.2,
    west: 28.6,
    center: [41.0082, 28.9784]
  },
  'ANKARA': {
    north: 40.0,
    south: 39.8,
    east: 33.0,
    west: 32.6,
    center: [39.9334, 32.8597]
  },
  'ELAZIĞ': {
    north: 38.7,
    south: 38.6,
    east: 39.3,
    west: 39.2,
    center: [38.6810, 39.2264]
  }
};

// Function to generate distributed coordinates within a city
const generateDistributedCoordinates = (index, total, city) => {
  const bounds = CITY_BOUNDS[city];
  if (!bounds) return [0, 0]; // Fallback if city not found

  // Use city center as the base point
  const [centerLat, centerLon] = bounds.center;
  
  // Generate random angle (0 to 2π)
  const angle = Math.random() * 2 * Math.PI;
  
  // Generate random distance from center (0 to maxRadius)
  // Using square root to ensure uniform distribution in the circle
  const maxRadius = 0.02; // Approximately 2km
  const distance = Math.sqrt(Math.random()) * maxRadius;
  
  // Convert polar coordinates to cartesian
  // Note: 1 degree of latitude is approximately 111km
  // 1 degree of longitude varies with latitude, but we'll use a rough approximation
  const latOffset = distance * Math.cos(angle);
  const lonOffset = distance * Math.sin(angle);
  
  // Calculate final coordinates
  const lat = centerLat + latOffset;
  const lon = centerLon + lonOffset;
  
  return [lat, lon];
};

// Update the ChangeMapView component to maintain fixed zoom
const ChangeMapView = ({ center }) => {
  const map = useMap();
  useEffect(() => {
    map.setView(center, 9); // Force zoom level to 9
  }, [center, map]);
  return null;
};

const RestaurantMap = () => {
  const [searchText, setSearchText] = useState('');
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [mapCenter, setMapCenter] = useState(CITY_BOUNDS['ISTANBUL'].center);
  const [restaurantCoordinates, setRestaurantCoordinates] = useState({});
  const [selectedCity, setSelectedCity] = useState('ISTANBUL');
  const mapRef = useRef(null);

  const handleCityChange = (event) => {
    const city = event.target.value;
    console.log('Selected city:', city);
    console.log('City bounds:', CITY_BOUNDS[city]);
    setSelectedCity(city);
    if (CITY_BOUNDS[city]) {
      const newCenter = CITY_BOUNDS[city].center;
      console.log('Setting new center:', newCenter);
      setMapCenter(newCenter);
    }
  };

  const handleSearch = async () => {
    if (!searchText.trim()) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await axios.get(`http://localhost:8001/search/search_text`, {
        params: {
          page: 0,
          page_size: 50,
          search_text: searchText
        }
      });
      const newRestaurants = response.data.results;
      setRestaurants(newRestaurants);
      
      // Generate coordinates only when new restaurants are fetched
      const newCoordinates = {};
      newRestaurants.forEach((restaurant, index) => {
        const city = restaurant.restaurant_city;
        if (!newCoordinates[city]) {
          newCoordinates[city] = [];
        }
        newCoordinates[city].push(
          generateDistributedCoordinates(index, newRestaurants.length, city)
        );
      });
      setRestaurantCoordinates(newCoordinates);
      
      // Update map center based on the first restaurant's city
      if (newRestaurants.length > 0) {
        const firstCity = newRestaurants[0].restaurant_city;
        if (CITY_BOUNDS[firstCity]) {
          setSelectedCity(firstCity);
          setMapCenter(CITY_BOUNDS[firstCity].center);
        }
      }
    } catch (err) {
      setError('Failed to fetch restaurant data. Please try again.');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSearch();
    }
  };

  // Group restaurants by city
  const restaurantsByCity = restaurants.reduce((acc, restaurant) => {
    const city = restaurant.restaurant_city;
    if (!acc[city]) {
      acc[city] = [];
    }
    acc[city].push(restaurant);
    return acc;
  }, {});

  return (
    <Box sx={{ 
      height: '100vh', 
      width: '100%', 
      display: 'flex', 
      flexDirection: 'column',
      backgroundColor: '#F5F7FA'
    }}>
      {/* Search Section */}
      <Box sx={{ 
        p: 2, 
        backgroundColor: '#F5F7FA', 
        zIndex: 1000,
        borderBottom: '1px solid rgba(0,0,0,0.1)'
      }}>
        <Container maxWidth="md">
          <Paper 
            elevation={3} 
            sx={{ 
              p: 3,
              backgroundColor: 'white',
              borderRadius: 2,
              mb: 2,
              boxShadow: '0 2px 4px rgba(0,0,0,0.05)'
            }}
          >
            <Typography 
              variant="h5" 
              gutterBottom 
              align="center" 
              sx={{ 
                mb: 3,
                color: '#1A1A1A',
                fontWeight: 600
              }}
            >
              Restaurant Search
            </Typography>
            
            <Grid container spacing={2}>
              <Grid item xs={12} md={5}>
                <FormControl fullWidth>
                  <InputLabel id="city-select-label" sx={{ color: '#6E7582' }}>City</InputLabel>
                  <Select
                    labelId="city-select-label"
                    id="city-select"
                    value={selectedCity}
                    label="City"
                    onChange={handleCityChange}
                    sx={{
                      '& .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#2F80ED',
                      },
                      '&:hover .MuiOutlinedInput-notchedOutline': {
                        borderColor: '#56CCF2',
                      },
                    }}
                  >
                    {Object.keys(CITY_BOUNDS).map((city) => (
                      <MenuItem key={city} value={city}>
                        {city}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={7}>
                <TextField
                  fullWidth
                  variant="outlined"
                  placeholder="Search restaurants..."
                  value={searchText}
                  onChange={(e) => setSearchText(e.target.value)}
                  onKeyPress={handleKeyPress}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      '& fieldset': {
                        borderColor: '#2F80ED',
                      },
                      '&:hover fieldset': {
                        borderColor: '#56CCF2',
                      },
                    },
                  }}
                />
              </Grid>
            </Grid>

            <Box sx={{ mt: 2, display: 'flex', justifyContent: 'center' }}>
              <Button 
                variant="contained" 
                onClick={handleSearch}
                disabled={loading}
                sx={{ 
                  minWidth: '200px',
                  backgroundColor: '#2F80ED',
                  '&:hover': {
                    backgroundColor: '#56CCF2',
                  },
                  color: 'white',
                  fontWeight: 600,
                  textTransform: 'none',
                  boxShadow: '0 2px 4px rgba(47, 128, 237, 0.2)'
                }}
              >
                {loading ? 'Searching...' : 'Search'}
              </Button>
            </Box>
            
            {error && (
              <Typography color="error" sx={{ mt: 2, textAlign: 'center', color: '#6E7582' }}>
                {error}
              </Typography>
            )}
          </Paper>
        </Container>
      </Box>

      {/* Map Section */}
      <Box sx={{ 
        flex: 1, 
        position: 'relative', 
        width: '100%',
        height: '100%',
        display: 'flex', 
        backgroundColor: '#F5F7FA'
      }}>
        <MapContainer
          ref={mapRef}
          center={mapCenter}
          zoom={9}
          minZoom={9}
          maxZoom={9}
          style={{ 
            height: '100%', 
            width: '100%',
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            borderRadius: '8px',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)'
          }}
        >
          <ChangeMapView center={mapCenter} />
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {Object.entries(restaurantsByCity).map(([city, cityRestaurants]) => 
            cityRestaurants.map((restaurant, index) => {
              const coordinates = restaurantCoordinates[city]?.[index] || [0, 0];
              return (
                <Marker
                  key={restaurant.restaurant_id}
                  position={coordinates}
                >
                  <Popup>
                    <Box sx={{ maxWidth: '300px' }}>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom sx={{ color: '#1A1A1A' }}>
                        {restaurant.restaurant_name}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 1, color: '#6E7582' }}>
                        Rating: {restaurant.restaurant_rate} ⭐
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 1, color: '#6E7582' }}>
                        Reviews: {restaurant.review_number}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 1, color: '#6E7582' }}>
                        City: {restaurant.restaurant_city}
                      </Typography>
                      <Typography variant="body2" sx={{ mb: 2, color: '#6E7582' }}>
                        Location: {restaurant.lat}, {restaurant.lon}
                      </Typography>
                      
                      {/* Products Section */}
                      {(restaurant.product_names?.length > 0 || restaurant.product_description?.length > 0) && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="subtitle2" fontWeight="bold" gutterBottom sx={{ color: '#1A1A1A' }}>
                            Products
                          </Typography>
                          <Box sx={{ maxHeight: '150px', overflowY: 'auto' }}>
                            {Array.from({ length: Math.max(
                              restaurant.product_names?.length || 0,
                              restaurant.product_description?.length || 0
                            )}).map((_, index) => (
                              <Box key={index} sx={{ 
                                mb: 1, 
                                p: 1, 
                                bgcolor: '#F5F7FA', 
                                borderRadius: 1 
                              }}>
                                {restaurant.product_names?.[index] && (
                                  <Typography variant="body2" fontWeight="medium" sx={{ color: '#1A1A1A' }}>
                                    {restaurant.product_names[index]}
                                  </Typography>
                                )}
                                {restaurant.product_description?.[index] && (
                                  <Typography variant="body2" sx={{ color: '#6E7582' }}>
                                    {restaurant.product_description[index]}
                                  </Typography>
                                )}
                              </Box>
                            ))}
                          </Box>
                        </Box>
                      )}

                      {/* Comments Section */}
                      {restaurant.comments?.length > 0 && (
                        <Box sx={{ mt: 2 }}>
                          <Typography variant="subtitle2" fontWeight="bold" gutterBottom sx={{ color: '#1A1A1A' }}>
                            Comments
                          </Typography>
                          <Box sx={{ maxHeight: '150px', overflowY: 'auto' }}>
                            {restaurant.comments.map((comment, index) => (
                              <Typography 
                                key={index} 
                                variant="body2" 
                                sx={{ 
                                  mb: 1, 
                                  p: 1, 
                                  bgcolor: '#F5F7FA', 
                                  borderRadius: 1,
                                  color: '#6E7582'
                                }}
                              >
                                {comment}
                              </Typography>
                            ))}
                          </Box>
                        </Box>
                      )}
                    </Box>
                  </Popup>
                </Marker>
              );
            })
          )}
        </MapContainer>
      </Box>
    </Box>
  );
};

export default RestaurantMap; 