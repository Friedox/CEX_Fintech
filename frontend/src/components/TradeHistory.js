import React from "react";

const TradeHistory = ({ trades }) => (
  <div className="trade-history">
    <h3>Trade History</h3>
    {trades.length === 0 ? (
      <p>No trade history available for this pair.</p>
    ) : (
      <ul>
        {trades.map((trade, index) => (
          <li key={index}>
            {trade.timestamp}: {trade.amount} @ {trade.price}
          </li>
        ))}
      </ul>
    )}
  </div>
);

export default TradeHistory;