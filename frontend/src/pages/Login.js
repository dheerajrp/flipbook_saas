import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    // Temporary authentication check
    if (username === "admin" && password === "password") {
      alert("Login successful!");
      navigate("/dashboard"); // Redirect to Dashboard
    } else {
      alert("Invalid username or password");
    }
  };

  const handleSignup = () => {
    alert("Signup feature coming soon!");
  };

  return (
    <div style={styles.container}>
      <h2>Login</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        style={styles.input}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={styles.input}
      />
      <button onClick={handleLogin} style={styles.button}>Sign In</button>
      <button onClick={handleSignup} style={styles.signupButton}>Sign Up</button>
    </div>
  );
}

// Simple inline CSS styles
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    height: "100vh",
    background: "#f5f5f5",
  },
  input: {
    margin: "10px",
    padding: "10px",
    width: "250px",
    fontSize: "16px",
  },
  button: {
    margin: "10px",
    padding: "10px",
    width: "150px",
    fontSize: "16px",
    cursor: "pointer",
    background: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "5px",
  },
  signupButton: {
    margin: "10px",
    padding: "10px",
    width: "150px",
    fontSize: "16px",
    cursor: "pointer",
    background: "#28a745",
    color: "white",
    border: "none",
    borderRadius: "5px",
  }
};

export default Login;
