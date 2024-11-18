import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const transferService = {
  transferFunds: async (data) => {
    const endpoint = `${API_URL}/api/v1/transfers`;
    console.log("Initiating transfer request to:", endpoint);
    console.log("Transfer payload:", data);
    try {
      const response = await axios.post(endpoint, data, { withCredentials: true });
      console.log("Transfer successful:", response.data);
      return response.data;
    } catch (error) {
      console.error("Transfer failed:", error.response?.data || error.message);
      throw error;
    }
  },

  getTransferHistory: async () => {
    const endpoint = `${API_URL}/api/v1/transfers/history`;
    console.log("Fetching transfer history from:", endpoint);
    try {
      const response = await axios.get(endpoint, { withCredentials: true });
      console.log("Transfer history fetched successfully:", response.data);
      return response.data;
    } catch (error) {
      console.error("Error fetching transfer history:", error.response?.data || error.message);
      throw error;
    }
  },
};

export default transferService;