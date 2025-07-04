import React from 'react';
import { translateCardArraysInMessage } from './cardUtils';

const ScoreDisplay = ({ score }) => {
  if (!score) {
    return (
      <div className="score-section">
        <div className="score-placeholder">
          <p>Select all 5 cards and click "Calculate Score" to see the result</p>
        </div>
      </div>
    );
  }

  const formatMessage = (message) => {
    if (!message) return [];
    
    // Split the message by | and filter out empty strings
    return message.split('|').filter(msg => msg.trim().length > 0);
  };

  const messages = formatMessage(score.message);

  return (
    <div className="score-section">
      <div className="score-display">
        <div className="score-header">
          <h2>Score</h2>
          <div className="score-value">{score.score}</div>
        </div>
        
        {messages.length > 0 && (
          <div className="score-breakdown">
            <h3>Breakdown</h3>
            <div className="breakdown-list">
              {messages.map((message, index) => (
                <div key={index} className="breakdown-item">
                  {translateCardArraysInMessage(message.trim())}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ScoreDisplay;
