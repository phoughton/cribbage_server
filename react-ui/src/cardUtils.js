// Utility functions for card translation and formatting

/**
 * Translates a card rank number to its readable name
 * @param {number} rank - The card rank (1-13)
 * @returns {string} - The readable rank name
 */
export const translateRank = (rank) => {
  const rankMap = {
    1: 'Ace',
    2: '2',
    3: '3',
    4: '4',
    5: '5',
    6: '6',
    7: '7',
    8: '8',
    9: '9',
    10: '10',
    11: 'Jack',
    12: 'Queen',
    13: 'King'
  };
  
  return rankMap[rank] || rank.toString();
};

/**
 * Translates a suit letter to its readable name
 * @param {string} suit - The suit letter (H, D, C, S)
 * @returns {string} - The readable suit name
 */
export const translateSuit = (suit) => {
  const suitMap = {
    'H': 'Hearts',
    'D': 'Diamonds',
    'C': 'Clubs',
    'S': 'Spades'
  };
  
  return suitMap[suit] || suit;
};

/**
 * Translates a card tuple to readable format
 * @param {number} rank - The card rank
 * @param {string} suit - The suit letter
 * @returns {string} - The readable card name (e.g., "5 of Hearts")
 */
export const translateCard = (rank, suit) => {
  return `${translateRank(rank)} of ${translateSuit(suit)}`;
};

/**
 * Parses and translates card tuples in scoring messages
 * @param {string} message - The scoring message containing card tuples
 * @returns {string} - The message with translated card names
 */
export const translateCardsInMessage = (message) => {
  if (!message) return message;
  
  // Regex to match card tuples like (5, 'D') or (11, 'H')
  const cardTupleRegex = /\((\d+),\s*'([HDCS])'\)/g;
  
  return message.replace(cardTupleRegex, (match, rank, suit) => {
    const rankNum = parseInt(rank, 10);
    return translateCard(rankNum, suit);
  });
};

/**
 * Parses and translates card arrays in scoring messages
 * @param {string} message - The scoring message containing card arrays
 * @returns {string} - The message with translated card names
 */
export const translateCardArraysInMessage = (message) => {
  if (!message) return message;
  
  // First translate individual card tuples
  let translatedMessage = translateCardsInMessage(message);
  
  // Then clean up the array brackets and formatting
  // Replace patterns like [5 of Hearts, Jack of Hearts] to be more readable
  translatedMessage = translatedMessage.replace(/\[([^\]]+)\]/g, (match, cardList) => {
    // Clean up any extra spaces and format nicely
    const cleanedList = cardList.replace(/,\s+/g, ', ');
    return `[${cleanedList}]`;
  });
  
  return translatedMessage;
};
