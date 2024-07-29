import React, { useState, useContext } from 'react';
import { ArticlesContext } from './ArticlesContext';
import './CustomDropdown.css';

function CustomDropdown() {
  const { language, setLanguage } = useContext(ArticlesContext);
  const [isOpen, setIsOpen] = useState(false);

  const languages = [
    { code: 'ar', name: 'Arabic' },
    { code: 'en', name: 'English' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'ja', name: 'Japanese' },
    { code: 'es', name: 'Spanish' },
    { code: 'uk', name: 'Ukrainian' },
  ];

  const handleLanguageChange = (code) => {
    setLanguage(code);
    setIsOpen(false);
  };

  return (
    <div className="custom-dropdown">
      <button onClick={() => setIsOpen(!isOpen)} className="dropdown-button">
        {languages.find(lang => lang.code === language).name}
      </button>
      {isOpen && (
        <ul className="dropdown-menu">
          {languages.map(lang => (
            <li key={lang.code} onClick={() => handleLanguageChange(lang.code)}>
              {lang.name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default CustomDropdown;