import random
from collections import deque
from termcolor import colored, cprint

# Planer (for this edition)
# - Limit player possibilities
# - 3 rounds (or selectable)
# - fancy select cards (only possible cards)?
# - Write in player names


import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--open", help="increase output verbosity",
                    action="store_true")
args = parser.parse_args()
if args.open:
    blind = False
else:
    blind = True

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
        self.legalMoves = []

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

    def returnPickedCards(self):
        array = []
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
                array.append(card + u'\u2665')
            elif suit == "D":
                array.append(card + u'\u2666')
            elif suit == "C":
                array.append(card + u'\u2663')
            elif suit == "S":
                array.append(card + u'\u2660')
        empty = " "
        text = empty.join(array)
        return text

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
    def showHand(self, showLegal=False):

        showLegalMoves=[]

        if showLegal and Game.currentPlay:
            Game.getLegalMoves()
            showLegalMoves = Game.players[Game.currentPlayer].legalMoves
        else:
            #set all as legal
            for x in range(len(Game.players[Game.currentPlayer].hand)):
                showLegalMoves.append(1)

        print "{}'s hand: ".format(self.name)

        for x in range(len(self.hand)):

            #format quick fix
            if x == 0 and showLegal:
                print "",
            
            print "{}.[".format(x+1),
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

            print "]",
            
            if not showLegal:
                print ""

            else:
                if showLegalMoves[x] == 0:
                    print " ",
                    cprint(u'\u2022', "red")


                else:
                    print " ",
                    #print u'\u2020'
                    cprint(u'\u2022', "green")

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

        print "[",

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

        print "]",

    def discard(self, num):
        return self.hand.pop(num)

class Game(object):
    def __init__(self):
        self.players = []
        self.roundNumber = 0
        self.currentPlay = []
        self.cardValuesOfCurrentPlay = []
        self.currentPlayer = 0
        self.cardNrToBeat = 0
        self.numberOfPlayers = 0
        #self.SetUp()


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

    def getLegalMoves(self):
        #empty legalmoves[]
        self.players[self.currentPlayer].legalMoves = []

        #If there is a currentPlayList, all moves are legal
        if not self.currentPlay:
            for x in range(len(self.players[self.currentPlayer].hand)):
                self.players[self.currentPlayer].legalMoves.append(1)

        if len(self.currentPlay) == 1:
        #for the card to beat
        # Make array of illegal (0) and legal (1)
            for x in range(len(self.players[self.currentPlayer].hand)):
                if x == 0:
                    #lowest is always legal
                    self.players[self.currentPlayer].legalMoves.append(1)
                else:
                    playerCardValue = self.getValue(self.players[self.currentPlayer].hand[x])

                    if playerCardValue >= self.cardValuesOfCurrentPlay[0]:
                        self.players[self.currentPlayer].legalMoves.append(1)
                    else:
                        self.players[self.currentPlayer].legalMoves.append(0)
        #if length of currentPlay is more than one
        else:

            for x in range(len(self.players[self.currentPlayer].pickedCards)):
                if self.getValue(self.players[self.currentPlayer].pickedCards[x])>=self.cardValuesOfCurrentPlay[self.cardNrToBeat]:
                    ## and there is a bigger card in currentPlay
                    if len(self.currentPlay)>=self.cardNrToBeat+1:
                        if self.getValue(self.players[self.currentPlayer].pickedCards[x])<self.cardValuesOfCurrentPlay[self.cardNrToBeat+1]:
                            self.cardNrToBeat=+1

            for x in range(len(self.players[self.currentPlayer].hand)):
                if x == 0:
                    #lowest is always legal
                    self.players[self.currentPlayer].legalMoves.append(1)
                else:
                    playerCardValue = self.getValue(self.players[self.currentPlayer].hand[x])
                    if playerCardValue >= self.cardValuesOfCurrentPlay[self.cardNrToBeat]:
                        self.players[self.currentPlayer].legalMoves.append(1)
                    else:
                        self.players[self.currentPlayer].legalMoves.append(0)

    def rearrangePlayers(self, winner):
        winnerName = str(self.players[winner].name)
        self.players = deque(self.players)

        zeroPlayer = str(self.players[0].name)
        
        while winnerName!=zeroPlayer:
            self.players.rotate(1)
            zeroPlayer = str(self.players[0].name)

    def checkIfDoubleCards(self):
        for x in range(len(self.players[self.currentPlayer].hand)):
            for y in range(x+1,len(self.players[self.currentPlayer].hand)):
                if self.getValue(self.players[self.currentPlayer].hand[x])==self.getValue(self.players[self.currentPlayer].hand[y]):
                    return(True)
        return(False)

    def playRound(self):
        self.roundNum =+1

        for x in range(len(self.players)):
            self.currentPlayer = x
            self.cardNrToBeat = 0
            if x==0:

                nowHand = len(self.players[x].hand)
                if nowHand <= 1:
                    self.endGame()

                print ""
                if self.checkIfDoubleCards():
                    self.players[x].showHand(showLegal=True)
                    text = raw_input(self.players[x].name+", how many cards do you want to Play? ")
                    numberOfCardsToPlay = int(text)

                    
                else:

                    numberOfCardsToPlay = 1
                    atHand = len(self.players[x].hand) - 1

                atHand = len(self.players[x].hand) - numberOfCardsToPlay



                if atHand == 0:
                    for z in range(len(self.players)):
                        self.players[z].showHand()
                    self.endGame()

                for i in range(numberOfCardsToPlay):
                    text = raw_input(self.players[x].name+", what card number do you want to play?")
                    cardPick = int(text)
                    self.players[x].pickCard(cardPick)
                    self.players[x].showHand(showLegal=True)
                
                self.currentPlay = self.players[x].pickedCards
                self.cardValuesOfCurrentPlay = []
                for y in range(len(self.players[x].pickedCards)):
                    self.cardValuesOfCurrentPlay.append(self.getValue(self.currentPlay[y]))

        
                newLeader = 0

                if blind:
                    self.pause()
                    self.printBlind(50)
                
                print "{} plays".format(self.players[x].name),
                self.players[x].showPickedCards()
            else:
                
                print ""


                for y in range(numberOfCardsToPlay):
                    self.players[x].showHand(showLegal=True)
                    text = raw_input(self.players[x].name+", what card number do you want to play?")
                    number2 = int(text)

                    self.players[x].pickCard(number2)

                oldLeader = newLeader
                newLeader = self.compareTwo(x,oldLeader)

                self.currentPlay = self.players[newLeader].pickedCards
                self.cardValuesOfCurrentPlay = []
                for y in range(len(self.players[newLeader].pickedCards)):
                    self.cardValuesOfCurrentPlay.append(self.getValue(self.currentPlay[y]))


        self.currentPlay = []
        


        winner = newLeader 
        
        return winner

    def endGame(self):
        ##Compare value of hands.
        cardValues = []
        for x in range(len(self.players)):
            cardValues.append([])
            for y in range(len(self.players[x].hand)):
                cardValues[x].append(int(self.getValue(self.players[x].hand[y])))

        playerValue = []
        for x in range(len(cardValues)):
            playerValue.append(0)
            for y in range(len(cardValues[x])):
                playerValue[x]=playerValue[x]+cardValues[x][y]

        
        for x in range(len(playerValue)):
            if x==0:
                lowScore = playerValue[x]
                lowPlayer = 0
            else:
                if playerValue[x]<lowScore:
                    lowScore = playerValue[x]
                    lowPlayer=x

        # for x in range(len(playerValue)):
        #     print playerValue[x]
        print""

        for x in range(len(self.players)):
            self.players[x].showHand()

        print "{} wins the game!".format(self.players[lowPlayer].name)
        exit()

        return lowPlayer

    def compareTwo(self,newPlayer,oldPlayer):

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
            newCards = self.players[newPlayer].returnPickedCards()
            oldCards = self.players[oldPlayer].returnPickedCards()


            print "{}'s".format(self.players[newPlayer].name),
            print newCards,
            print "beat's {}'s".format(self.players[oldPlayer].name),
            print oldCards

            if blind:
                self.pause()
                self.printBlind(50)

            print "{}'s".format(self.players[newPlayer].name),
            print newCards,
            print "beat's {}'s".format(self.players[oldPlayer].name),
            print oldCards

            #print "{}'s {}' beat's {}'s {}".format(self.players[newPlayer].name, newCards, self.players[oldPlayer].name, oldCards) 

            #txt = "'\\u2665'"
            #print txt

            return newPlayer

        else:
            newCards = self.players[newPlayer].returnPickedCards()
            oldCards = self.players[oldPlayer].returnPickedCards()
            print "{}'s".format(self.players[oldPlayer].name),
            print oldCards,
            print "beat's {}'s".format(self.players[newPlayer].name),
            print newCards

            if blind:
                self.pause()                
                self.printBlind(50)

            print "{}'s".format(self.players[oldPlayer].name),
            print oldCards,
            print "beat's {}'s".format(self.players[newPlayer].name),
            print newCards



            return oldPlayer

    def trashCards(self):
        for x in range(len(self.players)):
            for y in range(len(self.players[x].pickedCards)):
                #print y
                self.players[x].pickedCards.pop()

        #print self.players[0].pickedCards[1]

    def printBlind(self,rader):
        for r in range(0,rader):
            print ""

    def pause(self):
        print ""
        print "Press enter when next player is ready..."
        text = raw_input("")

    def topCard(self):
        print "Top card: "
        print ""

        for x in range(len(self.players)):
            self.players[x].firstCard = self.getValue(self.players[x].hand[6])
            self.players[x].sort()

            print self.players[x].name,
            self.players[x].showCard(6)
            print ""

            if not blind:
                self.players[x].showHand()

        highest = 0
        for z in range(len(self.players)):
            if self.players[z].firstCard > highest:
                highest = self.players[z].firstCard
                highestPlayer = z

        print ""
        print "{} begins!".format(self.players[highestPlayer].name)

        self.rearrangePlayers(highestPlayer)            

    def discardRound(self):

        zero = False
        for x in range(len(self.players)):

            if blind:
                self.pause()
                self.printBlind(50)

            self.players[x].showHand()

            if x==0:

                print ""
                discardsText = raw_input(self.players[x].name+", how many cards do you want to discard? ")
                discards = int(discardsText)

                if discards == 0:
                    zero = True
                    break

                for y in range(0,discards):
                    discardText = raw_input(self.players[x].name+", what card number do you want to discard? ")
                    discard = int(discardText)
                    self.players[x].discard(discard-1)
                self.players[x].draw(Deck, discards)
                self.players[x].sort()
                self.players[x].showHand()

            else:

                print ""

                for y in range(0,discards):
                    #self.players[x].showHand()
                    discardText = raw_input(self.players[x].name+", what card number do you wnat to discard? ")
                    discard = int(discardText)
                    self.players[x].discard(discard)
                    self.players[x].showHand()
                self.players[x].draw(Deck, discards)
                self.players[x].sort()
                self.players[x].showHand()


        if blind and not zero:
            self.pause()
            self.printBlind(50)

    def playGame(self):
        
        print "=== A game of Gurka ==="
        print ""

        for x in range(len(self.players)):
            self.players[x].draw(Deck, 7)

        self.topCard()
        self.discardRound()


        inGame = True
        while inGame:
            roundWinner = self.playRound()
            print self.players[roundWinner].name, " wins this round!"
            print""
            self.trashCards()
            self.rearrangePlayers(roundWinner)


            if not blind:
                for y in range(len(self.players)):
                    self.players[y].showHand()

            x=x+1

        winner = self.endGame()

    # def setSettings():
        #text = raw_input("How many players?")
        #number = int(text)




# Test making a Deck
Deck = Deck()
Deck.shuffle()
Game = Game()


# deck.show()

Helge = Player("Helge")
Stian = Player("Stian")
Ida = Player("Ida")

Game.joinGame(Helge)
Game.joinGame(Stian)
Game.joinGame(Ida)

Game.playGame()