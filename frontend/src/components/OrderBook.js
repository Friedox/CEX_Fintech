import React from "react";

const OrderBook = ({ buyOrders, sellOrders }) => (
  <div className="order-book">
    <h3>Order Book</h3>
    <div className="orders">
      <div className="buy-orders">
        <h4>Buy Orders</h4>
        {buyOrders.length === 0 ? (
          <p>No buy orders available.</p>
        ) : (
          <ul>
            {buyOrders.map((order, index) => (
              <li key={index}>
                {order.price} x {order.amount}
              </li>
            ))}
          </ul>
        )}
      </div>
      <div className="sell-orders">
        <h4>Sell Orders</h4>
        {sellOrders.length === 0 ? (
          <p>No sell orders available.</p>
        ) : (
          <ul>
            {sellOrders.map((order, index) => (
              <li key={index}>
                {order.price} x {order.amount}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  </div>
);

export default OrderBook;