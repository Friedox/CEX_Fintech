import React, { useState, useEffect } from "react";
import { useSelector } from "react-redux";
import Navbar from "../../components/Navbar";
import Footer from "../../components/Footer";
import faucetService from "../../services/faucetService";

const FaucetPage = () => {
  const { user, isAuthenticated } = useSelector((state) => state.auth);
  const [tokens, setTokens] = useState([]);
  const [selectedToken, setSelectedToken] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [fetchingTokens, setFetchingTokens] = useState(true);

  // Fetch tokens when component loads
  useEffect(() => {
    const fetchTokens = async () => {
      try {
        console.log("Fetching available tokens...");
        const response = await faucetService.getTokens();
        console.log("Available tokens fetched:", response);
        setTokens(response.detail || []); // Ensure tokens are properly assigned
      } catch (error) {
        console.error("Failed to fetch tokens:", error);
        setMessage("Failed to fetch tokens. Please try again later.");
      } finally {
        setFetchingTokens(false);
      }
    };

    fetchTokens();
  }, []);

  const handleClaim = async () => {
    if (!isAuthenticated || !user?.id) {
      setMessage("You must be logged in to claim tokens.");
      return;
    }

    if (!selectedToken) {
      setMessage("Please select a token to claim.");
      return;
    }

    setLoading(true);
    try {
      console.log("Attempting to claim tokens for:", selectedToken);
      const response = await faucetService.claimTokens(selectedToken);
      console.log("Claim response:", response);

      if (response.success) {
        setMessage(
          `Successfully claimed ${response.detail.amount} ${selectedToken}!`
        );
      } else {
        setMessage(response.detail?.message || "Failed to claim tokens.");
      }
    } catch (error) {
      console.error("Error while claiming tokens:", error);
      setMessage(error.response?.data?.message || "Failed to claim tokens.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="full-height">
      <Navbar />
      <div className="faucet-page">
        <h1>Faucet</h1>
        <p>Select a token to claim 5% of its total supply!</p>

        {fetchingTokens ? (
          <p>Loading available tokens...</p>
        ) : tokens.length === 0 ? (
          <p>No tokens available for claiming.</p>
        ) : (
          <>
            <select
              value={selectedToken}
              onChange={(e) => setSelectedToken(e.target.value)}
            >
              <option value="">-- Select a Token --</option>
              {tokens.map((token) => (
                <option key={token.ticker} value={token.ticker}>
                  {token.ticker} (Remaining: {token.remaining_supply} / Total:{" "}
                  {token.total_supply})
                </option>
              ))}
            </select>
            <button onClick={handleClaim} disabled={loading || !selectedToken}>
              {loading ? "Claiming..." : "Claim Tokens"}
            </button>
          </>
        )}

        {message && <p>{message}</p>}
      </div>
      <Footer />
    </div>
  );
};

export default FaucetPage;