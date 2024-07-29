import React, { useContext, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { ArticlesContext } from './ArticlesContext';
import './App.css';
import { formatDistanceToNow } from 'date-fns';

function Article() {
  const { id } = useParams();
  const { language } = useContext(ArticlesContext);
  const [article, setArticle] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchArticle = async () => {
      setIsLoading(true);
      const response = await fetch(`http://127.0.0.1:5000/article/${id}?language=${language}`);
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

  return (
    <div className="article-content">
      <h1>{article.title}</h1>
      <p><small>{formatDistanceToNow(new Date(article.publish_date))} ago</small></p>
      <img src={article.image_url} alt={article.title} />
      <p>{article.content}</p>
    </div>
  );
}

export default Article;