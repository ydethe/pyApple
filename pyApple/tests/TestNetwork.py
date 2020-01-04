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

import qt5reactor
qt5reactor.install()

# Put the path where pyApple is located here
#sys.path.append('~/pyApple')

import platform

from pyApple.network_reader import start

from pyApple.gui_elem import *


class TestNetwork (unittest.TestCase):
    def test(self):
        d = start("localhost", 8008)

        rep = Axe("Acc. x")
        alt = Line(u"Acc", d['t'], d['ax'], color='b')
        rep.addLine(alt)

        app = QApplication(sys.argv)

        fen = AppleWindow()
        pl = fen.createBoard(u"iPhone")
        pl.addAxe(rep)
        fen.render()

        app.exec_()


if __name__ == '__main__':
    unittest.main()
