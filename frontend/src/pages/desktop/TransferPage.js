import React, { useState } from "react";
import { useSelector } from "react-redux";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import transferService from "../../services/transferService";

const TransferPage = () => {
  const { user, isAuthenticated } = useSelector((state) => state.auth);
  const [formData, setFormData] = useState({ recipient: "", token: "", amount: "" });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!isAuthenticated || !user?.id) {
      setMessage("You must be logged in to perform a transfer.");
      return;
    }
    if (!formData.recipient || !formData.token || !formData.amount) {
      setMessage("All fields are required.");
      return;
    }

    setLoading(true);
    try {
      console.log("Submitting transfer form:", formData);
      const response = await transferService.transferFunds({
        sender_id: user.id, // Include sender's user ID
        receiver_id: parseInt(formData.recipient),
        token_ticker: formData.token,
        amount: parseFloat(formData.amount), // Ensure amount is numeric
      });
      setMessage(response.message || "Transfer successful!");
    } catch (error) {
      console.error("Transfer error:", error.response?.data || error.message);
      setMessage(
        error.response?.data?.message || "Transfer failed. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-height">
      <Navbar />
      <div className="transfer-page">
        <h1>Transfer Funds</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Recipient:
            <input
              type="text"
              name="recipient"
              value={formData.recipient}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Token:
            <input
              type="text"
              name="token"
              value={formData.token}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Amount:
            <input
              type="number"
              name="amount"
              value={formData.amount}
              onChange={handleChange}
              required
            />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? "Processing..." : "Transfer"}
          </button>
        </form>
        {message && <p>{message}</p>}
      </div>
      <Footer />
    </div>
  );
};

export default TransferPage;