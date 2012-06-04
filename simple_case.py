# -*- coding: latin-1 -*-

import sys

# Put the path where pyApple is located here
sys.path.append('~/pyApple')

import platform

from simple_reader import *

import tic_frame as tic


d = Simple_Reader('~/pyApple/data.txt')

carte = tic.Carte("Trace au sol", True, projection='merc')
tr_sol = tic.Courbe("Trace au sol", d['lon'], d['lat'], couleur='b')
carte.ajCourbe(tr_sol)

rep = tic.Repere("Altitude")
alt = tic.Courbe(u"Altitude", d['t'], d['alt'], couleur='b')
rep.ajCourbe(alt)
# print alt.moyenne()
# print sqrt(alt.variance())

fen = tic.Fenetre()
pl = fen.creerPlanche(u"Satellite")
pl.ajRepere(rep)
pl.ajRepere(carte)

fen.afficher()

