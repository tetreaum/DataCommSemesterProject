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


class Euchre:
    def __init__(self, id):
        self.turn = 0
        self.ready = False
        self.id = id
        self.moves = []
        self.players = {}
        self.trump = ""
        self.team1Score = 0
        self.team2Score = 0
        self.cards = [10, 11, 12, 13, 20, 21, 22, 23, 30, 31, 32, 33, 40, 41, 42, 43, 50, 51, 52, 53, 60, 61, 62, 63]

    # add a player to the dictionary with an empty list as their value (called when first connecting)
    def addPlayer(self, player):
        self.players[player] = []

    # checks if we have enough players to play
    def checkNumPlayers(self):
        return len(self.players)

    # returns the cards available in a players hand that they can play
    def getPlayerMove(self, p):
        return self.moves[p]  # return the cards in that player's hand

    # a client tells the server what card they want to play
    def playCard(self, player, move):
        self.moves[player] = move  # the player will tell the HostServer what it wants to play

    # I don't think we need this. 
    def connected(self):
        return self.ready  # tells the server who is all connected

    # A class to handle dealing the cards to each person's "hand" in the dictionary
    def deal(self):
        pass  # Deals the cards for the 'dealer' leaving the kitty up

    def pickTrump(self, player, move):
        pass  # Play move will be yes or no

    # Helper methods to get the Card out of the 2 digit number
    def getCard(self, i):
        return (int(i / 10))

    # Helper method to get card suit
    def getCardSuit(self, i):
        return (i % 10)

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
    def scoreTrick(self, playerOne, playerTwo, playerThree, playerFour, trump):
        # Checks for right bower or trump
        if self.getCardSuit(playerOne) == trump:
            if self.getCard(playerOne) == 3:
                playerOne = playerOne + 500
            else:
                playerOne = playerOne + 100
        # elif self.getCard(player) == 3:
        #     if self.getCardSuit(player) == (trump + 2 % 4):
        #         player = player + 250
        #     else:
        #         pass

        if self.getCardSuit(playerTwo) == trump:
            if self.getCard(playerTwo) == 3:
                playerTwo = playerTwo + 500
            else:
                playerTwo = playerTwo + 100

        if self.getCardSuit(playerThree) == trump:
            if self.getCard(playerThree) == 3:
                playerThree = playerThree + 500
            else:
                playerThree = playerThree + 100

        if self.getCardSuit(playerFour) == trump:
            if self.getCard(playerFour) == 3:
                playerFour = playerFour + 500
            else:
                playerFour = playerFour + 100

        # Check for left bower
        if self.getCard(playerOne) == 3 and self.getCardSuit(playerOne) == self.suitComp(trump):
            playerOne = playerOne + 250

        if self.getCard(playerTwo) == 3 and self.getCardSuit(playerTwo) == self.suitComp(trump):
            playerTwo = playerTwo + 250

        if self.getCard(playerThree) == 3 and self.getCardSuit(playerThree) == self.suitComp(trump):
            playerThree = playerThree + 250

        if self.getCard(playerFour) == 3 and self.getCardSuit(playerFour) == self.suitComp(trump):
            playerFour = playerFour + 250

        if playerOne > playerTwo and playerOne > playerThree and playerOne > playerFour:
            return 1

        if playerTwo > playerOne and playerTwo > playerThree and playerTwo > playerFour:
            return 2
        if playerThree > playerOne and playerThree > playerTwo and playerThree > playerFour:
            return 3

        if playerFour > playerOne and playerFour > playerTwo and playerFour > playerThree:
            return 4

    # Checks to see if either team has won, will be played between tricks. If no one has won, return "No"
    def checkWinner(self, team1Score, team2Score):
        if (team1Score > 9) or (team2Score > 9):
            if team1Score > 9:
                return "Team One!"
            else:
                return "Team Two!"
        else:
            return "No"
