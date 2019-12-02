import random


class GameBoard:
    placeInDeck = "ree"
    deck = [None] * 24
    discardPile = [10, 11, 12, 13, 20, 21, 22, 23, 30, 31, 32, 33, 40, 41, 42, 43, 50, 51, 52, 53, 60, 61, 62, 63]
    trump = 0

    def __init__(self):
        pass

    def gameRound(self):
        # loop through the game logic
        pass

    def newHand(self):
        tempHand = None * 5
        for i in tempHand:
            tempHand[i] = self.deck[self.placeInDeck]
            self.deck[self.placeInDeck] = None
            self.placeInDeck = self.placeInDeck + 1
        return tempHand

    # takes the discard pile, and shuffles it back into the deck
    def shuffleDeck(self):
        filled = False
        for i in self.discardPile:
            while (filled is False):
                r1 = random.randint(0, 23)
                if self.deck[r1] is None:
                    self.deck[r1] is self.discardPile[i]
                    filled is True

    def main(self):
        self.shuffleDeck(self)
        print(self.deck)

    main()
