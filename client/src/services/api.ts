import axios from 'axios';
import { Ad, AdStats, AdFilters } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const adsApi = {
  getAllAds: async (filters?: AdFilters): Promise<Ad[]> => {
    const params = new URLSearchParams();
    
    if (filters?.status) params.append('status', filters.status);
    if (filters?.platform) params.append('platform', filters.platform);
    if (filters?.startDate) params.append('startDate', filters.startDate);
    if (filters?.endDate) params.append('endDate', filters.endDate);
    if (filters?.multipleVersions !== undefined) {
      params.append('multipleVersions', filters.multipleVersions.toString());
    }

    const response = await api.get(`/ads?${params.toString()}`);
    return response.data.ads;
  },

  getAdById: async (adId: string): Promise<Ad> => {
    const response = await api.get(`/ads/${adId}`);
    return response.data.ad;
  },

  getStats: async (): Promise<AdStats> => {
    const response = await api.get('/ads/stats/summary');
    return response.data;
  },

  getAssetUrl: (assetPath: string | null): string | null => {
    if (!assetPath) return null;
    // Extract type and filename from path like "assets/images/123.jpg"
    const match = assetPath.match(/assets\/(images|videos)\/(.+)$/);
    if (match) {
      const [, type, filename] = match;
      return `${API_BASE_URL}/ads/assets/${type}/${filename}`;
    }
    return null;
  },
};

export default api;

