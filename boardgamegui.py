#!/usr/bin/env python3
'''
@author  Michele Tomaiuolo - http://www.ce.unipr.it/people/tomamic
@license This software is free - http://www.gnu.org/licenses/gpl.html
'''

import g2d
from boardgame import BoardGame
from time import time
from hitori import Hitori

W, H = 40, 40
LONG_PRESS = 0.5
circle = g2d.load_image("circle.jpg")

class BoardGameGui:
	def __init__(self, g: BoardGame):
		self._game = g
		self._downtime = 0
		self.update_buttons()

	def tick(self):
		if g2d.key_pressed("LeftButton"):
			self._downtime = time()
		elif g2d.key_released("LeftButton"):
			mouse = g2d.mouse_position()
			x, y = mouse[0] // W, mouse[1] // H
			stringa = "casella (" + str(y) + ", " + str(x) + ") "
			if time() - self._downtime > LONG_PRESS:
				self._game.flag_at(x, y)
				stringa += "cerchiata"
			else:
				self._game.play_at(x, y)
				stringa += "annerita"
			print(stringa)
			self.update_buttons()
		elif g2d.key_pressed("KeyW"):
			self._game.flag_cells()
			self.update_buttons()
		elif g2d.key_pressed("KeyE"):
			self._game.play_cells()
			self.update_buttons()
		elif g2d.key_pressed("KeyR"):
			cella_annerita = self._game.get_suggestion()
			if cella_annerita:
				self.update_buttons()
			else:
				g2d.alert("Nessun è possibile al momento trovare un suggerimento")
		elif g2d.key_pressed("KeyB"):
			if not self._game.backtracking():
				g2d.alert("Non è possibile vincere la partita con la configurazione attuale.")
			self.update_buttons()
		elif g2d.key_pressed("KeyC"):
			self._game.clear_all()
			self.update_buttons()

	def update_buttons(self):
		g2d.clear_canvas()
		g2d.set_color((0, 0, 0))
		cols, rows = self._game.cols(), self._game.rows()
		for y in range(1, rows):
			g2d.draw_line((0, y * H), (cols * W, y * H))
		for x in range(1, cols):
			g2d.draw_line((x * W, 0), (x * W, rows * H))
		for y in range(rows):
			for x in range(cols):
				center = x * W + W//2, y * H + H//2
				value = self._game.value_at(x, y)
				if value[-1] == "!":
					value = value[0:-1]
					g2d.draw_image_clip(circle, (0, 0, 899, 899), (x * W + 1, y * H + 1, W - 1, H - 1))
				elif value[-1] == "#":
					value = value[0:-1]
					g2d.fill_rect((x * W, y * H, W, H))
				g2d.draw_text_centered(value, center, H//2)
		g2d.update_canvas()
		if self._game.finished():
			g2d.alert(self._game.message())
			g2d.close_canvas()

def gui_play(game: BoardGame):
	g2d.init_canvas((game.cols() * W, game.rows() * H))
	ui = BoardGameGui(game)
	g2d.main_loop(ui.tick)
