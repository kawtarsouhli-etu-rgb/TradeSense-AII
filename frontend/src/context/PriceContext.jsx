import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import { marketAPI } from '../services/api';
import { getMockPrice, simulateAPICall } from '../services/mockMarketService';

const PriceContext = createContext();

export const usePrice = () => {
  const context = useContext(PriceContext);
  if (!context) {
    throw new Error('usePrice must be used within PriceProvider');
  }
  return context;
};

export const PriceProvider = ({ children }) => {
  const [prices, setPrices] = useState({});
  const [isLoading, setIsLoading] = useState({});
  const [error, setError] = useState(null);
  const intervalRefs = useRef({});

  // Fetch single price
  const fetchPrice = async (symbol, market = 'US') => {
    setIsLoading(prev => ({ ...prev, [`${symbol}-${market}`]: true }));
    try {
      const response = await marketAPI.getPrice(symbol, market);
      const priceData = response.data.data;
      
      setPrices(prev => ({
        ...prev,
        [`${symbol}-${market}`]: {
          ...priceData,
          lastUpdated: new Date().toISOString()
        }
      }));
      
      setError(null);
    } catch (err) {
      console.warn(`API failed for ${symbol}, using mock data:`, err);
      // Use mock data as fallback
      try {
        await simulateAPICall(200); // Simulate network delay
        const mockPriceData = getMockPrice(symbol, market);
        
        setPrices(prev => ({
          ...prev,
          [`${symbol}-${market}`]: {
            ...mockPriceData,
            lastUpdated: new Date().toISOString()
          }
        }));
        
        setError(null);
      } catch (mockErr) {
        console.error(`Error with mock data for ${symbol}:`, mockErr);
        setError(mockErr.message);
      }
    } finally {
      setIsLoading(prev => ({ ...prev, [`${symbol}-${market}`]: false }));
    }
  };

  // Fetch multiple prices
  const fetchMultiplePrices = async (symbols) => {
    const promises = symbols.map(({ symbol, market }) => 
      marketAPI.getPrice(symbol, market)
    );
    
    try {
      const responses = await Promise.all(promises);
      const newPrices = {};
      
      responses.forEach((response, index) => {
        const { symbol, market } = symbols[index];
        const priceData = response.data.data;
        newPrices[`${symbol}-${market}`] = {
          ...priceData,
          lastUpdated: new Date().toISOString()
        };
      });
      
      setPrices(prev => ({ ...prev, ...newPrices }));
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching multiple prices:', err);
    }
  };

  // Start auto-refresh for a symbol
  const startAutoRefresh = (symbol, market = 'US', intervalMs = 15000) => {
    const key = `${symbol}-${market}`;
    
    // Clear existing interval if any
    if (intervalRefs.current[key]) {
      clearInterval(intervalRefs.current[key]);
    }
    
    // Fetch immediately
    fetchPrice(symbol, market);
    
    // Set up interval
    intervalRefs.current[key] = setInterval(() => {
      fetchPrice(symbol, market);
    }, intervalMs);
  };

  // Stop auto-refresh for a symbol
  const stopAutoRefresh = (symbol, market = 'US') => {
    const key = `${symbol}-${market}`;
    if (intervalRefs.current[key]) {
      clearInterval(intervalRefs.current[key]);
      delete intervalRefs.current[key];
    }
  };

  // Stop all intervals on unmount
  useEffect(() => {
    return () => {
      Object.values(intervalRefs.current).forEach(clearInterval);
    };
  }, []);

  const value = {
    prices,
    isLoading,
    error,
    fetchPrice,
    fetchMultiplePrices,
    startAutoRefresh,
    stopAutoRefresh
  };

  return (
    <PriceContext.Provider value={value}>
      {children}
    </PriceContext.Provider>
  );
};
