import axios from 'axios';

// Base URL for the API - remove trailing slash if it exists
const API_URL = '/api';

// Authentication token from the Django backend
const API_TOKEN = '11d3acee94a184b88afa091ed3df7ef71850bffd';

// Create a custom axios instance with authentication headers
const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    'Authorization': `Token ${API_TOKEN}`
  }
});

// Interface for Reservation data
export interface Reservation {
  id: number;
  asset_id: number;
  asset_name: string;
  platform_id: number;
  platform_name: string;
  reservation_number: string;
  entry_date: string;
  end_date: string;
  number_of_nights: number;
  renting_person_full_name: string;
  price: string;
  created_at: string;
}

// Interface for Symptom data
export interface Symptom {
  id: number;
  name: string;
  child: boolean;
  adult: boolean;
  products: number[]; // Array of product IDs
  comments: Record<string, string> | null;
}

// Interface for paginated API response
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

// Interface for Product data
export interface Product {
  id: number;
  name: string;
}

// Function to fetch reservations
export const fetchReservations = async (month: number = 2, year: number = 2025): Promise<Reservation[]> => {
  try {
    const response = await apiClient.get(`/real_estate/reservations/`, {
      params: { month, year }
    });
    return response.data;
  } catch (error) {
    console.error('Error fetching reservations:', error);
    throw error;
  }
};

// Function to fetch symptoms
export const fetchSymptoms = async (): Promise<PaginatedResponse<Symptom>> => {
  try {
    const response = await apiClient.get(`/health/symptoms/`);
    return response.data;
  } catch (error) {
    console.error('Error fetching symptoms:', error);
    throw error;
  }
};

// Function to get an authentication token (for use in a real app)
export const getAuthToken = async (username: string, password: string): Promise<string> => {
  try {
    const response = await axios.post(`${API_URL}/api-token-auth/`, {
      username,
      password
    });
    return response.data.token;
  } catch (error) {
    console.error('Error getting auth token:', error);
    throw error;
  }
};
