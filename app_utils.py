import errors


ranks_to_num = {"A": 1, "2": 2, "3": 3, "4": 4, "5": 5,
                "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
                "J": 11, "Q": 12, "K": 13}


def translate_card(card):

    if len(card) > 3:
        raise Exception("Error: Invalid card ID.")
    suit = card[-1]
    
    if len(card) == 3:
        rank = card[0:2]
    else:
        rank = card[0]
    
    return (ranks_to_num.get(rank), suit)

