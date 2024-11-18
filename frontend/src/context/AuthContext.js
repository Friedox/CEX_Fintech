import React, { createContext, useState, useEffect } from "react";
import axios from "axios";

const AuthContext = createContext({
  user: null,
  isAuthenticated: false,
  login: () => {},
  logout: () => {},
});

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem("token");
      if (token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
        await fetchUserData(); // Await the promise
      }
    };

    fetchData(); // Ensure the promise is handled
  }, []);

  const fetchUserData = async () => {
    try {
      console.log("Fetching user data...");
      const response = await axios.get("/api/v1/auth/users/me/");
      console.log("User data received:", response.data);
      setUser(response.data);
      setIsAuthenticated(true);
    } catch (error) {
      console.error("Failed to fetch user data:", error);
      localStorage.removeItem("token");
      setIsAuthenticated(false);
      setUser(null);
    }
  };

  const login = (token) => {
    console.log("Setting token and fetching user data...");
    localStorage.setItem("token", token);
    axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    fetchUserData(); // Fetch user data after login
  };

  const logout = () => {
    console.log("Logging out...");
    setUser(null);
    setIsAuthenticated(false);
    localStorage.removeItem("token");
    delete axios.defaults.headers.common["Authorization"];
  };

  return (
    <AuthContext.Provider value={{ user, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;