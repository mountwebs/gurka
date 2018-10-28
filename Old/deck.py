from random import randint
def card_deck():
    #sets the card types and values
    card_value = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    card_type = ['Hearts','Spades','Clubs','Diamonds']
    deck = []
    #This iterates all 52 cards into a deck
    for i in card_type:
        for j in card_value:
            deck.append(j + ' of ' + i)
    return deck

new_deck = card_deck()
for x in new_deck:
	print(x)
