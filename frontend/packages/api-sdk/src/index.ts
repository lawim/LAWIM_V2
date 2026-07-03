export interface ApiResponse<T> {
  data: T;
  message?: string;
}

export interface PropertySummary {
  id: string;
  title: string;
  location: string;
  price: number;
  type: string;
}

export interface MarketListing {
  id: string;
  title: string;
  category: string;
  price: number;
  status: string;
}

export interface UserProfile {
  id: string;
  name: string;
  role: string;
  email: string;
}

const mockDelay = () => Promise.resolve();

export const apiSdk = {
  async getProperties(): Promise<ApiResponse<PropertySummary[]>> {
    await mockDelay();
    return {
      data: [
        { id: 'p1', title: 'Maison Bellevue', location: 'Lyon', price: 420000, type: 'House' },
        { id: 'p2', title: 'Appartement Lumière', location: 'Paris', price: 610000, type: 'Apartment' }
      ]
    };
  },

  async getMarketListings(): Promise<ApiResponse<MarketListing[]>> {
    await mockDelay();
    return {
      data: [
        { id: 'm1', title: 'Audit immobilier', category: 'Services', price: 1800, status: 'Open' },
        { id: 'm2', title: 'Campagne de prospection', category: 'Marketing', price: 3200, status: 'In review' }
      ]
    };
  },

  async getProfile(): Promise<ApiResponse<UserProfile>> {
    await mockDelay();
    return {
      data: {
        id: 'u1',
        name: 'Alicia Dubois',
        role: 'Director',
        email: 'alicia@lawim.example'
      }
    };
  }
};

export type ApiSdk = typeof apiSdk;
