
from hitori import Hitori
from boardgame import console_play

print("Digitare il filename: ")
filename = input()
h = Hitori(filename)
console_play(h)