
score = 0
cards = [None] * 5


class Player:
    def __init__(self, score, cards):
        score = 0
        cards = GameBoard.newHand()

    def NewHand(self, person):
        cards = GameBoard.newHand()

    def getScore(self):
        return (score)

    def playCard(self):
        print("Which card do you want to pick")
        decision = raw_input(cards + "either 1,2,3,4,5")
        return (decision)
