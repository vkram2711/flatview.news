import React from 'react';
import { HashRouter, Route, Routes } from 'react-router-dom';
import NewsFeed from './NewsFeed';
import Article from './Article';
import CustomDropdown from './CustomDropdown';
import { ArticlesProvider } from './ArticlesContext';
import './App.css';

function App() {
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
          </div>
        </HashRouter>
      </ArticlesProvider>
  );
}

export default App;