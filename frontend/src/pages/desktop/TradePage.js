import React, { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import faucetService from "../../services/faucetService";

const TradePage = () => {
  const [tokens, setTokens] = useState([]);
  const [selectedToken1, setSelectedToken1] = useState("");
  const [selectedToken2, setSelectedToken2] = useState("");
  const [tokenPair, setTokenPair] = useState("");
  const [primaryOrderBook, setPrimaryOrderBook] = useState({ buy_orders: [], sell_orders: [] });
  const [secondaryOrderBook, setSecondaryOrderBook] = useState({ buy_orders: [], sell_orders: [] });
  const [combinedOrderBook, setCombinedOrderBook] = useState({ buy_orders: [], sell_orders: [] });
  const [primarySocket, setPrimarySocket] = useState(null);
  const [secondarySocket, setSecondarySocket] = useState(null);
  const [price, setPrice] = useState("");
  const [quantity, setQuantity] = useState("");
  const [orderType, setOrderType] = useState("buy");
  const [message, setMessage] = useState("");
  const [loadingTokens, setLoadingTokens] = useState(true);

  // Fetch tokens on component load
  useEffect(() => {
    const fetchTokens = async () => {
      try {
        const response = await faucetService.getTokens();
        setTokens(response.detail || []);
      } catch (error) {
        console.error("Failed to fetch tokens:", error);
        setMessage("Failed to fetch tokens. Please try again later.");
      } finally {
        setLoadingTokens(false);
      }
    };

    fetchTokens();
  }, []);

  // Create trading pair when two tokens are selected
  useEffect(() => {
    if (selectedToken1 && selectedToken2) {
      setTokenPair(`${selectedToken1}/${selectedToken2}`);
    }
  }, [selectedToken1, selectedToken2]);

  // Fetch orders for both token pairs and combine them
  useEffect(() => {
    const combineOrderBooks = () => {
      const invertedSecondaryOrderBook = {
        buy_orders: secondaryOrderBook.sell_orders.map((order) => ({
          id: order.id,
          price: order.quantity,
          quantity: order.price,
        })),
        sell_orders: secondaryOrderBook.buy_orders.map((order) => ({
          id: order.id,
          price: order.quantity,
          quantity: order.price,
        })),
      };

      const combinedBuyOrders = [...primaryOrderBook.buy_orders, ...invertedSecondaryOrderBook.buy_orders].sort(
        (a, b) => b.price - a.price
      );
      const combinedSellOrders = [...primaryOrderBook.sell_orders, ...invertedSecondaryOrderBook.sell_orders].sort(
        (a, b) => a.price - b.price
      );

      setCombinedOrderBook({ buy_orders: combinedBuyOrders, sell_orders: combinedSellOrders });
    };

    combineOrderBooks();
  }, [primaryOrderBook, secondaryOrderBook]);

  // Connect to WebSocket when token pair changes
  useEffect(() => {
    if (tokenPair) {
      const [token1, token2] = tokenPair.split("/");
      const pair1 = `${token1}-${token2}`;
      const pair2 = `${token2}-${token1}`;

      // WebSocket for primary pair
      const ws1 = new WebSocket(`ws://localhost:8000/api/v1/trade_ws/${pair1}`);
      setPrimarySocket(ws1);

      ws1.onopen = () => {
        ws1.send(JSON.stringify({ action: "get_order_book" }));
      };

      ws1.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === "order_book_update") {
          setPrimaryOrderBook(message.data);
        }
      };

      ws1.onerror = () => setMessage("WebSocket error occurred.");
      ws1.onclose = () => setMessage("WebSocket connection for primary pair closed.");

      // WebSocket for secondary pair
      const ws2 = new WebSocket(`ws://localhost:8000/api/v1/trade_ws/${pair2}`);
      setSecondarySocket(ws2);

      ws2.onopen = () => {
        ws2.send(JSON.stringify({ action: "get_order_book" }));
      };

      ws2.onmessage = (event) => {
        const message = JSON.parse(event.data);
        if (message.type === "order_book_update") {
          setSecondaryOrderBook(message.data);
        }
      };

      ws2.onerror = () => setMessage("WebSocket error occurred.");
      ws2.onclose = () => setMessage("WebSocket connection for secondary pair closed.");

      return () => {
        ws1.close();
        ws2.close();
      };
    }
  }, [tokenPair]);

  const handleCreateOrder = () => {
    // Decide the primary WebSocket connection
    const activeSocket = primarySocket;

    // Ensure the WebSocket is ready before sending
    if (!activeSocket || activeSocket.readyState !== WebSocket.OPEN) {
      setMessage("WebSocket connection not established.");
      console.error("WebSocket is not open:", activeSocket?.readyState);
      return;
    }

    // Validate price and quantity inputs
    if (!price || !quantity || isNaN(price) || isNaN(quantity)) {
      setMessage("Please enter valid price and quantity.");
      console.error("Invalid price or quantity:", { price, quantity });
      return;
    }

    // Create the order payload
    const orderPayload = {
      action: "create_order",
      order: {
        token_pair: tokenPair,
        price: parseFloat(price), // Ensure price is sent as a number
        quantity: parseFloat(quantity), // Ensure quantity is sent as a number
        order_type: orderType,
      },
    };

    // Log the payload for debugging purposes
    console.log("Sending order payload:", orderPayload);

    // Send the payload to the WebSocket server
    activeSocket.send(JSON.stringify(orderPayload));

    // Provide feedback to the user
    setMessage("Order sent successfully!");
  };

  return (
    <div className="full-height">
      <Navbar />
      <div className="trade-page">
        <h1>Trade Page</h1>

        <div className="token-selector">
          {loadingTokens ? (
            <p>Loading tokens...</p>
          ) : tokens.length === 0 ? (
            <p>No tokens available.</p>
          ) : (
            <>
              <label>Select Token 1:</label>
              <select value={selectedToken1} onChange={(e) => setSelectedToken1(e.target.value)}>
                <option value="">-- Select Token --</option>
                {tokens.map((token) => (
                  <option key={token.id} value={token.ticker}>
                    {token.ticker}
                  </option>
                ))}
              </select>
              <label>Select Token 2:</label>
              <select value={selectedToken2} onChange={(e) => setSelectedToken2(e.target.value)}>
                <option value="">-- Select Token --</option>
                {tokens.map((token) => (
                  <option key={token.id} value={token.ticker}>
                    {token.ticker}
                  </option>
                ))}
              </select>
              {tokenPair && <p>Selected Pair: {tokenPair}</p>}
            </>
          )}
        </div>

        <div className="order-form">
          <h2>Create Order</h2>
          <label>Order Type:</label>
          <select value={orderType} onChange={(e) => setOrderType(e.target.value)}>
            <option value="buy">Buy</option>
            <option value="sell">Sell</option>
          </select>
          <label>Price:</label>
          <input type="number" value={price} onChange={(e) => setPrice(e.target.value)} />
          <label>Quantity:</label>
          <input type="number" value={quantity} onChange={(e) => setQuantity(e.target.value)} />
          <button onClick={handleCreateOrder}>Place Order</button>
        </div>

        <div className="order-book">
          <h2>Order Book</h2>
          <div className="order-section">
            <h3>Buy Orders</h3>
            {combinedOrderBook.buy_orders.length === 0 ? (
              <p>No buy orders available.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Quantity</th>
                    <th>Price</th>
                  </tr>
                </thead>
                <tbody>
                  {combinedOrderBook.buy_orders.map((order, index) => (
                    <tr key={index}>
                      <td>{order.quantity.toFixed(2)}</td>
                      <td>{order.price.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          <div className="order-section">
            <h3>Sell Orders</h3>
            {combinedOrderBook.sell_orders.length === 0 ? (
              <p>No sell orders available.</p>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Quantity</th>
                    <th>Price</th>
                  </tr>
                </thead>
                <tbody>
                  {combinedOrderBook.sell_orders.map((order, index) => (
                    <tr key={index}>
                      <td>{order.quantity.toFixed(2)}</td>
                      <td>{order.price.toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>

        {message && <p>{message}</p>}
      </div>
      <Footer />
    </div>
  );
};

export default TradePage;