import React from 'react';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';

const FAQPage = () => {
  return (
    <>
      <Navbar />
      <div className="container">
        <h2>Frequently Asked Questions</h2>
        <p>Find answers to the most common questions about our platform, trading, and security.</p>
        <p>If you need more help, feel free to reach out to our support team for additional assistance.</p>
      </div>
      <Footer />
    </>
  );
};

export default FAQPage;