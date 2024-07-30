// src/FeedbackButton.js
import React from 'react';
import './FeedbackForm.css';

function FeedbackButton({ onClick }) {
  return (
    <button className="feedback-button" onClick={onClick}>
      Feedback
    </button>
  );
}

export default FeedbackButton;