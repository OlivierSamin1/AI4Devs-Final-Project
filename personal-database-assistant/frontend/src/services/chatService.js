import axios from 'axios';

// Create an axios instance with base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  }
});

/**
 * Send a message to the chat API
 * @param {string} message - The message to send
 * @returns {Promise} - The response from the API
 */
export const sendMessage = async (message) => {
  return api.post('/chat', { message });
};

/**
 * Check the health of the API
 * @returns {Promise} - The response from the API
 */
export const checkHealth = async () => {
  return api.get('/health');
}; 