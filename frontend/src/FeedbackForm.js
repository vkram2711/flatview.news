// src/FeedbackForm.js
import React, { useState } from 'react';
import './FeedbackForm.css';
import {API_BASE_URL} from "./config";

function FeedbackForm({ onClose }) {
  const [rating, setRating] = useState(null);
  const [feedback, setFeedback] = useState('');
  const [contact, setEmail] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch(`${API_BASE_URL}/feedback`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rating, feedback, contact }),
      });
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      onClose();
    } catch (error) {
      console.error('Error submitting feedback:', error);
    }
  };

  return (
    <div className="feedback-form-overlay">
      <div className="feedback-form">
        <button className="close-button" onClick={onClose}>X</button>
        <form onSubmit={handleSubmit}>
          <label>
            Rating:
            <div className="rating-buttons">
              {[...Array(10)].map((_, i) => (
                <button
                  type="button"
                  key={i + 1}
                  className={`rating-button ${rating === i + 1 ? 'selected' : ''}`}
                  onClick={() => setRating(i + 1)}
                >
                  {i + 1}
                </button>
              ))}
            </div>
          </label>
          <label>
            Feedback:
            <textarea
              className="feedback-textarea"
              value={feedback}
              onChange={(e) => setFeedback(e.target.value)}
            />
          </label>
          <label>
            Email:
            <input
              className="feedback-input"
              type="email"
              value={contact}
              onChange={(e) => setEmail(e.target.value)}
            />
          </label>
          <button className="submit-button" type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default FeedbackForm;