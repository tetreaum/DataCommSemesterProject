
class Card:

    NINE = 1
    TEN = 2
    JACK = 3
    QUEEN = 4
    KING = 5
    ACE = 6

# deck of cards is
# 10,11,12,13,20,21,22,23,30,31,32,33,40,41,42,43,50,51,52,53,60,61,62,63

# suits in alphabetical order
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

    def __init__(self, cardNum):
        if cardNum == 0:
            print("Hi")

    def getCard(self, i):
        return (int(i / 10))

    def getCardSuit(self, i):
        return (i % 10)

    def suitComp(self, index):
        if index == 0:
            return 3
        elif index == 1:
            return 2
        elif index == 2:
            return 1
        elif index == 3:
            return 0

    # compare all 4 peoples cards and return a 1 2 3 or 4 depending on who won that hand
    def compareCards(self, playerOne, playerTwo, playerThree, playerFour, trump):
        if self.getCardSuit(playerOne) == trump:
            if self.getCard(playerOne) == 3:
                playerOne = playerOne + 500
            else:
                playerOne = playerOne + 100

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
