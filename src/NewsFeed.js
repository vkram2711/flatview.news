import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { ArticlesContext } from './ArticlesContext';
import './App.css';

function NewsFeed() {
  const { articles, language, setLanguage } = useContext(ArticlesContext);

  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  return (
    <div className="App">
      <header>
        <select value={language} onChange={handleLanguageChange}>
          <option value="ar">Arabic</option>
          <option value="en">English</option>
          <option value="fr">French</option>
          <option value="de">German</option>
          <option value="ja">Japanese</option>
          <option value="es">Spanish</option>
          <option value="uk">Ukrainian</option>
        </select>
      </header>
      <h1>News Feed</h1>
      {articles.map((article, index) => (
        <div key={index} className="article-summary">
          <h2>{article.title}</h2>
          <p>{article.description}</p>
          <p><small>{new Date(article.publish_date).toLocaleDateString()}</small></p>
          <Link to={`/article/${index}`}>Read more</Link>
        </div>
      ))}
    </div>
  );
}

export default NewsFeed;