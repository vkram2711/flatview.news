import React, { createContext, useState, useEffect } from 'react';

export const ArticlesContext = createContext();

export const ArticlesProvider = ({ children }) => {
  const [articles, setArticles] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [language, setLanguage] = useState(localStorage.getItem('language') || 'en');

  useEffect(() => {
    // Fetch articles based on the current language
    const fetchArticles = async () => {
      setIsLoading(true);
      const response = await fetch(`http://127.0.0.1:5000/top_news?language=${language}`);
      const data = await response.json();

      setArticles(data.original_articles);

      setIsLoading(false);
    };

    fetchArticles();
  }, [language]);

  useEffect(() => {
    localStorage.setItem('language', language);
  }, [language]);

  return (
    <ArticlesContext.Provider value={{ articles, isLoading, language, setLanguage }}>
      {children}
    </ArticlesContext.Provider>
  );
};