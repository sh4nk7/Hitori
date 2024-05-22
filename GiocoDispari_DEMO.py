
from giocodispari import GiocoDispari 
from boardgame import console_play


h, w = input("Inserire dimensioni [h w]: ").split(" ")
g = GiocoDispari(int(h), int(w))
console_play(g)