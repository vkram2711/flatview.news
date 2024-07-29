import React, { createContext, useState, useEffect } from 'react';

export const ArticlesContext = createContext();

export const ArticlesProvider = ({ children }) => {
  const [articles, setArticles] = useState([]);
  const [language, setLanguage] = useState('en');

  useEffect(() => {
    fetch(`http://127.0.0.1:5000/top_news?language=${language}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setArticles(data.original_articles);
      })
      .catch(error => console.error('Error fetching articles:', error));
  }, [language]);

  return (
    <ArticlesContext.Provider value={{ articles, language, setLanguage }}>
      {children}
    </ArticlesContext.Provider>
  );
};