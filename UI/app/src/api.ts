    import axios from 'axios';

    // Base URL for the API
    const API_URL = '/api';

    // Interface for Symptom data
    export interface Symptom {
      id: number;
      name: string;
      child: boolean;
      adult: boolean;
      products: Product[];
      comments: Record<string, string> | null;
    }

    // Interface for Product data
    export interface Product {
      id: number;
      name: string;
    }

    // Function to fetch symptoms
    export const fetchSymptoms = async (): Promise<Symptom[]> => {
      try {
        const response = await axios.get(`${API_URL}/api/health/symptoms/`);
        return response.data;
      } catch (error) {
        console.error('Error fetching symptoms:', error);
        throw error;
      }
    };

    // ... existing code for other API functions ...
