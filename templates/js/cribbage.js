'use strict';

const e = React.createElement;

class LikeButton extends React.Component {
  constructor(props) {
    super(props);
    this.state = { liked: false };
  }

  render() {
    if (this.state.liked) {
      return `Card Suit: ${this.props.commentID}`;
    }

    return e(
      'button',
      { onClick: () => this.setState({ liked: true }) },
      `${this.props.commentID}`
    );
  }
}

// Find all DOM containers, and render Like buttons into them.
document.querySelectorAll('.suit_container')
  .forEach(domContainer => {
    // Read the comment ID from a data-* attribute.
    const cardSuit = domContainer.dataset.card_suit;
    ReactDOM.render(
      e(LikeButton, { commentID: cardSuit }),
      domContainer
    );
  });