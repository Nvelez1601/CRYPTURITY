import axios from 'axios';

const resolveBaseUrl = (): string => {
  const configured = import.meta.env.VITE_API_BASE_URL;
  if (configured && configured.length > 0) {
    return configured.replace(/[\/]+$/, '');
  }

  if (import.meta.env.DEV) {
    return 'http://localhost:8000';
  }

  if (typeof window !== 'undefined' && window.location) {
    return window.location.origin.replace(/[\/]+$/, '');
  }

  return 'http://localhost:8000';
};

const baseURL = resolveBaseUrl();

export const apiClient = axios.create({
  baseURL,
  timeout: 8000,
  headers: {
    'Content-Type': 'application/json'
  }
});
