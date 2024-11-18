import React, { useState } from "react";
import tradeService from "../services/tradeService";

const OrderForm = ({ tokenTicker, refreshOrderBook }) => {
  const [orderType, setOrderType] = useState("buy");
  const [price, setPrice] = useState("");
  const [amount, setAmount] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!price || !amount) {
      setMessage("Price and amount are required.");
      return;
    }

    setLoading(true);
    try {
      const response = await tradeService.createOrder({
        token_ticker: tokenTicker,
        order_type: orderType,
        price: parseFloat(price),
        amount: parseFloat(amount),
      });
      setMessage(response.message || "Order placed successfully.");
      setPrice("");
      setAmount("");
      refreshOrderBook();
    } catch (error) {
      setMessage(
        error.response?.data?.message || "Failed to place order. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="order-form">
      <h3>Place an Order</h3>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Order Type:</label>
          <select
            value={orderType}
            onChange={(e) => setOrderType(e.target.value)}
          >
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
        </div>
        <div>
          <label>Price:</label>
          <input
            type="number"
            step="0.01"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
          />
        </div>
        <div>
          <label>Amount:</label>
          <input
            type="number"
            step="0.01"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Placing..." : "Place Order"}
        </button>
      </form>
      {message && <p>{message}</p>}
    </div>
  );
};

export default OrderForm;