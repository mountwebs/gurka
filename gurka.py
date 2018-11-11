import random
from random import randint
from collections import deque
from termcolor import colored, cprint
import argparse
import textwrap

# Plans (for this edition)
# - Limit player possibilities
# - 3 rounds (or selectable)
# - fancy select cards (only possible cards)?

# Missing feature: ending with two or more cards?
# Missing feature two players wins the round


parser = argparse.ArgumentParser(
     formatter_class=argparse.RawDescriptionHelpFormatter,
     description=textwrap.dedent('''\
The card game Gurka, written in Python.
--------------------------------

         '''))
parser = argparse.ArgumentParser()
parser.add_argument("-o", "--open", help="Everyone can see everyones cards",
                    action="store_true")
parser.add_argument("-m", "--many", help="First player can always play many cards, regardless of wether s/he has double cards.",
                    action="store_true")
parser.add_argument("-nd", "--noDiscard", help="Skip Discard Round",
                    action="store_true")
parser.add_argument("-t", "--test", help="Testing",
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

class Deck(object):
    def __init__(self, num):
        self.cards = []
        self.deckNr = num
        self.build()
        

    # Display all cards in the deck
    def show(self):
        for card in self.cards:
            print card.show()

    # Generate 52 cards
    def build(self):
        for x in range(self.deckNr):
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

    def removeDeck(self):
        self.cards = []
        return self

    def newDeck(self,num=1):
        for _ in range(num):
            self.build()

    # Return the top card
    def deal(self):
        return self.cards.pop()

class Player(object):
    def __init__(self, name, isBot=False):
        self.name = name
        self.hand = []
        self.pickedCards = []
        self.legalMoves = []
        self.score = 0;
        self.isBot = isBot

    def sortPickedCards(self):
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

    def pickCard(self, num):
        card = self.hand[num-1]
        self.pickedCards.append(card)
        self.hand.pop(num-1)

        self.sortPickedCards()

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
        elif showLegal:
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

    def getOptions(self, plusOne=False):
        options = []
        if plusOne:
            for _ in range(len(self.legalMoves)):
                        if self.legalMoves[_] == 1:
                            _ = _ +1
                            options.append(_)
        else:
            for _ in range(len(self.legalMoves)):
                        if self.legalMoves[_] == 1:
                            options.append(_)

        return options

    def botPickCardRandom(self, num, legal=False):
        
        # self.showHand()
        # print self.legalMoves
        if legal:
            for x in range(num):
                Game.getLegalMoves()
                options = []
                options = self.getOptions()

                # for _ in range(len(self.legalMoves)):
                #     if self.legalMoves[_] == 1:
                #         options.append(_)

                cardOpt = randint(1, len(options))
                cardNr = options[cardOpt-1]
                TheCard = self.hand[cardNr]
                self.pickedCards.append(TheCard)
                self.hand.pop(cardNr)

                # self.showHand()
                # print self.legalMoves
                # print options
                # print cardOpt
                # print cardNr
                # print self.pickedCards

        else: 
            for x in range(num):
                cardNr = randint(1, len(self.hand))
                #print cardNr

                TheCard = self.hand[cardNr-1]
                self.pickedCards.append(TheCard)
                self.hand.pop(cardNr-1)

        self.sortPickedCards()
 
        return self

    def botRandomDiscards(self, num):
        for x in range(num):
            hand.pop(num)


class Game(object):
    def __init__(self):
        self.players = []
        self.roundNumber = 0
        self.currentPlay = []
        self.cardValuesOfCurrentPlay = [] 
        self.currentPlayer = 0
        self.cardNrToBeat = 0
        self.numberOfPlayers = 0
        self.numberOfRounds = 0
        self.decks = 1
        #self.setUp()

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

        while True:

            for x in range(len(self.players)):
                self.currentPlayer = x
                self.cardNrToBeat = 0

                if self.players[x].isBot and x==0:

                    nowHand = len(self.players[x].hand)
                    if nowHand <= 1:
                        return

                    #Skipping double cards for now

                    numberOfCardsToPlay = 1
                    atHand = len(self.players[x].hand) - numberOfCardsToPlay

                    if atHand == 0:
                        return

                    self.currentPlay = self.players[x].pickedCards
                    self.cardValuesOfCurrentPlay = []

                    ## Pick cards
                    self.players[self.currentPlayer].botPickCardRandom(numberOfCardsToPlay)

                    ## Add cardValues
                    for y in range(len(self.players[x].pickedCards)):
                        self.cardValuesOfCurrentPlay.append(self.getValue(self.currentPlay[y]))

                    self.currentPlay = self.players[x].pickedCards
                    self.cardValuesOfCurrentPlay = []
                    for y in range(len(self.players[x].pickedCards)):
                        self.cardValuesOfCurrentPlay.append(self.getValue(self.currentPlay[y]))
            
                    newLeader = 0

                    print "{} plays".format(self.players[x].name),
                    self.players[x].showPickedCards()

                elif self.players[x].isBot:

                    ### Pick Cards
                    self.players[self.currentPlayer].botPickCardRandom(numberOfCardsToPlay, legal=True)

                    print "{} plays".format(self.players[x].name),
                    self.players[x].showPickedCards()

                    oldLeader = newLeader
                    newLeader = self.compareTwo(x,oldLeader)


                    self.currentPlay = self.players[newLeader].pickedCards
                    self.cardValuesOfCurrentPlay = []
                    for y in range(len(self.players[newLeader].pickedCards)):
                        self.cardValuesOfCurrentPlay.append(self.getValue(self.currentPlay[y]))

                    

                elif x==0:
                    nowHand = len(self.players[x].hand)
                    if nowHand <= 1:
                        return

                    print ""
                    if self.checkIfDoubleCards() or args.many:
                        self.players[x].showHand(showLegal=True)
                        string = self.players[x].name+", how many cards do you want to Play? "
                        text = askPlayer(string, integer=True, between=[1,len(self.players[self.currentPlayer].hand)])
                        numberOfCardsToPlay = int(text)

                    else:

                        numberOfCardsToPlay = 1

                    atHand = len(self.players[x].hand) - numberOfCardsToPlay

                    if atHand == 0:
                        return

                    for i in range(numberOfCardsToPlay):
                        if not self.checkIfDoubleCards():
                            self.players[x].showHand(showLegal=True)
                        string = self.players[x].name+", what card number do you want to play? "
                        text = askPlayer(string,)
                        cardPick = int(text)
                        self.players[x].pickCard(cardPick)
                        if self.checkIfDoubleCards():
                            self.players[x].showHand(showLegal=True)
                    
                    self.currentPlay = self.players[x].pickedCards
                    self.cardValuesOfCurrentPlay = []
                    for y in range(len(self.players[x].pickedCards)):
                        self.cardValuesOfCurrentPlay.append(self.getValue(self.currentPlay[y]))

            
                    newLeader = 0

                    #If blind or next player is bot...
                    if blind and not (self.nextPlayerIsBot() or self.players[self.currentPlayer].isBot) and len(self.players)>x+1:
                        self.pause()
                        self.printBlind(50)
                    
                    print "{} plays".format(self.players[x].name),
                    self.players[x].showPickedCards()

                else:
                    
                    print ""


                    for y in range(numberOfCardsToPlay):
                        self.players[x].showHand(showLegal=True)
                        string = self.players[x].name+", what card number do you want to play? "
                        self.getLegalMoves()
                        options= self.players[self.currentPlayer].getOptions(plusOne=True)
                        text = askWhatCard(string, options)
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

            print self.players[winner].name + " wins this round!"
            print""


            
            self.trashCards()
            self.rearrangePlayers(winner)


            if not blind:
                for y in range(len(self.players)):
                    self.players[y].showHand()

    def nextPlayerIsBot(self):
        try:
            if self.players[self.currentPlayer + 1].isBot:
                return True
            else:
                return False
        except:
            pass

        return False

    def endRound(self):
        ##Compare value of hands.
        cardValues = []
        winners = []

        for x in range(len(self.players)):
            cardValues.append([])
            for y in range(len(self.players[x].hand)):
                cardValues[x].append(int(self.getValue(self.players[x].hand[y])))

        playerRoundScore = []
        for x in range(len(cardValues)):
            playerRoundScore.append(0)
            for y in range(len(cardValues[x])):
                playerRoundScore[x]=playerRoundScore[x]+cardValues[x][y]

        minValue = min(playerRoundScore)
        
        for x in range(len(playerRoundScore)):
            if playerRoundScore[x] == minValue:
                winners.append(x)
            # if x==0:
            #     lowScore = playerRoundScore[x]
            #     lowPlayer = 0
            # else:
            #     if playerRoundScore[x]<lowScore:
            #         lowScore = playerRoundScore[x]
            #         lowPlayer=x


        print""

        for x in range(len(self.players)):
            self.players[x].showHand()

        print ""

        for x in range(len(self.players)):
            for y in range(len(winners)):
                if x == winners[y]:
                    playerRoundScore[x] = 0

            self.players[x].score = self.players[x].score + playerRoundScore[x]
            print "{}'s score is {} this round and {} in total ".format(self.players[x].name, playerRoundScore[x], self.players[x].score)

        print ""

        if len(winners) > 1:
            print "Winners of this round:"
            for y in range(len(winners)):
                print self.players[winners[y]].name

        else:
            print "{} wins this round!".format(self.players[winners[0]].name)

        return

    def endGame(self):
        scores = []
        winners = []
        
        for x in range(len(self.players)):
            scores.append(self.players[x].score)

        minValue = min(scores)

        for x in range(len(scores)):
            if self.players[x].score == minValue:
                winners.append(x)

        # for x in range(len(self.players)):
        #     if x==0:
        #         lowScore = self.players[x].score
        #         lowPlayer = x
        #     else:
        #         if self.players[x]<lowScore:
        #             lowScore = self.players[x].score
        #             lowPlayer=x
        print ""

        if len(winners) > 1:
            print "Winners of the Game! :"
            for y in range(len(winners)):
                print self.players[winners[y]].name
        else:
            print "{} wins the game!".format(self.players[winners[0]].name)

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

            if blind and not (self.nextPlayerIsBot() or self.players[self.currentPlayer].isBot):
                self.pause()
                self.printBlind(50)

            if not self.nextPlayerIsBot() and self.nrOfHumanPlayers()>=2:
                print "{}'s".format(self.players[newPlayer].name),
                print newCards,
                print "beats {}'s".format(self.players[oldPlayer].name),
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

            if blind and not self.nextPlayerIsBot() and not self.players[self.currentPlayer].isBot:
                self.pause()                
                self.printBlind(50)

            if not self.nextPlayerIsBot() and self.nrOfHumanPlayers()>=2:
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

    def pause(self, newRound=False):

        if newRound:
            print ""
            print "Press enter to begin new round..."
            text = raw_input("")

        else:
            print ""
            print "Press enter when next player is ready..."
            text = raw_input("")

    def topCard(self):
        print "Top card: "
        print ""

        firstCardValue = []

        for x in range(len(self.players)):
            firstCardValue.append(self.getValue(self.players[x].hand[6]))

            print self.players[x].name,
            self.players[x].showCard(6)
            print ""

            self.players[x].sort()

            if not blind:
                self.players[x].showHand()

        highestPlayer = max(xrange(len(firstCardValue)), key=firstCardValue.__getitem__)

        # highest = 0
        # for z in range(len(self.players)):
        #     if self.getValue(self.players[z].firstCard) > highest:
        #         highest = self.getValue(self.players[z].firstCard)

        #         highestPlayer = z

        print ""
        print "{} begins!".format(self.players[highestPlayer].name)

        self.rearrangePlayers(highestPlayer)            

    def discardRound(self):
        zero = False
        for x in range(len(self.players)):
            self.currentPlayer = x

            if self.players[x].isBot and x == 0:
                discards = randint(0, len(self.players[self.currentPlayer].hand))
                for _ in range(discards):
                    discard = randint(1, len(self.players[self.currentPlayer].hand))
                    self.players[x].discard(discard-1)
                self.players[x].draw(Deck, discards)
                self.players[x].sort()

                print "{} discards {} cards".format(self.players[self.currentPlayer].name, discards)
                print ""

            elif self.players[x].isBot:
                for _ in range(discards):
                    discard = randint(1, len(self.players[self.currentPlayer].hand))
                    self.players[x].discard(discard-1)
                self.players[x].draw(Deck, discards)
                self.players[x].sort()

            ### if Human player
            else:

                # if blind and self.nrOfHumanPlayers()>1:
                #     self.pause()
                #     self.printBlind(50)


                self.players[x].showHand()

                if x==0:

                    print ""
                    #discardsText = raw_input(self.players[x].name+", how many cards do you want to discard? ")
                    discards = askPlayer(self.players[x].name+", how many cards do you want to discard? ", integer=True, between=[0,7])


                    if discards == 0:
                        zero = True
                        break

                    for y in range(0,discards):
                        discard = askPlayer(self.players[x].name+", what card number do you want to discard? ", integer=True, between=[1,len(self.players[x].hand)])
                        #discardText = raw_input(self.players[x].name+", what card number do you want to discard? ")
                        #discard = int(discardText)
                        self.players[x].discard(discard-1)
                        self.players[x].showHand()
                    self.players[x].draw(Deck, discards)
                    self.players[x].sort()
                    self.players[x].showHand()

                else:

                    print ""

                    #discardText = raw_input(self.players[x].name+", do you want to discard 0 or {} cards? ".format(discards))
                    string = self.players[x].name+", do you want to discard 0 or {} cards? ".format(discards)
                    wannaDiscard = askPlayer(string, arrayOfInts=[0,discards], integer=True)

                    if wannaDiscard>0:
                        for y in range(0,discards):
                            #self.players[x].showHand()
                            #discardText = raw_input(self.players[x].name+", what card number do you want to discard? ")
                            #discard = int(discardText)
                            discard = askPlayer(self.players[x].name+", what card number do you want to discard? ", integer=True, between=[1,len(self.players[x].hand)])
                            self.players[x].discard(discard-1)
                            self.players[x].showHand()
                        self.players[x].draw(Deck, discards)
                        self.players[x].sort()
                        self.players[x].showHand()

            if blind and not (self.nextPlayerIsBot() or self.players[self.currentPlayer].isBot):
                self.pause()
                self.printBlind(50)

    def scratch(self):
        for x in range(len(self.players)):
            self.players[x].hand = []
            self.players[x].pickedCards = []
            self.players[x].legalMoves = []

        self.currentPlay = []
        self.cardValuesOfCurrentPlay = []
        self.currentPlayer = 0
        self.cardNrToBeat = 0        

    def playGame(self):
        print "=== A game of Gurka ==="
        print ""

        for roundNr in range(self.numberOfRounds):
            #How many decks?
            Deck.removeDeck()
            Deck.newDeck(self.decks)
            Deck.shuffle()

            for x in range(len(self.players)):
                self.players[x].draw(Deck, 7)

            self.topCard()

            if not args.noDiscard:
                self.discardRound()

            self.playRound()
            if (self.numberOfRounds - roundNr)>1:
                self.endRound()
                self.pause(newRound=True)
                self.scratch()
            else:
                self.endRound()
                self.endGame()
                exit()
            #x=x+1

        #winner = self.endGame()

    def setUp(self):
        rounds=askPlayer("How many rounds do you want to play? ", integer=True, over=0)
        #rounds = raw_input("How many rounds do you want to play? ")
        self.numberOfRounds = int(rounds)
        while True:
            nrOfBots = askPlayer("How many bots? ", integer=True)
            nrOfBots = int(nrOfBots)
            for _ in range(nrOfBots):
                int_ = _+ 1
                str_ = str(int_)
                bot = "bot" + str_
                newBot = Player(bot, isBot=True)
                self.players.append(newBot)

            nrOfPlayers = askPlayer("How many players? ", integer=True)
            nrOfPlayers = int(nrOfPlayers)
            if (nrOfBots + nrOfPlayers) >= 2:
                break
            else:
                print "There has to be at least two players"

        names = []
        for x in range(nrOfPlayers):
            string = "What is the name of player {}? ".format(x+1)
            name = askPlayer(string)
            name = str(name)
            newPlayer = Player(name)
            self.players.append(newPlayer)

        self.decks = 1 + len(self.players)/3

    def nrOfHumanPlayers(self):
        nrOfHumanPlayers = 0
        for x in range(len(self.players)):
            if not self.players[x].isBot:
                nrOfHumanPlayers = nrOfHumanPlayers + 1

        return nrOfHumanPlayers

def askPlayer(keys, integer=False, between=[], over=-1, arrayOfInts=[]):
    if integer:
        string=False
    else:
        string=True
    
    while True:  
        try:
            if integer or between or over> -1:
                out = int(raw_input(keys))
            elif string:
                out = str(raw_input(keys))
        except:
            print "Does not compute... Try again."
            print ""
            continue

        if string and not out:
            print "Does not compute... Try again."
            continue
        if between:
            if out>=between[0] and out<=between[1]:
                return out
            else:
                print "The number has to be between {} and {}".format(between[0], between[1])
                continue

        elif arrayOfInts:
            rightNumber = False
            for _ in range(len(arrayOfInts)):
                if arrayOfInts[_] == out:
                    return out
            
            print "Does not compute... Try again."
            continue

        elif over > -1:
            if out>over:
                return out
            else:
                print "The number has to be bigger then {}".format(over)
                continue
        else:
            break



        
    return out


    # def createBots(self, num):
        #botNames = [GRTA, Terminator, Bot]
        #for _ in range(num):

def askWhatCard(keys,array):
    while True:
        try:
            out = int(raw_input(keys))
        except:
            print "Does not compute... Try again."
            continue
        inArray = False
        for _ in range(len(array)):
            if out == array[_]:
                return out
        
        print "Not a legal move... Try again."
        print ""



### Setup
Deck = Deck(1)
Deck.shuffle()
Game = Game()

if args.test:
    GRTA = Player("GRTA", isBot=True)
    Game.joinGame(GRTA)
    GRTA.draw(Deck, 7)
    GRTA.sort()
    GRTA.showHand()
    Terminator = Player("Terminator", isBot=True)
    Game.joinGame(Terminator)
    Terminator.draw(Deck, 7)
    Terminator.sort()
    Terminator.showHand()
    Game.playGame()


else:
    Game.setUp()
    Game.playGame()



# deck.show()

## REPL Test
# from gurka import Card, Deck, Player, Game
# Deck = Deck(1)
# Deck.shuffle()
# Game = Game()



