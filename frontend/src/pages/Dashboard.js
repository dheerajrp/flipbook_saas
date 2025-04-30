import React, { useEffect, useState } from "react";
import { getFlipbooks } from "../api/api";

const Dashboard = () => {
  const [flipbooks, setFlipbooks] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchFlipbooks = async () => {
      const token = localStorage.getItem("access_token");
      if (!token) {
        setError("Unauthorized. Please log in.");
        return;
      }

      try {
        const data = await getFlipbooks(token);
        setFlipbooks(data);
      } catch (err) {
        setError(err.detail || "Error fetching flipbooks");
      }
    };

    fetchFlipbooks();
  }, []);

  return (
    <div>
      <h2>Flipbooks</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <ul>
        {flipbooks.map((flipbook) => (
          <li key={flipbook.id}>{flipbook.title}</li>
        ))}
      </ul>
    </div>
  );
};

export default Dashboard;
