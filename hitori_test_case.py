
import unittest
from hitori import Hitori

class HitoriTestCase(unittest.TestCase):
	
	NONE = 0
	PLAY_AT_MOVE = 1
	FLAG_AT_MOVE = 2
	
    
	def test_black_circle_cells(self):
		
		test_moves = ( 	(HitoriTestCase.PLAY_AT_MOVE, 0, 0, "2#"),
						(HitoriTestCase.PLAY_AT_MOVE, 1, 0, "2#"),
						(HitoriTestCase.FLAG_AT_MOVE, 1, 1, "3!"),
						(HitoriTestCase.PLAY_AT_MOVE, 3, 1, "4#"),
						(HitoriTestCase.FLAG_AT_MOVE, 0, 4, "5!"),
						(HitoriTestCase.NONE, 2, 1, "1"),
						(HitoriTestCase.NONE, 3, 2, "3") )
		
		h = Hitori("hitori-5x5.txt")
		
		for param in test_moves:
				move, x, y, value = param
				if (move == HitoriTestCase.PLAY_AT_MOVE):
					h.play_at(x, y)
				elif (move == HitoriTestCase.FLAG_AT_MOVE):
					h.flag_at(x, y)

				self.assertTrue(h.value_at(x, y) == value)

	# test che verifica se hitori riconosce lo stato di una scacchiera che rappresenta
	# una partita vinta
	def test_game_finished(self):

		test_moves = ( 	(0, 0),
						(2, 0),
						(4, 1),
						(0, 2),
						(2, 2),
						(1, 3),
						(3, 3) )

		h = Hitori("hitori-5x5.txt")

		for param in test_moves:
			x, y = param
			h.play_at(x, y)

		self.assertTrue(h.finished())

	# test che verifica se hitori riconosce la violazione delle regole
	# a causa della contiguita' tra due celle annerite, anche nel caso in cui
	# le annotazioni consentono di avere un numero solo per ogni riga e colonna
	def test_adiacent_black_cells(self):

		test_moves = ( 	(0, 0),
						(2, 0),
						(4, 1),
						(0, 2),
						(2, 2),
						(1, 3),
						(3, 3),
						(4, 0))

		h = Hitori("hitori-5x5.txt")

		for param in test_moves:
			x, y = param
			h.play_at(x, y)

		self.assertFalse(h.finished())

	# test che verifica se hitori riconosce la mancata fine del gioco
	# nel caso la scacchiera abbia due caselle dallo stesso valore 
	# non annerite in una medesima colonna
	def test_duplicated_values(self):

		test_moves = ( 	(0, 0),
						(2, 0),
						(4, 1),
						(0, 2),
						(2, 2),
						(1, 3) )

		h = Hitori("hitori-5x5.txt")

		for param in test_moves:
			x, y = param
			h.play_at(x, y)
		
		self.assertFalse(h.finished())

	# test che verifica, nell'ordine, che:
	# - dopo l'annerimento della casella (2, 2) della scacchiera hitori-5x5.txt, tre chiamate successive di get_suggestion() 
	#   portano all'annerimento, nell'ordine, delle caselle (2, 0), (0, 0) e (0, 2)
	# - una successiva chiamata di get_suggestion() non trova ulteriori suggerimenti, ma la partita non è finita e i suggerimenti
	#   dati non hanno portato alla violazione di alcuna regola
	# - esiste una soluzione per la configurazione ottenuta, la cui esecuzione porta a vincere la partita
	def test_suggestions_correctness_backtracking(self):

		h = Hitori("hitori-5x5.txt")

		h.play_at(2, 2)
		self.assertTrue(h.get_suggestion())
		self.assertTrue(h.value_at(2, 0)[-1] == "#")
		self.assertTrue(h.get_suggestion())
		self.assertTrue(h.value_at(0, 0)[-1] == "#")
		self.assertTrue(h.get_suggestion())
		self.assertTrue(h.value_at(0, 2)[-1] == "#")
		self.assertFalse(h.get_suggestion())
		self.assertFalse(h.finished())
		self.assertFalse(h.wrong())
		self.assertTrue(h.backtracking())
		self.assertTrue(h.finished())

	# test che verifica, nell'ordine, che:
	# - dopo aver annerito le caselle (0, 2) e (0, 1) non esiste una soluzione che porta alla vittoria a causa della contiguità
	#   di due caselle annerite
	# - dopo aver tolto ogni annotazione dalla scacchiera e aver annerito la sola casella (0, 2), esiste una soluzione
	def test_correctness_backtracking(self):

		h = Hitori("hitori-5x5.txt")

		h.play_at(2, 0)
		h.play_at(1, 0)
		self.assertFalse(h.backtracking())
		h.clear_all()
		h.play_at(2, 0)
		self.assertTrue(h.backtracking())




testCase = HitoriTestCase()
testCase.test_black_circle_cells()
testCase.test_game_finished()
testCase.test_adiacent_black_cells()
testCase.test_duplicated_values()
testCase.test_suggestions_correctness_backtracking()
testCase.test_correctness_backtracking()
				