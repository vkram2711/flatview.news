// src/App.js
import React, { useState } from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';
import NewsFeed from './NewsFeed';
import Article from './Article';
import CustomDropdown from './CustomDropdown';
import { ArticlesProvider } from './ArticlesContext';
import FeedbackButton from './FeedbackButton';
import FeedbackForm from './FeedbackForm';
import './App.css';

function App() {
  const [isFeedbackFormVisible, setIsFeedbackFormVisible] = useState(false);

  const toggleFeedbackForm = () => {
    setIsFeedbackFormVisible(!isFeedbackFormVisible);
  };

  return (
    <ArticlesProvider>
      <HashRouter>
        <div className="App">
          <header>
            <CustomDropdown />
          </header>
          <Routes>
            <Route path="/" element={<NewsFeed />} />
            <Route path="/article/:id" element={<Article />} />
          </Routes>
          <FeedbackButton onClick={toggleFeedbackForm} />
          {isFeedbackFormVisible && <FeedbackForm onClose={toggleFeedbackForm} />}
        </div>
      </HashRouter>
    </ArticlesProvider>
  );
}

export default App;