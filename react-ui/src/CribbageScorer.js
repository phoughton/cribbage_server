import React, { useState } from 'react';
import CardSlot from './CardSlot';
import ScoreDisplay from './ScoreDisplay';
import './CribbageScorer.css';

const CribbageScorer = () => {
  const [cards, setCards] = useState([null, null, null, null, null]); // 4 hand cards + 1 starter
  const [isCrib, setIsCrib] = useState(false);
  const [score, setScore] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'];
  const suits = ['H', 'D', 'C', 'S']; // Hearts, Diamonds, Clubs, Spades
  const suitSymbols = { 'H': '♥', 'D': '♦', 'C': '♣', 'S': '♠' };

  const updateCard = (index, card) => {
    const newCards = [...cards];
    newCards[index] = card;
    setCards(newCards);
    setScore(null); // Clear score when cards change
    setError(null);
  };

  const clearCard = (index) => {
    const newCards = [...cards];
    newCards[index] = null;
    setCards(newCards);
    setScore(null);
    setError(null);
  };

  const clearAll = () => {
    setCards([null, null, null, null, null]);
    setIsCrib(false);
    setScore(null);
    setError(null);
  };

  const isCardSelected = (rank, suit) => {
    return cards.some(card => card && card.rank === rank && card.suit === suit);
  };

  const canCalculateScore = () => {
    return cards.every(card => card !== null);
  };

  const calculateScore = async () => {
    if (!canCalculateScore()) {
      setError('Please select all 5 cards');
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      const starter = `${cards[0].rank}${cards[0].suit}`;
      const hand = cards.slice(1).map(card => `${card.rank}${card.suit}`);

      const response = await fetch('/score_hand_show', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          starter: starter,
          hand: hand,
          isCrib: isCrib
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Failed to calculate score');
      }

      const result = await response.json();
      setScore(result);
    } catch (err) {
      setError(err.message || 'Failed to calculate score');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="cribbage-scorer">
      <div className="header">
        <h1>Cribbage Scorer</h1>
      </div>

      <div className="cards-section">
        <div className="starter-section">
          <h3>Starter Card</h3>
          <CardSlot
            card={cards[0]}
            index={0}
            onUpdateCard={updateCard}
            onClearCard={clearCard}
            ranks={ranks}
            suits={suits}
            suitSymbols={suitSymbols}
            isCardSelected={isCardSelected}
            label="Starter"
          />
        </div>

        <div className="hand-section">
          <h3>Hand Cards</h3>
          <div className="hand-cards">
            {[1, 2, 3, 4].map(index => (
              <CardSlot
                key={index}
                card={cards[index]}
                index={index}
                onUpdateCard={updateCard}
                onClearCard={clearCard}
                ranks={ranks}
                suits={suits}
                suitSymbols={suitSymbols}
                isCardSelected={isCardSelected}
                label={`Card ${index}`}
              />
            ))}
          </div>
        </div>
      </div>

      <div className="controls">
        <div className="crib-toggle">
          <label>
            <input
              type="checkbox"
              checked={isCrib}
              onChange={(e) => setIsCrib(e.target.checked)}
            />
            <span className="crib-label">Crib Hand</span>
          </label>
        </div>

        <div className="buttons">
          <button
            className="score-button"
            onClick={calculateScore}
            disabled={!canCalculateScore() || isLoading}
          >
            {isLoading ? 'Calculating...' : 'Calculate Score'}
          </button>
          <button
            className="clear-button"
            onClick={clearAll}
          >
            Clear All
          </button>
        </div>
      </div>

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      <ScoreDisplay score={score} />
    </div>
  );
};

export default CribbageScorer;
