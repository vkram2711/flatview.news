// src/NewsFeed.js
import React, { useContext } from 'react';
import { ArticlesContext } from './ArticlesContext';
import './App.css';
import { formatDistanceToNow } from 'date-fns';
import { extractDomain } from './utils';

function NewsFeed() {
  const { articles, isLoading } = useContext(ArticlesContext);

  const handleClick = (url) => {
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return (
    <div className="news-feed">
      <h1>News Feed</h1>
      {isLoading ? (
        <div className="loading-bar">Loading...</div>
      ) : (
        articles.map((article, index) => (
          <div key={index} className="article-summary" onClick={() => handleClick(article.source.url)}>
            <img src={article.image_url} alt={article.title} className="article-image"/>
            <div className="article-details">
              <h2>{article.title}</h2>
              <p>{article.description}</p>
              <p><small>{formatDistanceToNow(new Date(article.publish_date))} ago</small></p>
              {article.country && <p><small>Country: {article.country}</small></p>}
            </div>
            <div className="article-source">{extractDomain(article.source.url)}</div>
          </div>
        ))
      )}
    </div>
  );
}

export default NewsFeed;