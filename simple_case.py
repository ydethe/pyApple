# -*- coding: latin-1 -*-

import sys

# Put the path where pyApple is located here
#sys.path.append('~/pyApple')

import platform

from simple_reader import *

from gui_elem import *


d = Simple_Reader('data.txt')

carte = Map("Trace au sol", True, projection='merc')
tr_sol = Line("Trace au sol", d['lon'], d['lat'], color='b')
carte.addLine(tr_sol)

rep = Axe("Altitude")
alt = Line(u"Altitude", d['t'], d['alt'], color='b')
rep.addLine(alt)

fen = AppleWindow()
pl = fen.createBoard(u"Satellite")
pl.addAxe(rep)
pl.addAxe(carte)

fen.display()

