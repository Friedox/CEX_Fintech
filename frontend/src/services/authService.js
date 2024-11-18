import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const authService = {
  register: async (data) => {
    const endpoint = `${API_URL}/api/v1/auth/signup`;
    console.log("Sending registration request:", data);
    return axios.post(endpoint, data);
  },

  login: async (data) => {
    const endpoint = `${API_URL}/api/v1/auth/login`;
    const payload = {
      login: data.email, // Map 'email' to 'login'
      password: data.password,
    };
    console.log("Sending login request:", payload);
    return axios.post(endpoint, payload, { withCredentials: true }); // Include cookies
  },

  getUserDetails: async () => {
    const endpoint = `${API_URL}/api/v1/auth/users/me/`;
    console.log("Fetching user details");
    try {
      const response = await axios.get(endpoint, { withCredentials: true }); // Send cookies
      console.log(response.data)
      return response.data; // Returns user details including user_id
    } catch (error) {
      console.error("Error fetching user details:", error.response?.data || error.message);
      throw error;
    }
  },
};

export default authService;
