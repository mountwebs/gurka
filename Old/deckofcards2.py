import random

class Card(object):
    def __init__(self, suit, val, rv):
        self.suit = suit
        self.value = val
        self.realValue = rv

    # Implementing build in methods so that you can print a card object
    def __unicode__(self):
        return self.show()
    def __str__(self):
        return self.show()
    def __repr__(self):
        return self.show()
        
    def show(self):
        if self.value == 1:
            val = "A"
        elif self.value == 11:
            val = "J"
        elif self.value == 12:
            val = "Q"
        elif self.value == 13:
            val = "K"
        else:
            val = self.value

        return "{} of {}".format(val, self.suit)

        # return "{} of {}, {}".format(val, self.suit, self.realValue)

    #def showValue(self)
    #    return "{}".format(self.value)

    # def value(self)
    #    return self.value 


class Deck(object):
    def __init__(self):
        self.cards = []
        self.build()

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            print card.show()

    # Generate 52 cards
    def build(self):
        self.cards = []
        for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in range(1,14):
                self.cards.append(Card(suit, val, val))

    # Shuffle the deck
    def shuffle(self, num=1):
        length = len(self.cards)
        for _ in range(num):
            # This is the fisher yates shuffle algorithm
            for i in range(length-1, 0, -1):
                randi = random.randint(0, i)
                if i == randi:
                    continue
                self.cards[i], self.cards[randi] = self.cards[randi], self.cards[i]
            # You can also use the build in shuffle method
            # random.shuffle(self.cards)

    # Return the top card
    def deal(self):
        return self.cards.pop()


class Player(object):
    def __init__(self, name):
        self.name = name
        self.hand = []

    # Draw n number of cards from a deck
    # Returns true in n cards are drawn, false if less then that
    def draw(self, deck, num=1):
        for _ in range(num):
            card = deck.deal()
            if card:
                self.hand.append(card)
            else: 
                return False
        return True

    # Display all the cards in the players hand
    def showHand(self):
        print "{}'s hand: {}".format(self.name, self.hand)
        return self

    def showCard(self, num):
        print self.hand[num]

    def discard(self, num):
        return self.hand.pop(num)




    #def discard(num):
    #    return self.hand.pop()


# Test making a Card
# card = Card('Spades', 6)
# print card

### Print av "suits"
#print u'\u2660'
# u2665  u2666  u2663

# Test making a Deck
Deck = Deck()
Deck.shuffle()

# deck.show()

Stian = Player("Stian")
Helge = Player("Helge")

Stian.draw(Deck, 50)
Helge.draw(Deck, 1)
Deck.show()

#Stian.showHand()
#Stian.discard(0)


#Helge.draw(myDeck, 2)

#Helge.showHand()


