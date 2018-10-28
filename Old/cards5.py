import random

class Card(object):
    def __init__(self, suit, val):
        self.suit = suit
        self.value = val
       # self.realValue = rv

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

        return "{}{}".format(val, self.suit)

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
        for suit in ['H', 'C', 'D', 'S']:
            for val in range(1,14):
                self.cards.append(Card(suit, val))

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
        self.pickedCards = []

    def pickCard(self, num):
        card = self.hand[num-1]
        self.pickedCards.append(card)
        self.hand.pop(num-1)

        ## Sort (every time)

        for iter_num in range(len(self.pickedCards)-1,0,-1):
            #print "iter= ",iter_num
            #print len(self.hand)
            for idx in range(iter_num):
                # print idx
                #print "value=",self.getValue(self.hand[idx]),
                #print "card ", self.hand[idx]
                # print "idx=",self.getValue(self.hand[idx+1])
                if self.getValue(self.pickedCards[idx])>self.getValue(self.pickedCards[idx+1]):
                    temp = self.pickedCards[idx]
                    self.pickedCards[idx] = self.pickedCards[idx+1]
                    self.pickedCards[idx+1] = temp    


        return self


    def showPickedCards(self):
        for x in range(len(self.pickedCards)):
            card = str(self.pickedCards[x])
            #print len(card)
            if len(card)==2:
                suit = str(card)[1:]
                card = str(card)[:1]
               # print card
            else:
                suit = str(card)[2:]
                card = str(card)[:2]
               # print card
            #print suit

            ###symboler
            if suit == "H":
                print card + u'\u2665',
            elif suit == "D":
                print card + u'\u2666',
            elif suit == "C":
                print card + u'\u2663',
            elif suit == "S":
                print card + u'\u2660',
        print ""

        return self

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
        #print "{}'s hand: {}".format(self.name, self.hand)
        print "{}'s hand: ".format(self.name),
        #l = len(self.hand)

        for x in range(len(self.hand)):
            card = str(self.hand[x])
            #print len(card)
            if len(card)==2:
                suit = str(card)[1:]
                card = str(card)[:1]
               # print card
            else:
                suit = str(card)[2:]
                card = str(card)[:2]
               # print card
            #print suit

            ###symboler
            if suit == "H":
                print card + u'\u2665',
            elif suit == "D":
                print card + u'\u2666',
            elif suit == "C":
                print card + u'\u2663',
            elif suit == "S":
                print card + u'\u2660',

                #### Farger og slikt 
                #card = card + 
            #     # print cprint("test", 'red', 'on_white')
            #     print "\033[1;31;47m",card,
            #     #print colored(self.hand[x], 'red', 'on_white')

            # if suit == "S":
            #     print "\033[1;30;47m",card,

            #print self.hand[x],#
        print ""
        

        return self

    def sort(self):
        # Bubble sort

            for iter_num in range(len(self.hand)-1,0,-1):
                #print "iter= ",iter_num
                #print len(self.hand)
                for idx in range(iter_num):
                    # print idx
                    #print "value=",self.getValue(self.hand[idx]),
                    #print "card ", self.hand[idx]
                    # print "idx=",self.getValue(self.hand[idx+1])
                    if self.getValue(self.hand[idx])>self.getValue(self.hand[idx+1]):
                        temp = self.hand[idx]
                        self.hand[idx] = self.hand[idx+1]
                        self.hand[idx+1] = temp


    def getValue(self, card):
        # number = self.hand[num]
        # print number
        if len(str(card))==2:
            cardVal = str(card)[:1]
        else:
            cardVal = str(card)[:2]
    
        if  cardVal == "A":
            realValue = 14    
        elif cardVal == "J":
            realValue = 11
        elif cardVal == "Q":
            realValue = 12
        elif cardVal == "K":
            realValue = 13

        else:
            realValue = int(cardVal)
        return realValue
        #print val


    def showCard(self, num):
        #print self.hand[num]

        card = str(self.hand[num])
        if len(card)==2:
                suit = str(card)[1:]
                card = str(card)[:1]
               # print card
        else:
            suit = str(card)[2:]
            card = str(card)[:2]
           # print card
        #print suit

        if suit == "H":
            print card + u'\u2665',
        elif suit == "D":
            print card + u'\u2666',
        elif suit == "C":
            print card + u'\u2663',
        elif suit == "S":
            print card + u'\u2660',



    def discard(self, num):
        return self.hand.pop(num)


class Game(object):
    def __init__(self):
        self.players = []
        self.roundNum = 0
        #self.build()

    def joinGame(self, player):
        self.players.append(player)
        return self

    def getValue(self, card):
        # number = self.hand[num]
        # print number
        if len(str(card))==2:
            cardVal = str(card)[:1]
        else:
            cardVal = str(card)[:2]
    
        if  cardVal == "A":
            realValue = 14    
        elif cardVal == "J":
            realValue = 11
        elif cardVal == "Q":
            realValue = 12
        elif cardVal == "K":
            realValue = 13

        else:
            realValue = int(cardVal)
        return realValue
        #print val

    def playRound(self):
        self.roundNum =+1

        for x in range(len(self.players)):
            if x==0:
                text = raw_input(self.players[x].name+", how many cards do you want to Play? ")
                numberOfCards = int(text)

                for i in range(numberOfCards):
                    
                    text = raw_input(self.players[x].name+", what card number do you want to play?")
                    cardPick = int(text)
                    self.players[x].pickCard(cardPick)
                
                newLeader = 0
                self.players[x].showPickedCards()
            else:
                for y in range(numberOfCards):
                    text = raw_input(self.players[x].name+", what card number do you want to play?")
                    number2 = int(text)

                    self.players[x].pickCard(number2)
                oldLeader = newLeader
                newLeader = self.compareCards(x,oldLeader)
                self.players[x].showPickedCards()
        winner = newLeader 
        print self.players[winner].name, " wins this round!"



    def compareCards(self,newPlayer,oldPlayer):

        cardValuesOldPlayer = []
        for x in range(len(self.players[oldPlayer].pickedCards)):
            cardValuesOldPlayer.append(self.getValue(self.players[oldPlayer].pickedCards[x]))

        cardValuesNewPlayer = []
        for x in range(len(self.players[newPlayer].pickedCards)):
            cardValuesNewPlayer.append(self.getValue(self.players[newPlayer].pickedCards[x]))

        # print "old"
        # print cardValuesOldPlayer
        # print "new"
        # print cardValuesNewPlayer


        for x in range(len(cardValuesOldPlayer)):
            if cardValuesNewPlayer[x]>=cardValuesOldPlayer[x]:
                new = True
            else:
                new = False
                break

        if new:
            print self.players[newPlayer].name," beats " ,self.players[oldPlayer].name
            return newPlayer

        else:
            print self.players[oldPlayer].name," beats ", self.players[newPlayer].name
            return oldPlayer




# Test making a Deck
Deck = Deck()
Deck.shuffle()

Game = Game()


# deck.show()

Stian = Player("Stian")
Bob = Player("Bob")
Helge = Player("Helge")

Game.joinGame(Stian)
Game.joinGame(Bob)
Game.joinGame(Helge)

Bob.draw(Deck, 7)
Bob.sort()
Bob.showHand()

Stian.draw(Deck, 7)
Stian.sort()
Stian.showHand()

Helge.draw(Deck, 7)
Helge.sort()
Helge.showHand()

Game.playRound()

# Stian.pickCard(2)
# Bob.pickCard(3)
# Helge.pickCard(3)
Stian.showPickedCards()
Bob.showPickedCards()
Helge.showPickedCards()






### Discarding
# text = raw_input("How many cards to dicard?")
# number = int(text)

# for _ in range(number):
#     text = raw_input("")
#     discard = int(text)
#     Stian.discard(discard-1)
#     Stian.showHand()
#     print _
###

### Testing

# Test making a Card
# card = Card('Spades', 6)
# print card

### Print av "suits"
#print u'\u2660'
# u2665  u2666  u2663

#Stian.showCard(2)


#Stian.draw(Deck, number)
#Stian.sort()
#Stian.showHand()

#Stian.showHand()
#Stian.discard(0)

#Helge.draw(myDeck, 2)

#Helge.showHand()