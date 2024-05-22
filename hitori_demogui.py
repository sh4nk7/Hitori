
from hitori import Hitori
import boardgamegui

print("Selezionare la difficolta desiderata:")
print("1. Easy (5x5)")
print("2. Medium (6x6)")
print("3. Hard (8x8)")
print("4. Very hard (9x9)")
print("5. Super hard (12x12)")
print("6. Impossible (15x15)")

opzione = int(input())
if opzione >= 1 and opzione <= 6:
	filename = "hitori-"
	if opzione == 1:
		filename += "5x5"
	elif opzione == 2:
		filename += "6x6"
	elif opzione == 3:
		filename += "8x8"
	elif opzione == 4:
		filename += "9x9"
	elif opzione == 5:
		filename += "12x12"
	else:
		filename += "15x15"

	filename += ".txt"
	h = Hitori(filename)
	boardgamegui.gui_play(h)
else:
	print("opzione non valida")