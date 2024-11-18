import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const walletService = {
  getBalances: async () => {
    const endpoint = `${API_URL}/api/v1/wallets/balances`;
    return axios.get(endpoint);
  },
  getWalletDetails: async (token) => {
    const endpoint = `${API_URL}/api/v1/wallets/${token}`;
    return axios.get(endpoint);
  },
  deposit: async (data) => {
    const endpoint = `${API_URL}/api/v1/wallets/deposit`;
    return axios.post(endpoint, data);
  },
  withdraw: async (data) => {
    const endpoint = `${API_URL}/api/v1/wallets/withdraw`;
    return axios.post(endpoint, data);
  },
};

export default walletService;