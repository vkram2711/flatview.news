// src/App.js
import React, { useState } from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';
import { Auth0Provider } from '@auth0/auth0-react';
import { Elements } from '@stripe/react-stripe-js';
import { stripePromise } from './stripeConfig';
import NewsFeed from './NewsFeed';
import CustomDropdown from './CustomDropdown';
import { ArticlesProvider } from './ArticlesContext';
import FeedbackButton from './FeedbackButton';
import FeedbackForm from './FeedbackForm';
import LoginButton from './LoginButton';
import Profile from './Profile';
import './App.css';
import authConfig from './auth_config.json';
import CheckoutForm from "./CheckoutForm";

function App() {
  const [isFeedbackFormVisible, setIsFeedbackFormVisible] = useState(false);

  const toggleFeedbackForm = () => {
    setIsFeedbackFormVisible(!isFeedbackFormVisible);
  };

  return (
    <Auth0Provider
      domain={authConfig.domain}
      clientId={authConfig.clientId}
      authorizationParams={{
        redirect_uri: window.location.origin
      }}
      useRefreshTokens={true}
      cacheLocation="localstorage"
    >
      <ArticlesProvider>
        <HashRouter>
          <Elements stripe={stripePromise}>
            <div className="App">
              <header>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%'}}>
                  <div style={{display: 'flex', alignItems: 'center'}}>
                    <CustomDropdown/>
                  </div>
                  <div>
                    <LoginButton/>
                  </div>
                </div>
              </header>

              <Routes>
                <Route path="/" element={<NewsFeed/>}/>
                <Route path="/checkout" element={<CheckoutForm/>}/>
                <Route path="/profile" element={<Profile/>}/>
              </Routes>
              <FeedbackButton onClick={toggleFeedbackForm}/>
              {isFeedbackFormVisible && <FeedbackForm onClose={toggleFeedbackForm}/>}
            </div>
          </Elements>
        </HashRouter>
      </ArticlesProvider>
    </Auth0Provider>
  );
}

export default App;