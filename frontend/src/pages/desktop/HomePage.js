import React from 'react';
import Navbar from '../../components/Navbar';
import HeroSection from '../../components/HeroSection';
import MarketOverview from '../../components/MarketOverview';
import FeaturesSection from '../../components/FeaturesSection';
import Testimonials from '../../components/Testimonials';
import SecurityFeatures from '../../components/SecurityFeatures';
import FAQSection from '../../components/FAQSection';
import Footer from '../../components/Footer';

const HomePage = () => {
  return (
    <div>
      <Navbar />
      <HeroSection />
      <MarketOverview />
      <FeaturesSection />
      <Testimonials />
      <SecurityFeatures />
      <FAQSection />
      <Footer />
    </div>
  );
};

export default HomePage;