import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NewsFeed from './NewsFeed';
import Article from './Article';
import CustomDropdown from './CustomDropdown';
import { ArticlesProvider } from './ArticlesContext';
import './App.css';

function App() {
  return (
    <ArticlesProvider>
      <Router>
        <div className="App">
          <header>
            <CustomDropdown />
          </header>
          <Routes>
            <Route path="/" element={<NewsFeed />} />
            <Route path="/article/:id" element={<Article />} />
          </Routes>
        </div>
      </Router>
    </ArticlesProvider>
  );
}

export default App;