import React from 'react';
import { Routes, Route } from 'react-router-dom';
import HomePage from '../pages/desktop/HomePage';
import MarketPage from '../pages/desktop/MarketPage';
import FeaturesPage from '../pages/desktop/FeaturesPage';
import FAQPage from '../pages/desktop/FAQPage';
import Dashboard from '../pages/desktop/Dashboard';
import LoginPage from '../pages/desktop/LoginPage';
import RegisterPage from '../pages/desktop/RegisterPage';
import PrivateRoute from '../routes/PrivateRoute';
import FaucetPage from "../pages/desktop/FaucetPage";
import TransferPage from "../pages/desktop/TransferPage";
import CreateTokenPage from "../pages/desktop/CreateTokenPage";
import TradePage from "../pages/desktop/TradePage";


const DesktopRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/market" element={<MarketPage />} />
      <Route path="/features" element={<FeaturesPage />} />
      <Route path="/faq" element={<FAQPage />} />

      {/* Защищённый маршрут для dashboard */}
      <Route element={<PrivateRoute />}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/crane" element={<FaucetPage />} />
        <Route path="/transfer" element={<TransferPage />} />
        <Route path="/trade" element={<TradePage />} />
        <Route path="/create-token" element={<CreateTokenPage />} />
      </Route>
    </Routes>
  );
};

export default DesktopRoutes;