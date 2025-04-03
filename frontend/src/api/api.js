import axios from "axios";

// Base API URL from environment variables
const API_BASE_URL = "http://127.0.0.1:8000/api";

// Create Axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// Login API
export const loginUser = async (credentials) => {
  try {
    const response = await api.post("/token/", credentials);
    return response.data; // Contains access and refresh tokens
  } catch (error) {
    throw error.response ? error.response.data : error.message;
  }
};

// Register API
export const registerUser = async (userData) => {
  try {
    const response = await api.post("/register/", userData);
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : error.message;
  }
};

// Fetch Flipbooks (Only for authenticated users)
export const getFlipbooks = async (token) => {
  try {
    const response = await api.get("/flipbooks/", {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  } catch (error) {
    throw error.response ? error.response.data : error.message;
  }
};

// Refresh token logic
const refreshAccessToken = async () => {
  try {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) return null;

    const response = await axios.post(`${API_BASE_URL}/token/refresh/`, { refresh: refreshToken });
    localStorage.setItem("access_token", response.data.access);
    return response.data.access;
  } catch {
    return null;
  }
};

// Automatically refresh expired tokens
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response.status === 401) {
      const newToken = await refreshAccessToken();
      if (newToken) {
        error.config.headers.Authorization = `Bearer ${newToken}`;
        return api.request(error.config);
      }
    }
    return Promise.reject(error);
  }
);

