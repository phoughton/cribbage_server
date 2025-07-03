import React, { useState } from 'react';

const CardSlot = ({ 
  card, 
  index, 
  onUpdateCard, 
  onClearCard, 
  ranks, 
  suits, 
  suitSymbols, 
  isCardSelected, 
  label 
}) => {
  const [showSelector, setShowSelector] = useState(false);
  const [selectedRank, setSelectedRank] = useState('');
  const [selectedSuit, setSelectedSuit] = useState('');

  const handleCardSelect = () => {
    if (selectedRank && selectedSuit) {
      onUpdateCard(index, { rank: selectedRank, suit: selectedSuit });
      setShowSelector(false);
      setSelectedRank('');
      setSelectedSuit('');
    }
  };

  const handleClear = () => {
    onClearCard(index);
    setShowSelector(false);
    setSelectedRank('');
    setSelectedSuit('');
  };

  const handleCancel = () => {
    setShowSelector(false);
    setSelectedRank('');
    setSelectedSuit('');
  };

  const getCardColor = (suit) => {
    return (suit === 'H' || suit === 'D') ? 'red' : 'black';
  };

  return (
    <div className="card-slot">
      <div 
        className={`card-display ${card ? 'filled' : 'empty'}`}
        onClick={() => setShowSelector(true)}
      >
        {card ? (
          <div className={`card-content ${getCardColor(card.suit)}`}>
            <div className="card-rank">{card.rank}</div>
            <div className="card-suit">{suitSymbols[card.suit]}</div>
          </div>
        ) : (
          <div className="empty-card">
            <span>+</span>
            <div className="card-label">{label}</div>
          </div>
        )}
      </div>

      {showSelector && (
        <div className="card-selector-overlay">
          <div className="card-selector">
            <div className="selector-header">
              <h4>Select {label}</h4>
              <button className="close-btn" onClick={handleCancel}>×</button>
            </div>

            <div className="rank-selection">
              <h5>Rank</h5>
              <div className="rank-grid">
                {ranks.map(rank => (
                  <button
                    key={rank}
                    className={`rank-btn ${selectedRank === rank ? 'selected' : ''}`}
                    onClick={() => setSelectedRank(rank)}
                  >
                    {rank}
                  </button>
                ))}
              </div>
            </div>

            <div className="suit-selection">
              <h5>Suit</h5>
              <div className="suit-grid">
                {suits.map(suit => (
                  <button
                    key={suit}
                    className={`suit-btn ${selectedSuit === suit ? 'selected' : ''} ${getCardColor(suit)}`}
                    onClick={() => setSelectedSuit(suit)}
                    disabled={selectedRank && isCardSelected(selectedRank, suit)}
                  >
                    {suitSymbols[suit]}
                  </button>
                ))}
              </div>
            </div>

            <div className="selector-actions">
              <button
                className="confirm-btn"
                onClick={handleCardSelect}
                disabled={!selectedRank || !selectedSuit || isCardSelected(selectedRank, selectedSuit)}
              >
                Select Card
              </button>
              {card && (
                <button className="clear-btn" onClick={handleClear}>
                  Clear
                </button>
              )}
              <button className="cancel-btn" onClick={handleCancel}>
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CardSlot;
