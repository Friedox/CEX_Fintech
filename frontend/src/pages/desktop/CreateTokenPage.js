import React, { useState } from "react";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import tokenService from "../../services/tokenService";

const CreateTokenPage = () => {
  const [formData, setFormData] = useState({ name: "", ticker: "", total_supply: "" });
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!formData.name || !formData.ticker || !formData.total_supply) {
      setMessage("All fields are required.");
      return;
    }

    setLoading(true);
    try {
      await tokenService.createToken(formData);
      setMessage("Token created successfully!");
    } catch (error) {
      console.error("Token creation failed:", error);
      setMessage("Failed to create token. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-height">
      <Navbar />
      <div className="create-token-page">
        <h1>Create Token</h1>
        <form onSubmit={handleSubmit}>
          <label>
            Name:
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Ticker:
            <input
              type="text"
              name="ticker"
              value={formData.ticker}
              onChange={handleChange}
              required
            />
          </label>
          <label>
            Total Supply:
            <input
              type="number"
              name="total_supply"
              value={formData.total_supply}
              onChange={handleChange}
              required
            />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? "Creating..." : "Create Token"}
          </button>
        </form>
        {message && <p>{message}</p>}
      </div>
      <Footer />
    </div>
  );
};

export default CreateTokenPage;
