import React from "react";
import { useSelector } from "react-redux";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";

const Dashboard = () => {
  // Get user and balance data from Redux
  const user = useSelector((state) => state.auth?.user);
  const balance = useSelector((state) => state.wallet?.balances);

  return (
    <div className="full-height">
      {/* Navbar */}
      <Navbar />
      <div className="dashboard">
        <div className="dashboard-content">
          <h1>Welcome to your Dashboard</h1>

          {/* User Info Section */}
          <section className="user-info">
            {user ? (
              <>
                <h2>Hello, {user.username}!</h2>
                <p>Email: {user.email}</p>
              </>
            ) : (
              <p>Loading user data...</p>
            )}
          </section>

          {/* Balances Section */}
          <section className="balance-info">
            <h2>Your Balances</h2>
            {balance ? (
              <ul>
                {Object.entries(balance).map(([currency, amount]) => (
                  <li key={currency}>
                    <strong>{currency.toUpperCase()}</strong>: {amount}
                  </li>
                ))}
              </ul>
            ) : (
              <p>Loading balance information...</p>
            )}
          </section>

          {/* Assets Section */}
          <section className="assets-info">
            <h2>Your Assets</h2>
            {balance ? (
              <div className="asset-list">
                {Object.entries(balance).map(([currency, amount]) => (
                  <div className="asset-card" key={currency}>
                    <p>
                      <strong>Asset:</strong> {currency.toUpperCase()}
                    </p>
                    <p>
                      <strong>Amount:</strong> {amount}
                    </p>
                    <p>
                      <strong>Value:</strong> $0.00 {/* Placeholder */}
                    </p>
                  </div>
                ))}
              </div>
            ) : (
              <p>No assets information available.</p>
            )}
          </section>
        </div>
      </div>

      {/* Footer */}
      <Footer />
    </div>
  );
};

export default Dashboard;