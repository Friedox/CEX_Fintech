import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const faucetService = {
  // Fetch available tokens
  getTokens: async () => {
    const endpoint = `${API_URL}/api/v1/faucet/tokens`;
    console.log("Fetching tokens from:", endpoint);

    try {
      const response = await axios.get(endpoint, { withCredentials: true }); // Include cookies
      console.log("Tokens fetched successfully:", response.data);
      return response.data;
    } catch (error) {
      console.error(
        "Error fetching tokens:",
        error.response?.data || error.message
      );
      throw error;
    }
  },

  // Claim tokens using token ticker
  claimTokens: async (tokenTicker) => {
    const endpoint = `${API_URL}/api/v1/faucet/claim`;
    const payload = { token_ticker: tokenTicker };

    console.log("Attempting to claim tokens:");
    console.log("Endpoint:", endpoint);
    console.log("Payload:", payload);

    try {
      const response = await axios.post(endpoint, payload, {
        withCredentials: true, // Include cookies
      });
      console.log("Tokens claimed successfully:", response.data);
      return response.data;
    } catch (error) {
      console.error(
        "Error claiming tokens:",
        error.response?.data || error.message
      );
      throw error;
    }
  },
};

export default faucetService;