import { createContext, useState, useEffect } from "react";
import axios from "axios";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [accessToken, setAccessToken] = useState(localStorage.getItem("accessToken") || "");
    const [refreshToken, setRefreshToken] = useState(localStorage.getItem("refreshToken") || "");

    useEffect(() => {
        if (refreshToken) {
            refreshAccessToken();
        }
    }, []);

    const login = async (username, password) => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/token/", { username, password });
            setAccessToken(response.data.access);
            setRefreshToken(response.data.refresh);
            localStorage.setItem("accessToken", response.data.access);
            localStorage.setItem("refreshToken", response.data.refresh);
            setUser({ username });
        } catch (error) {
            console.error("Login failed", error);
        }
    };

    const refreshAccessToken = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/api/token/refresh/", { refresh: refreshToken });
            setAccessToken(response.data.access);
            localStorage.setItem("accessToken", response.data.access);
        } catch (error) {
            console.error("Failed to refresh token", error);
            logout();
        }
    };

    const logout = () => {
        setAccessToken(null);
        setRefreshToken(null);
        setUser(null);
        localStorage.removeItem("accessToken");
        localStorage.removeItem("refreshToken");
    };

    return (
        <AuthContext.Provider value={{ user, accessToken, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;
