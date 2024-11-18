import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000";

const tokenService = {
  createToken: async (tokenData) => {
    const endpoint = `${API_URL}/api/v1/tokens/`;
    const response = await axios.post(endpoint, tokenData);
    return response.data;
  },
};

export default tokenService;