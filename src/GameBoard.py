import random


class GameBoard:
	  placeInDeck
	  deck = [None] * 24
	  discardPile = [10,11,12,13,20,21,22,23,30,31,32,33,40,41,42,43,50,51,52,53,60,61,62,63]
	  trump = 0
	  
	  def  __init__():

		shuffleDeck()

		print(deck)


	def gameRound():
	#loop through the game logic


	def newHand():
		tempHand = None * 5
		for i in tempHand:
			tempHand[i] = deck[placeInDeck]
			deck[placeInDeck] = None
			placeInDeck = placeInDeck + 1
		return tempHand




#takes the discard pile, and shuffles it back into the deck
	def shuffleDeck():
		filled = false
		for i in discardPile:
			while (filled == False):
				r1 = random.randint(0, 23)
				if deck[r1] == None:
					deck[r1] == discardPile[i]
					filled == True
