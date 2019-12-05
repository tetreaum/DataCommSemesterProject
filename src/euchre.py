"""
A class to hold all of our game logic. It's very loosely based on how the tutorial below
has their game logic for rock paper scissors. However, our game is much more complex and
we wrote all of the game logic ourselves.
https://techwithtim.net/tutorials/python-online-game-tutorial/online-rock-paper-scissors-p1/
For cards, the first digit is the card value, and the second digit is the suit

NINE = 1
TEN = 2
JACK = 3
QUEEN = 4
KING = 5
ACE = 6

CLUBS = 0
DIAMONDS = 1
HEARTS = 2
SPADES = 3
"""
import random


class Euchre:
    def __init__(self):
        self.dealingPhase = True  # set to this at the start
        self.choosingTrumpPhase1 = False  # 
        self.choosingTrumpPhase2 = False
        self.discardPhase = False
        self.playingCardsPhase = False
        self.gameEnd = False
        self.turn = 0  # Iterate in playCard, keeps track of whose playing
        self.ready = True  # When all players have redied up
        self.moves = {}  # A list of the moves that have been played
        self.scores = [0, 0]
        self.players = {}  # A list of players and their hands
        self.dealer = -1  # The current dealer (set in deal)
        self.leader = 0  # The player who will play first
        self.trump = 0  # The current trump suit
        self.team1Score = 0  # The current score for team one
        self.team2Score = 0  # The current score for team two
        self.winner = -1
        self.cards = [10, 11, 12, 13, 20, 21, 22, 23, 30, 31, 32, 33, 40, 41, 42, 43, 50, 51, 52, 53, 60, 61, 62, 63]  # All the cards in the deck
        self.suits = [0, 1, 2, 3]
        self.kitty = 0

    # add a player to the dictionary with an empty list as their value (called when first connecting)
    def addPlayer(self, player):
        self.players[player] = []

    # A class to handle dealing the cards to each person's "hand" in the dictionary
    # It shuffles the cards at the start and gives a copy of the cards to the player's hand.
    # The last 4 cards are the kitty
    # The list will still be full after the players have their cards
    def deal(self):
        self.dealer = (self.dealer + 1) % 4
        self.turn = (self.dealer + 1) % 4
        random.shuffle(self.cards)
        counter = 0  # The place in the deck
        for hand in self.players:  # For each player
            self.players[hand].clear()  # removes the last hand
            for i in range(0, 5):  # Adds 5 cards
                self.players[hand].append(self.cards[counter])  # Add a card to their hand
                counter = counter + 1  # Move the place in the deck along one
        self.kitty = self.cards[20]
        self.dealingPhase = False
        self.choosingTrumpPhase1 = True

    # A helper method to build tempCardsInHand for gameStateBuilder
    def buildTempCardsInHand(self, playerNum):
        counter = 1
        tempCardsInHand = self.getCardSuitText(self.trump)
        for card in self.players[playerNum]:
            tempCardsInHand = tempCardsInHand + "\n" + str(counter) + ": " + self.getCardText(card) + " of " + self.getCardSuitText(card)
            counter = counter + 1
        return tempCardsInHand

    # A helper method to build tempCardsInHand for gameStateBuilder
    def buildCardsInHandAndSuitOptions(self, playerNum):
        tempCardsInHand = self.buildTempCardsInHand(playerNum)
        tempSuits = []
        tempSuitsString = ""
        counter = 1
        for suit in self.suits:
            if suit != self.getCardSuit(self.kitty):
                tempSuits.append(suit)
        for suit in tempSuits:
            tempSuitsString = tempSuitsString + "\n" + str(counter) + ": " + self.getCardSuitText(suit)
            counter = counter + 1
        return tempCardsInHand + "\nOptions: " + tempSuitsString + "\n4: Pass"

    # A helper method to build tempCardsOnTable for gameStateBuilder
    def buildTempCardsOnTable(self):
        tempCardsOnTable = ""
        for move in self.moves:
            tempCardsOnTable = tempCardsOnTable + "\nPlayer " + str(move) + ": played the " + self.getCardText(self.moves[move]) + " of " + self.getCardSuitText(self.moves[move])
        return tempCardsOnTable

    def gameLoop(self, option):
        if self.dealingPhase:
            self.deal()
        elif self.choosingTrumpPhase1:
            self.pickTrumpStage1(self.turn, option)
            if option == "1":
                self.choosingTrumpPhase1 = False
                self.discardPhase = True
            else:
                self.iterateTurn()
                if self.turn == (self.dealer + 1) % 4:
                    self.choosingTrumpPhase1 = False
                    self.choosingTrumpPhase2 = True
        elif self.discardPhase:
            self.discard(self.dealer, int(option))
        elif self.choosingTrumpPhase2:
            if option != "4":
                self.pickTrumpStage2(self.turn, int(option))
            else:
                self.iterateTurn()
                if self.turn == (self.dealer + 1) % 4:
                    self.deal()
                else:
                    pass
        elif self.playingCardsPhase:
            if self.leader == (self.turn + 1) % 4:
                self.playCard(self.turn, int(option))
                winner = self.scoreTrick(self.moves[0], self.moves[1], self.moves[2], self.moves[3])
                if winner == 0 or winner == 2:
                    self.scores[0] = self.scores[0] + 1
                elif winner == 1 or winner == 3:
                    self.scores[1] = self.scores[1] + 1
                else:
                    print("Scoring tricks is broken (line 131ish in gameloop)")
                if self.scores[0] + self.scores[1] == 5:
                    if self.scores[0] > self.scores[1]:
                        self.team1Score = self.team1Score + 1
                    elif self.scores[0] < self.scores[1]:
                        self.team2Score = self.team2Score + 1
                    self.scores = [0, 0]
                    self.playingCardsPhase = False
                    self.dealingPhase = True
                else:
                    pass  # do nothing the hand isn't done yet
            else:
                self.playCard(self.turn, int(option))
        self.checkWinner()

    # builds the current information of the game so the player can use that to think
    def gameStateBuilder(self, playerNumber, broadcast):
        turnString = ""
        if not broadcast:
            turnString = "YOUR TURN:\n\n"
        if self.dealingPhase:  # Should never send anything
            return "This text should never appear (See gameStateBuilder in euchre)"
        # Call buildTempCardsInHand to show player what their hand is when choosing trump in phase 1. Gives them a yes or no option
        elif self.choosingTrumpPhase1:
            tempCardsInHand = ""
            tempCardsInHand = self.buildTempCardsInHand(playerNumber)
            return turnString + \
                "Team One Score: " + str(self.team1Score) + " Team Two Score: " + str(self.team2Score) + \
                "\nKitty: " + self.getCardText(self.kitty) + " of " + self.getCardSuitText(self.kitty) + \
                "\n hand: " + \
                tempCardsInHand + \
                "\nOptions: " + "\n1: Yes\n2: No"
        # Call buildCardsInHandAndSuitOptions to show player what their hand is when choosing trump in phase 2. Gives them a yes or no option
        elif self.choosingTrumpPhase2:
            cardsInHandAndSuitOptions = self.buildCardsInHandAndSuitOptions(playerNumber)
            return turnString + \
                "Team One Score: " + str(self.team1Score) + " Team Two Score: " + str(self.team2Score) + \
                "\nOptions: " + \
                cardsInHandAndSuitOptions
        # Calls buildTempCardsInHand and then sends it back to the player with options for which card to remove
        elif self.discardPhase:
            tempCardsInHand = self.buildTempCardsInHand(playerNumber)
            return turnString + \
                "Team One Score: " + str(self.team1Score) + " Team Two Score: " + str(self.team2Score) + \
                "\nKitty: " + self.getCardText(self.kitty) + " of " + self.getCardSuitText(self.kitty) + \
                "\nOptions: " + \
                tempCardsInHand
        # Calls buildTempCardsInHand and also buildTempCardsOnTable and gives the player their options for what cards to play
        elif self.playingCardsPhase:
            tempCardsOnTable = self.buildTempCardsOnTable()
            tempCardsInHand = self.buildTempCardsInHand(playerNumber)
            return turnString + \
                "Team One Score: " + str(self.team1Score) + " Team Two Score: " + str(self.team2Score) + \
                tempCardsOnTable + \
                "\nOptions: " + \
                tempCardsInHand
        elif self.gameEnd:
            if self.winner == 1:
                return "Team One Wins!"
            elif self.winner == 2:
                return "Team Two Wins!"
            else:
                return "This text should never appear (Check gameEnding)"

    # clears moves so that the play can not be messed up
    def newRound(self):
        self.moves.clear()
        self.leader = (self.dealer + 1) % 4
        self.turn = self.leader

    # Iterates the turn to the next player
    def iterateTurn(self):
        self.turn = (self.turn + 1) % 4

    # Allows the dealer to switch the card in their hand for the card on the kitty
    def discard(self, player, option):
        self.players[player].pop((option - 1))
        self.players[player].append(self.kitty)
        self.discardPhase = False
        self.playingCardsPhase = True

    # a client tells the server what card they want to play
    def playCard(self, player, move):
        self.moves[player] = self.players[player][move - 1]  # the player will tell the HostServer what it wants to play
        self.players[player].pop(move - 1)  # Note this might be wrong
        self.iterateTurn()

    # If the player says "yes" take trump, else, next move
    def pickTrumpStage1(self, player, move):
        if move == "1":
            self.trump = self.getCardSuit(self.kitty)
            self.turn = (self.dealer + 1) % 4
            self.choosingTrumpPhase1 = False
            self.discardPhase = True
        else:
            pass  # Next turn
        
    # The player will say a specific suit (from the options listed) and then trump will be picked and playingCardsPhase ensues
    def pickTrumpStage2(self, player, option):
        tempSuits = []
        for suit in self.suits:
            if suit != self.getCardSuit(self.kitty):
                tempSuits.append(suit)
        self.trump = tempSuits[option - 1]
        self.turn = (self.dealer + 1) % 4
        self.choosingTrumpPhase2 = False
        self.playingCardsPhase = True

    # Helper methods to get the Card out of the 2 digit number
    def getCard(self, i):
        return (int(i / 10))

    # Helper method to get card suit
    def getCardSuit(self, i):
        return (i % 10)

    # Helper methods to get the Card out of the 2 digit number
    def getCardText(self, i):
        cardNum = int(i / 10)
        if cardNum == 1:
            return "9"
        elif cardNum == 2:
            return "10"
        elif cardNum == 3:
            return "Jack"
        elif cardNum == 4:
            return "Queen"
        elif cardNum == 5:
            return "King"
        elif cardNum == 6:
            return "Ace"
        return "This text should never appear (See getCardText)"

    # Helper method to get card suit
    def getCardSuitText(self, i):
        suitNum = int(i % 10)
        if suitNum == 0:
            return "Clubs"
        elif suitNum == 1:
            return "Diamonds"
        elif suitNum == 2:
            return "Hearts"
        elif suitNum == 3:
            return "Spades"
        else:
            return "Trump Not Selected Yet"

    # Helper method to get if the card is a left bower
    def suitComp(self, index):
        if index == 0:
            return 3
        elif index == 1:
            return 2
        elif index == 2:
            return 1
        elif index == 3:
            return 0

    # Compares cards from each hand, returns the number of the player who won the trick
    def scoreTrick(self, playerOne, playerTwo, playerThree, playerFour):
        tempScore1 = playerOne
        tempScore2 = playerTwo
        tempScore3 = playerThree
        tempScore4 = playerFour
        # Checks for right bower or trump
        if self.getCardSuit(playerOne) == self.trump:
            if self.getCard(playerOne) == 3:
                tempScore1 = tempScore1 + 500
            else:
                tempScore1 = tempScore1 + 100
        if self.getCardSuit(playerTwo) == self.trump:
            if self.getCard(playerTwo) == 3:
                tempScore2 = tempScore2 + 500
            else:
                tempScore2 = tempScore2 + 100
        if self.getCardSuit(playerThree) == self.trump:
            if self.getCard(playerThree) == 3:
                tempScore3 = tempScore3 + 500
            else:
                tempScore3 = tempScore3 + 100
        if self.getCardSuit(playerFour) == self.trump:
            if self.getCard(playerFour) == 3:
                tempScore4 = tempScore4 + 500
            else:
                tempScore4 = tempScore4 + 100

        # Check for left bower
        if self.getCard(playerOne) == 3 and self.getCardSuit(playerOne) == self.suitComp(self.trump):
            tempScore1 = tempScore1 + 250
        if self.getCard(playerTwo) == 3 and self.getCardSuit(playerTwo) == self.suitComp(self.trump):
            tempScore2 = tempScore2 + 250
        if self.getCard(playerThree) == 3 and self.getCardSuit(playerThree) == self.suitComp(self.trump):
            tempScore3 = tempScore3 + 250
        if self.getCard(playerFour) == 3 and self.getCardSuit(playerFour) == self.suitComp(self.trump):
            tempScore4 = tempScore4 + 250

        # Check for same suit as lead
        if self.getCardSuit(playerOne) == self.getCardSuit(self.moves[self.leader]):
            tempScore1 = tempScore1 + 50
        if self.getCardSuit(playerTwo) == self.getCardSuit(self.moves[self.leader]):
            tempScore2 = tempScore2 + 50
        if self.getCardSuit(playerThree) == self.getCardSuit(self.moves[self.leader]):
            tempScore3 = tempScore3 + 50
        if self.getCardSuit(playerFour) == self.getCardSuit(self.moves[self.leader]):
            tempScore4 = tempScore4 + 50

        if tempScore1 > tempScore2 and tempScore1 > tempScore3 and tempScore1 > tempScore4:
            self.leader = 0
            self.newRound()
            return 0
        elif tempScore2 > tempScore1 and tempScore2 > tempScore3 and tempScore2 > tempScore4:
            self.leader = 1
            self.newRound()
            return 1
        elif tempScore3 > tempScore1 and tempScore3 > tempScore2 and tempScore3 > tempScore4:
            self.leader = 2
            self.newRound()
            return 2
        elif tempScore4 > tempScore1 and tempScore4 > tempScore2 and tempScore4 > tempScore3:
            self.leader = 3
            self.newRound()
            return 3
        else:
            return "This means it's broken"

    # Checks to see if either team has won, will be played between tricks. If no one has won, return "No"
    def checkWinner(self):
        if (self.team1Score > 9) or (self.team2Score > 9):
            if self.team1Score > 9:
                self.gameEnd = True
                self.winner = 1
            else:
                self.gameEnd = True
                self.winner = 2
        else:
            pass
