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

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout

from pyApple.graph_elem import *
import time


class AppleFrame(QWidget):
   """
   This is the main widget embedded in the app's windows.
   It inherits from wx.Frame.
   The user should not manipulate it, because this is handled by the AppleWindow class.
   """
   def __init__(self, parent):
      """
      Initializes an instance of AppleFrame.
      Should not be called by the user.
      The arguments are the same as in wx.Frame's constructor.

      """
      super(QWidget, self).__init__(parent)
      self.layout = QVBoxLayout(self)

      # Initialize tab screen
      self.tabs = QTabWidget()
      self.tabs.resize(300,200)

      # Add tabs to widget
      self.layout.addWidget(self.tabs)
      self.setLayout(self.layout)


class AppleWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 tabs - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.main_frame = AppleFrame(self)
        self.setCentralWidget(self.main_frame)

        self.__boards = []

    def createBoard(self, titre):
        pl = Board(self)

        self.main_frame.tabs.addTab(pl, titre)
        self.__boards.append(pl)
        return pl

    def render(self):
        for pl in self.__boards:
            pl.render()
        self.show()

    def update(self):
        res = False
        for pl in self.__boards:
           res = res or pl.update()
        return res


def test():
   import doctest

   doctest.testmod()


if __name__ == '__main__':
    test()
