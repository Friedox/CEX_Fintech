import React from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';

const MarketPage = () => {
  return (
    <>
      <Navbar />
      <div className="container">
        <h2>Market Overview</h2>
        <p>Explore the latest trends, prices, and analytics in the cryptocurrency market.</p>
        <p>Here you will find an overview of current market prices, recent changes, and trading volumes for major cryptocurrencies.</p>
      </div>
      <Footer />
    </>
  );
};

export default MarketPage;