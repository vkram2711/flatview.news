// src/Article.js
import React, { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { ArticlesContext } from './ArticlesContext';
import './App.css';
import { formatDistanceToNow } from 'date-fns';
import { extractDomain, capitalizeFirstLetter } from './utils';
import { API_BASE_URL } from './config';

function Article() {
  const { id } = useParams();
  const { language } = useContext(ArticlesContext);
  const [article, setArticle] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchArticle = async () => {
      setIsLoading(true);
      const response = await fetch(`${API_BASE_URL}/article/${id}?language=${language}`);
      const data = await response.json();
      setArticle(data);
      setIsLoading(false);
    };

    fetchArticle();
  }, [id, language]);

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!article) {
    return <div>Article not found</div>;
  }

  const sourceName = article.source.name || extractDomain(article.source.url);

  return (
    <div className="article-content">
      <h1>{article.title}</h1>
      <p><small>{formatDistanceToNow(new Date(article.publish_date))} ago</small></p>
      {article.country && <p><small>Country: {capitalizeFirstLetter(article.country)}</small></p>}
      {article.creator && <p><small>Author: {article.creator}</small></p>}
      <img src={article.image_url} alt={article.title} />
      <div className="article-source-info">
        <div className="source-card">
          <p>
            {article.source.icon && (
              <img src={article.source.icon} alt={sourceName} className="source-icon" />
            )}
            <a href={article.source.url} target="_blank" rel="noopener noreferrer">{sourceName}</a>
          </p>
          {article.country && <p>Country: {capitalizeFirstLetter(article.country)}</p>}
          {article.creator && <p>Author: {article.creator}</p>}
        </div>
      </div>
      <p>{article.content}</p>
    </div>
  );
}

export default Article;