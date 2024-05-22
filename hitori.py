
from boardgame import BoardGame

class Hitori(BoardGame):

	CLEAR = 0
	BLACK = 1
	CIRCLE = 2
	
	def __init__(self, filename):
		
		self._rows = 0
		self._cols = 0
		self._num_mosse = 0
		
		with open(filename) as file:
			
			numeri = file.readline().split(",")
			dim = len(numeri)
			self._rows = dim
			self._cols = dim
			
			matrice = []
			
			numeri = [int(numeri[i]) for i in range(dim)]
			matrice.append(numeri)
			
			for i in range(dim - 1):
				numeri = file.readline().split(",")
				matrice.append([int(numeri[i]) for i in range(dim)])
			
			self._numeri = matrice 
			self._mosse = [[Hitori.CLEAR for j in range(dim)] for i in range(dim)]
			self._annotazioni = [[Hitori.CLEAR for j in range(dim)] for i in range(dim)]
	
	def cols(self):
		return self._cols
	
	def rows(self):
		return self._rows
	
	def play_at(self, x: int, y: int):
		
		# se la casella è già nera, ne rimuovo il colore
		if (self._mosse[y][x] == Hitori.BLACK):
			self._mosse[y][x] = Hitori.CLEAR
		else:
			self._mosse[y][x] = Hitori.BLACK
			self._num_mosse += 1

	
	def flag_at(self, x: int, y: int):
	
		# se la casella è già cerchiata, ne rimuovo il cerchio
		if (self._mosse[y][x] == Hitori.CIRCLE):
			self._mosse[y][x] = Hitori.CLEAR
		else:
			self._mosse[y][x] = Hitori.CIRCLE
		self._num_mosse += 1
	
	def value_at(self, x: int, y: int) -> str:
		
		value = str(self._numeri[y][x])
		if (self._mosse[y][x] == Hitori.BLACK):
			value += "#"
		elif (self._mosse[y][x] == Hitori.CIRCLE):
			value += "!"
		
		return value

	def clear_all(self):

		for i in range(self._rows):
			for j in range(self._cols):
				self._mosse[i][j] = Hitori.CLEAR

	def flag_cells(self):

		# cerco le caselle annerite
		for i in range(self._rows):
			for j in range(self._cols):
				if self._mosse[i][j] == Hitori.BLACK:
					for offset_i in range(-1, 2):
						for offset_j in range(-1, 2):
							coord_y = i + offset_i;
							coord_x = j + offset_j
							# cerchio ogni cella adiacente a quella annerita
							if (offset_i != offset_j and (offset_i == 0 or offset_j == 0) and coord_y >= 0 and coord_y < self._rows and 
								coord_x >= 0 and coord_x < self._cols):
								self._mosse[coord_y][coord_x] = Hitori.CIRCLE

	def play_cells(self):
		
		#cerco le caselle cerchiate
		for y in range(self._rows):
			for x in range(self._cols):
				if self._mosse[y][x] == Hitori.CIRCLE:
					# cerco sulla stessa colonna tutte le caselle non annerite con lo stesso numero di quella cerchiata, per annerirle
					for i in range(self._rows):
						if i != y and self._numeri[i][x] == self._numeri[y][x] and self._mosse[i][x] != Hitori.BLACK:
							self._mosse[i][x] = Hitori.BLACK
					#faccio lo stesso lungo la stessa riga della casella cerchiata
					for j in range(self._cols):
						if j != x and self._numeri[y][j] == self._numeri[y][x] and self._mosse[y][j] != Hitori.BLACK:
							self._mosse[y][j] = Hitori.BLACK

	def mark_auto(self):
		self.flag_cells()
		self.play_cells()

	def wrong(self) -> bool:

		self._annotazioni = [[self._mosse[i][j] for j in range(self._cols)] for i in range(self._rows)]

		for y in range(self._rows):
			for x in range(self._cols):
				
				# contatore delle caselle nere contigue a quella corrente, nel caso sia in una casella bianca	
				num_caselle_nere = 0

				for i in range(-1, 2):
					for j in range(-1, 2):
						coord_y = y + i
						coord_x = x + j
						if i != j and (i == 0 or j == 0) and coord_y >= 0 and coord_y < self._rows and coord_x >= 0 and coord_x < self._cols:
							if self._annotazioni[coord_y][coord_x] == Hitori.BLACK:
								if self._annotazioni[y][x] == Hitori.BLACK:
									return True
								elif self._annotazioni[y][x] == Hitori.CLEAR:
									num_caselle_nere += 1
							elif ((self._annotazioni[y][x] == Hitori.CIRCLE and self._numeri[y][x] == self._numeri[coord_y][coord_x] and 
								self._annotazioni[coord_y][coord_x] == Hitori.CIRCLE)):
								return True
						# if i != j and (i == 0 or j == 0) and coord_y >= 0 and coord_y < self._rows and coord_x >= 0 and coord_x < self._cols:
						# 	if self._annotazioni[y][x] == Hitori.CLEAR and self._annotazioni[coord_y][coord_x] == Hitori.BLACK:
						# 		num_caselle_nere += 1
						# 	elif ((self._annotazioni[y][x] == Hitori.CIRCLE and self._numeri[y][x] == self._numeri[coord_y][coord_x] and self._annotazioni[coord_y][coord_x] == Hitori.CIRCLE) or 
						# 		(self._annotazioni[y][x] == Hitori.BLACK and self._annotazioni[coord_y][coord_x] == Hitori.BLACK)):
						# 		return True

				if self._annotazioni[y][x] == Hitori.CLEAR and num_caselle_nere == 4:
					return True

		return not self.rete_connessa()

	def get_suggestions(self):

		for i in range(self._rows):
			for j in range(self._cols):
				if self._mosse[i][j] == Hitori.CLEAR:

					stato_iniziale = [[self._mosse[i][j] for j in range(self._cols)] for i in range(self._rows)]

					# provo ad annotare la casella corrente
					self._mosse[i][j] = Hitori.BLACK

					# automatizzo l'annotazione delle caselle
					self.mark_auto()

					if not self.wrong():

						# memorizzo lo stato della scacchiera a seguito delle mosse automatizzate 
						risultato_casella_annerita = [[self._mosse[y][x] for x in range(self._cols)] for y in range(self._rows)]

						# riporto lo stato della scacchiera allo stato iniziale
						self._mosse = [[stato_iniziale[y][x] for x in range(self._cols)] for y in range(self._rows)]

						# provo a cerchiare la casella corrente
						self._mosse[i][j] = Hitori.CIRCLE

						#automatizzo l'annotazione delle caselle
						self.mark_auto()

						if not self.wrong():

							# memorizzo lo stato della scacchiera a seguito delle mosse automatizzate
							risultato_casella_cerchiata = [[self._mosse[y][x] for x in range(self._cols)] for y in range(self._rows)]

							# riporto lo stato della scacchiera allo stato iniziale
							self._mosse = [[stato_iniziale[y][x] for x in range(self._cols)] for y in range(self._rows)]

							# confronto le celle ottenute dai due risultati, se i due risultati hanno settato la stessa annotazione
							# per una determinata casella, effettuo sulla stessa la medesima annotazione nella griglia
							for y in range(self._rows):
								for x in range(self._cols):
									if (self._mosse[y][x] != risultato_casella_annerita[y][x] and 
										(risultato_casella_annerita[y][x] == risultato_casella_cerchiata[y][x])):
										self._mosse[y][x] = risultato_casella_annerita[y][x]
						else:
							# riporto lo stato della scacchiera allo stato iniziale
							self._mosse = [[stato_iniziale[y][x] for x in range(self._cols)] for y in range(self._rows)]
					
					else:
						# riporto lo stato della scacchiera allo stato iniziale
						self._mosse = [[stato_iniziale[y][x] for x in range(self._cols)] for y in range(self._rows)]

	
	# fornisce un suggerimento annerendo una casella 
	def get_suggestion(self):

		casella_da_annerire_trovata = False
		i = 0
		while i < self._rows and not casella_da_annerire_trovata:
			j = 0
			while j < self._cols and not casella_da_annerire_trovata:
				if self._mosse[i][j] == Hitori.CLEAR:

					stato_iniziale = [[self._mosse[i][j] for j in range(self._cols)] for i in range(self._rows)]

					# provo ad annotare la casella corrente
					self._mosse[i][j] = Hitori.BLACK

					# automatizzo l'annotazione delle caselle
					self.mark_auto()

					if not self.wrong():

						# memorizzo lo stato della scacchiera a seguito delle mosse automatizzate 
						risultato_casella_annerita = [[self._mosse[y][x] for x in range(self._cols)] for y in range(self._rows)]

						# riporto lo stato della scacchiera allo stato iniziale
						self._mosse = [[stato_iniziale[y][x] for x in range(self._cols)] for y in range(self._rows)]

						# provo a cerchiare la casella corrente
						self._mosse[i][j] = Hitori.CIRCLE

						#automatizzo l'annotazione delle caselle
						self.mark_auto()

						if not self.wrong():

							# memorizzo lo stato della scacchiera a seguito delle mosse automatizzate
							risultato_casella_cerchiata = [[self._mosse[y][x] for x in range(self._cols)] for y in range(self._rows)]

							# riporto lo stato della scacchiera allo stato iniziale
							self._mosse = [[stato_iniziale[y][x] for x in range(self._cols)] for y in range(self._rows)]

							# confronto le celle ottenute dai due risultati, se i due risultati hanno settato la stessa annotazione
							# (cioè entrambi assegnano l'annerimento o il cerciamento) per una determinata casella, 
							# essa è un'annotazione corretta per quella stessa casella, quindi da consigliare. 
							# Il suggerimento da dare all'utente, però, è quello dell'annerimento di una sola casella, quindi sono interessato
							# solo alle caselle per cui i due risultati hanno assegnato l'annerimento e di queste annerisco solo la prima
							# che trovo
							casella_da_annerire_trovata = False
							y = 0
							while y < self._rows and not casella_da_annerire_trovata:
								x = 0
								while x < self._cols and not casella_da_annerire_trovata:
									if (self._mosse[y][x] != risultato_casella_annerita[y][x] and
										risultato_casella_annerita[y][x] == Hitori.BLACK and
										risultato_casella_annerita[y][x] == risultato_casella_cerchiata[y][x]):
										casella_da_annerire_trovata = True
										self._mosse[y][x] = risultato_casella_annerita[y][x]
									x += 1
								y += 1
						else:
							# riporto lo stato della scacchiera allo stato iniziale
							self._mosse = [[stato_iniziale[y][x] for x in range(self._cols)] for y in range(self._rows)]
					
					else:
						# riporto lo stato della scacchiera allo stato iniziale
						self._mosse = [[stato_iniziale[y][x] for x in range(self._cols)] for y in range(self._rows)]
				j += 1
			i += 1
		return casella_da_annerire_trovata

	def backtracking(self) -> bool:
		return self.solve_recursive(0, 0)

	def solve_recursive(self, i: int, j: int) -> bool:

		self.mark_auto()
		if self.wrong():
			return False 

		trovata_casella_bianca = False
		while i < self._rows and not trovata_casella_bianca:
			while j < self._cols and not trovata_casella_bianca:
				if self._mosse[i][j] == Hitori.CLEAR:
					trovata_casella_bianca = True
				else:
					j += 1
			if not trovata_casella_bianca:
				i += 1
				j = 0

		if trovata_casella_bianca:
			stato_precedente = [[self._mosse[y][x] for x in range(self._cols)] for y in range(self._rows)]
			for a in [Hitori.BLACK, Hitori.CIRCLE]:
				self._mosse[i][j] = a 
				if self.solve_recursive(i, j + 1):
					return True
				self._mosse = [[stato_precedente[y][x] for x in range(self._cols)] for y in range(self._rows)]

		return self.finished()

	
	def finished(self) -> bool:
	
		if self.wrong():
			return False

		for i in range(self._rows):
			clearnumbers = [self._numeri[i][j] for j in range(self._cols) if self._mosse[i][j] != Hitori.BLACK]
			# verifico se ci sono doppioni in una stessa riga. Appena ne trovo uno, restituisco false
			l = list()
			for number in clearnumbers:
				if (number in l):
					return False
				else:
					l.append(number)
		
		for j in range(self._cols):
			clearnumbers = [self._numeri[i][j] for i in range(self._rows) if self._mosse[i][j] != Hitori.BLACK]
			# verifico se ci sono doppioni in una stessa colonna. Appena ne trovo uno, restituisco false
			l = list()
			for number in clearnumbers:
				if (number in l):
					return False
				else:
					l.append(number)
		
		return self.rete_connessa()

	def rete_connessa(self) -> bool:
		matrice = [[False for j in range(self._cols)] for i in range(self._rows)]
		
		i_prima_cella_vuota = 0
		
		# cerco la prima casella bianca, da cui far partire la funzione che esplora la connessione delle caselle bianche
		trovataCellaBianca = False
		while i_prima_cella_vuota < self._rows and not trovataCellaBianca:
			j_prima_cella_vuota = 0
			while j_prima_cella_vuota < self._cols and not trovataCellaBianca:
				if self._mosse[i_prima_cella_vuota][j_prima_cella_vuota] != Hitori.BLACK:
					trovataCellaBianca = True
				else:
					j_prima_cella_vuota += 1
			if not trovataCellaBianca:
				i_prima_cella_vuota += 1

		n = self.esplora_connessione(j_prima_cella_vuota, i_prima_cella_vuota, matrice)

		# conto adesso le caselle bianche, dando per scontato che almeno una ne ho trovata
		#(altrimenti avrei tutte caselle nere)
		num_caselle_vuote = 1

		i = i_prima_cella_vuota
		j = j_prima_cella_vuota + 1
		while i < self._rows:
			while j < self._cols:
				if self._mosse[i][j] != Hitori.BLACK:
					num_caselle_vuote += 1
				j += 1
			i += 1
			j = 0

		return num_caselle_vuote == n

	def esplora_connessione(self, x: int, y: int, matrice):

		matrice[y][x] = True
		num_caselle = 1
		for i in range(-1, 2):
			for j in range(-1, 2):
				coord_x = x + j
				coord_y = y + i
				if (i != j and (i == 0 or j == 0) and coord_x >= 0 and coord_x < self._cols and coord_y >= 0 and coord_y < self._rows and
					self._mosse[coord_y][coord_x] != Hitori.BLACK and not matrice[coord_y][coord_x]):
					num_caselle += self.esplora_connessione(coord_x, coord_y, matrice)
		return num_caselle
		
	def message(self):
		return "Complimenti, hai vinto! [N. mosse: " + str(self._num_mosse) + "]"