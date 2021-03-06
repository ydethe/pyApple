# -*- coding: latin-1 -*-

#     This file is part of pyApple.
#
#     pyApple is free software: you can redistribute it and/or modify
#     it under the terms of the Lesser GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     pyApple is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     Lesser GNU General Public License for more details.
#
#     You should have received a copy of the Lesser GNU General Public License
#     along with pyApple.  If not, see <http://www.gnu.org/licenses/>.
import unittest
import sys

# Put the path where pyApple is located here
#sys.path.append('~/pyApple')

import platform

from pyApple.simple_reader import *

from pyApple.gui_elem import *


class TestSimple (unittest.TestCase):
    def test(self):
        d = Simple_Reader('pyApple/tests/data.txt')

        carte = Map("Trace au sol")
        tr_sol = Line("Trace au sol", d['lon'], d['lat'], color='b')
        carte.addLine(tr_sol)

        rep = Axe("Altitude")
        alt = Line(u"Altitude", d['t'], d['alt'], color='b')
        rep.addLine(alt)

        app = QApplication(sys.argv)

        fen = AppleWindow()
        pl = fen.createBoard(u"Satellite")
        pl.addAxe(rep)
        # pl.addAxe(carte)
        fen.render()

        app.exec_()
        # sys.exit(app.exec_())


if __name__ == '__main__':
    unittest.main()
