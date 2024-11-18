import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const tradeService = {
  getOrderBook: async (pair) => {
    const endpoint = `${API_URL}/api/v1/orders/${pair}/book`;
    console.log(`Fetching order book for pair: ${pair}`);
    try {
      const response = await axios.get(endpoint, { withCredentials: true });
      return response.data;
    } catch (error) {
      console.error("Error fetching order book:", error.response?.data || error.message);
      throw error;
    }
  },
  getTradeHistory: async (pair) => {
    const endpoint = `${API_URL}/api/v1/trades/history/${pair}`;
    console.log(`Fetching trade history for pair: ${pair}`);
    try {
      const response = await axios.get(endpoint, { withCredentials: true });
      return response.data;
    } catch (error) {
      console.error("Error fetching trade history:", error.response?.data || error.message);
      throw error;
    }
  },
};

export default tradeService;