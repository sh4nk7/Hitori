
from random import seed
from random import randint
from boardgame import BoardGame
from boardgame import print_game

class GiocoDispari(BoardGame):

	CLEAR = 0
	MARKED = 1

	def __init__(self, h: int, w: int):

		# riempio la matrice con numeri incrementali da 1 a w * h
		matrix = [[j for j in range(i * w + 1, i * w + w + 1)] for i in range(h)]

		# scambio celle a caso della matrice
		numMosse = int(w * h / 2)
		seed()
		for i in range(numMosse):
			i_1 = randint(0, h - 1)
			j_1 = randint(0, w - 1)
			i_2 = randint(0, h - 1)
			j_2 = randint(0, w - 1)
			temp = matrix[i_1][j_1]
			matrix[i_1][j_1] = matrix[i_2][j_2]
			matrix[i_2][j_2] = temp

		self._numeri = matrix
		self._mosse = [[GiocoDispari.CLEAR for j in range(w)] for i in range(h)]
		self._rows = h
		self._cols = w
		self._num_mosse = 0

	def cols(self) -> int:
		return self._cols

	def rows(self) -> int:
		return self._rows

	def play_at(self, x: int, y: int):
		
		if self._mosse[y][x] == GiocoDispari.CLEAR:
			self._mosse[y][x] = GiocoDispari.MARKED
		else:
			self._mosse[y][x] = GiocoDispari.CLEAR

		self._num_mosse += 1

	def value_at(self, x: int, y: int) -> str:
		
		value = str(self._numeri[y][x])
		if self._mosse[y][x] == GiocoDispari.MARKED:
			value += "!"
		return value

	def finished(self) -> bool:
		
		for i in range(self._rows):
			for j in range(self._cols):
				if ((self._numeri[i][j] % 2 == 0 and self._mosse[i][j] == GiocoDispari.MARKED) or 
					(self._numeri[i][j] % 2 != 0 and self._mosse[i][j] == GiocoDispari.CLEAR)):
					return False
		
		return True

	def message(self):
		return "Complimenti, hai vinto! [N. mosse: " + str(self._num_mosse) + "]"
