   import axios from 'axios';

    // Base URL for the API
    const API_URL = '/api';

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

    // Function to fetch reservations
    export const fetchReservations = async (month: number = 2, year: number = 2025): Promise<Reservation[]> => {
      try {
        const response = await axios.get(`${API_URL}/api/reservations/`, {
          params: { month, year }
        });
        return response.data;
      } catch (error) {
        console.error('Error fetching reservations:', error);
        throw error;
      }
    };
