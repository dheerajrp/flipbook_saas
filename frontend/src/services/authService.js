import axios from "axios";

// Base API URL (change this if needed)
const API_URL = "http://127.0.0.1:8000/api/";

// Register User
export const register = async (username, password) => {
    return await axios.post(`${API_URL}register/`, { username, password });
};

// Login User
export const login = async (username, password) => {
    const response = await axios.post(`${API_URL}token/`, { username, password });
    if (response.data.access) {
        localStorage.setItem("access_token", response.data.access);
        localStorage.setItem("refresh_token", response.data.refresh);
    }
    return response.data;
};

// Refresh Token
export const refreshToken = async () => {
    const refresh_token = localStorage.getItem("refresh_token");
    if (refresh_token) {
        const response = await axios.post(`${API_URL}token/refresh/`, { refresh: refresh_token });
        localStorage.setItem("access_token", response.data.access);
        return response.data.access;
    }
    return null;
};

// Get Auth Header
export const authHeader = () => {
    const token = localStorage.getItem("access_token");
    return token ? { Authorization: `Bearer ${token}` } : {};
};

// Logout User
export const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
};
