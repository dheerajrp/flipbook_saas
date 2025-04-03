import React, { useEffect, useState } from "react";
import axios from "axios";
import { authHeader, logout } from "../services/authService";
import { useNavigate } from "react-router-dom";

const Dashboard = () => {
    const [message, setMessage] = useState("");
    const navigate = useNavigate();

    useEffect(() => {
        axios.get("http://127.0.0.1:8000/api/protected/", { headers: authHeader() })
            .then((response) => {
                setMessage(response.data.message);
            })
            .catch(() => {
                logout();
                navigate("/login"); // Redirect to login if unauthorized
            });
    }, [navigate]);

    return (
        <div>
            <h2>Dashboard</h2>
            <p>{message}</p>
            <button onClick={() => { logout(); navigate("/login"); }}>Logout</button>
        </div>
    );
};

export default Dashboard;
