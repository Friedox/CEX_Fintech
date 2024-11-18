import React from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';

const FeaturesPage = () => {
  return (
    <>
      <Navbar />
      <div className="container">
        <h2>Platform Features</h2>
        <p>Discover the unique features and tools offered by our crypto exchange platform.</p>
        <p>From advanced trading tools to secure wallet options, our platform is designed to enhance your trading experience.</p>
      </div>
      <Footer />
    </>
  );
};

export default FeaturesPage;