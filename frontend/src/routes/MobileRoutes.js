import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from '../store';
import Login from '../pages/mobile/LoginPage';


function MobileRoutes() {
    return (
        <Provider store={store}>
            <Routes>
                <Route path="/" element={<Login />} />
            </Routes>
        </Provider>
    );
}

export default MobileRoutes;