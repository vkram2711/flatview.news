import React, { useContext } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ArticlesContext } from './ArticlesContext';
import './App.css';
import { formatDistanceToNow } from 'date-fns';

function NewsFeed() {
  const { articles, isLoading } = useContext(ArticlesContext);
  const navigate = useNavigate();

  const handleClick = (index) => {
    navigate(`/article/${articles[index]._id}`);
  };

  return (
    <div className="news-feed">
      <h1>News Feed</h1>
      {isLoading ? (
        <div className="loading-bar">Loading...</div>
      ) : (
        articles.map((article, index) => (
          <div key={index} className="article-summary" onClick={() => handleClick(index)}>
            <img src={article.image_url} alt={article.title} className="article-image" />
            <div className="article-details">
              <h2>{article.title}</h2>
              <p>{article.description}</p>
              <p><small>{formatDistanceToNow(new Date(article.publish_date))} ago</small></p>
            </div>
          </div>
        ))
      )}
    </div>
  );
}

export default NewsFeed;