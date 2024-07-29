import React, { useContext } from 'react';
import { useParams } from 'react-router-dom';
import { ArticlesContext } from './ArticlesContext';
import './App.css';

function Article() {
  const { id } = useParams();
  const { articles } = useContext(ArticlesContext);
  const article = articles[id];

  return (
    <div className="article-content">
      <h1>{article.title}</h1>
      <p><small>{new Date(article.publish_date).toLocaleDateString()}</small></p>
      {article.image_url && <img src={article.image_url} alt={article.title} />}
      <p>{article.content}</p>
      <a href={article.source.url} target="_blank" rel="noopener noreferrer">Source</a>
    </div>
  );
}

export default Article;