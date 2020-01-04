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

from math import *
import numpy as np

import matplotlib
matplotlib.use('QT5Agg')
import cartopy.crs as ccrs
from mpl_toolkits.mplot3d import Axes3D

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout

from matplotlib.figure import Figure

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QWidget

from pyApple.aplCommon import *
from pyApple.base_reader import *


def auto_layout(nb_axes):
   """
   Computes the best layout that make nb_axes fit onto the board.

   Parameters
   ----------
   nb_axes : integer
      Number of axes on the board

   Returns
   -------
   (rows, cols) : integer, integer
      Number of rows, and number of columns

   Tests
   -----
   >>> auto_layout(3)
   (2, 2)
   >>> auto_layout(7)
   (3, 3)

   """
   ro = int(round(sqrt(nb_axes)))
   co = int(ceil(float(nb_axes)/float(ro)))
   return ro, co


def moy_pond(moys,ponds=None):
   """
   moy_pond(moys,ponds) computes the average of moys, with th eponderation ponds

   Parameters
   ----------
   moys : array
      Array of numbers to average
   ponds : array (Optionnal)
      Array of coefficents on the numbers to average
      If not given, assumed to be 1 for everything

   Returns
   -------
   m : number
      Average

   Tests
   -----
   >>> moy_pond([1., 2., 3.])
   2.0
   >>> moy_pond([1., 2., 3.], [1., 1., 2.])
   2.25

   """
   if ponds == None:
      ponds = [1. for i in moys]
   tot = sum(ponds)
   moy = 0.
   for y, p in zip(moys, ponds):
      moy += y*p/tot
   return moy


class LineBase (object):
   def __init__(self, title, var_x, var_y, var_z=None, formula_x=None, formula_y=None, formula_z=None):
      self.title = title
      self.var_x = var_x
      self.var_y = var_y
      self.var_z = var_z
      self.plot_data = []

      if formula_x != None:
         self.formula_x = formula_x
      else:
         self.formula_x = identity

      if formula_y != None:
         self.formula_y = formula_y
      else:
         self.formula_y = identity

      if formula_z != None:
         self.formula_z = formula_z
      else:
         self.formula_z = identity

      self.type= 'undef'

   def update(self):
      self.var_x.update()
      self.var_y.update()
      if self.var_z != None:
         self.var_z.update()

      x_d, y_d = self.plot_data[-1].get_data()
      new_x = list(self.var_x)
      new_y = list(self.var_y)
      if len(x_d) != len(new_x) or len(y_d) != len(new_y):
         self.plot_data[-1].set_xdata(new_x)
         self.plot_data[-1].set_ydata(new_y)
         res = True
      else:
         res = False

      return res


class Line (LineBase):
   """
   Line is the class which describes a plottable 2D line.
   """
   def __init__(self, title, var_x, var_y, color='b', formula_x=None, formula_y=None):
      """
      Instanciates a plottable Line.

      Parameters
      ----------
      title : string
         Title of the line
      var_x :
         An iterable object containing the x data
      var_y :
         An iterable object containing the y data
      color :
         The color of the line. Is the same than in matplotlib, e.g. b, r, c, m, k, y, g. Default is blue ('b')
      formula_x :
         The function applied to all the elements of the x data. Default is identity (no modification)
      formula_y :
         The function applied to all the elements of the y data. Default is identity (no modification)

      Tests
      -----
      >>> l = Line('Temperature', [0., 1., 2.], [200., 210., 205.], color='b')

      """
      LineBase.__init__(self, title, var_x, var_y, None, formula_x, formula_y, None)
      self.color = color
      self.type= 'line2d'

   def get_min(self):
      """
      Returns the tuple (x_min, y_min) where x_min is the minimum value of the x data,
      taking the function formula_x into account. (The same for y_min)

      Returns
      -------
      (x_min, y_min) : tuple of number
         Tuple containing the minimum value of x-data and the minimum value of y-data

      Tests
      -----
      >>> l = Line('Temperature', [0., 1., 2.], [200., 210., 205.], color='b')
      >>> l.get_min()
      (0.0, 200.0)

      """
      x_d = filter(lambda x:x>-999,list(self.var_x))
      if len(x_d) == 0:
         return 0., 0.
      min_x = min(x_d)
      min_y = min(filter(lambda x:x>-999,list(self.var_y)))
      return self.formula_x(min_x), self.formula_y(min_y)

   def get_max(self):
      """
      Returns the tuple (x_max, y_max) where x_max is the maximum value of the x data,
      taking the function formula_x into account. (The same for y_max)

      Returns
      -------
      (x_max, y_max) : tuple of number
         Tuple containing the maximum value of x-data and the maximum value of y-data

      Tests
      -----
      >>> l = Line('Temperature', [0., 1., 2.], [200., 210., 205.], color='b')
      >>> l.get_max()
      (2.0, 210.0)

      """
      x_d = filter(lambda x:x>-999,list(self.var_x))
      if len(x_d) == 0:
         return 0., 0.
      max_x = max(x_d)
      max_y = max(filter(lambda x:x>-999,list(self.var_y)))
      return self.formula_x(max_x), self.formula_y(max_y)

   def render(self, axe, transf=None):
      """
      Main method of the Line class to render the Line on an Axe.
      Should not be called by the user. It is called automatically by the Axe class.

      Parameters
      ----------
      axe : matplotlib.axes.Axes
         The matplotlib axe we will plot the line on.
      transf : function
         A function which takes 2 iterable arguments, and returns a tuple of 2 lists
         This function (which is ignored by default) is a 2D distortion of the line, and is very much used by the Map class
         to make the line compliant with the projection used.

      """
      tab_x = []
      tab_y = []
      self.plot_data = []
      for x, y in zip(self.var_x, self.var_y):
         if y < -999:
            if transf != None:
               tab_x, tab_y = transf(tab_x, tab_y)
            self.plot_data.extend(axe.plot(tab_x, tab_y, self.color, linewidth=1., label=self.title))
            tab_x = []
            tab_y = []
         else:
            tab_x.append(self.formula_x(x))
            tab_y.append(self.formula_y(y))
      if tab_x != [] or self.plot_data == []:
         if transf != None:
            tab_x, tab_y = transf(tab_x, tab_y)
         self.plot_data.extend(axe.plot(tab_x, tab_y, self.color, linewidth=1., label=self.title))

   def average(self, meth='trap', fct=identity):
      """
      Computes the average value of the line, assuming it represents a continuous function.
      It is based on an numerical integration method, assuming the x-data is sorted.
      An optionnal function can be applied to the y-data to compute for example the average of the squared y-values.

      Parameters
      ----------
      meth : string (Optionnal)
         Name of the integration method. Is 'trap' by default, and can be:
         - 'trap'  : integration with trapezes
         - 'left'  : integration with rectangles whose height is the left value of the line
         - 'right' : integration with rectangles whose height is the right value of the line
      fct : function (Optionnal)
         Function applied to the y-values before averaging

      Returns
      -------
      m : number
         Average of the line

      Tests
      -----
      >>> l = Line('Temperature', [0., 1., 3.], [200., 210., 205.], color='b')
      >>> l.average()
      206.66666666666666

      """
      tab_x = []
      tab_y = []
      moys = []
      ponds = []

      val_conv_data = -999.

      for x, y in zip(self.x, self.y)+[(val_conv_data*2,val_conv_data*2)]:
         if y < val_conv_data:
            # Traitement ici
            if [tab_x[i+1]-tab_x[i] for i in range(len(tab_x)-1) if tab_x[i+1]-tab_x[i] < 0.] != []:
               return val_conv_data
            integrale = 0.
            for i in range(len(tab_x)-1):
               if meth == 'trap':
                  integrale += (tab_y[i] + tab_y[i+1])/2.*(tab_x[i+1] - tab_x[i])
               if meth == 'left':
                  integrale += tab_y[i]*(tab_x[i+1] - tab_x[i])
               if meth == 'right':
                  integrale += tab_y[i+1]*(tab_x[i+1] - tab_x[i])
            delta = max(tab_x) - min(tab_x)
            moys.append(integrale/delta)
            ponds.append(delta)
            tab_x = []
            tab_y = []
         else:
            tab_x.append(x)
            tab_y.append(fct(y))
      return moy_pond(moys,ponds)

   def std_dev(self, meth='trap'):
      """
      Computes the standard-deviation of the Line, assuming it represents a continuous function.
      It is based on an numerical integration method, assuming the x-data is sorted.

      Parameters
      ----------
      meth : string (Optionnal)
         Name of the integration method. Is 'trap' by default, and can be:
         - 'trap'  : integration with trapezes
         - 'left'  : integration with rectangles whose height is the left value of the line
         - 'right' : integration with rectangles whose height is the right value of the line

      Returns
      -------
      sd : number
         Standard-deviation of the line

      Tests
      -----
      >>> l = Line('Temperature', [0., 1., 3.], [200., 210., 205.], color='b')
      >>> l.std_dev()
      13.888888888890506

      """

      return self.average(meth, lambda x:x**2) - self.average(meth)**2


class Line3D (object):
   """
   Line3D is the class which describes a plottable 3D line.
   """
   def __init__(self, title, var_x, var_y, var_z, color='b', formula_x=None, formula_y=None, formula_z=None):
      """
      Instanciates a plottable Line.

      Parameters
      ----------
      title : string
         Title of the line
      var_x :
         An iterable object containing the x data
      var_y :
         An iterable object containing the y data
      var_z :
         An iterable object containing the z data
      color :
         The color of the line. Is the same than in matplotlib, e.g. b, r, c, m, k, y, g. Default is blue ('b')
      formula_x :
         The function applied to all the elements of the x data. Default is identity (no modification)
      formula_y :
         The function applied to all the elements of the y data. Default is identity (no modification)
      formula_z :
         The function applied to all the elements of the z data. Default is identity (no modification)

      """
      LineBase.__init__(self, title, var_x, var_y, var_z, formula_x, formula_y, formula_z)
      self.color = color
      self.type= 'line3d'

   def get_min(self):
      """
      Returns the tuple (x_min, y_min, z_min) where x_min is the minimum value of the x data,
      taking the function formula_x into account. (The same for y_min and z_min)

      Returns
      -------
      (x_min, y_min, z_min) : tuple of number
         Tuple containing the minimum value of x-data, y-data and z-data

      """
      min_x = min(filter(lambda x:x>-9999999,self.x))
      min_y = min(filter(lambda x:x>-9999999,self.y))
      min_z = min(filter(lambda x:x>-9999999,self.z))
      return min_x, min_y, min_z

   def get_max(self):
      """
      Returns the tuple (x_max, y_max, z_max) where x_max is the maximum value of the x data,
      taking the function formula_x into account. (The same for y_max and z_max)

      Returns
      -------
      (x_max, y_max, z_max) : tuple of number
         Tuple containing the maximum value of x-data, y-data and z-data

      """
      max_x = max(filter(lambda x:x>-9999999,self.x))
      max_y = max(filter(lambda x:x>-9999999,self.y))
      max_z = max(filter(lambda x:x>-9999999,self.z))
      return max_x, max_y, max_z

   def render(self, axe):
      """
      Main method of the Line3D class to render the Line3D on an Axe.
      Should not be called by the user. It is called automatically by the Axe class.

      Parameters
      ----------
      axe : matplotlib.axes.Axes
         The matplotlib axe we will plot the line on.

      """
      tab_x = []
      tab_y = []
      tab_z = []
      self.plot_data = []
      for x, y, z in zip(self.x, self.y, self.z):
         if y < -9999999:
            self.plot_data.extend(axe.plot(tab_x, tab_y, tab_z, self.color, linewidth=1., label=self.title))
            tab_x = []
            tab_y = []
            tab_z = []
         else:
            tab_x.append(x)
            tab_y.append(y)
            tab_z.append(z)
      if tab_x != []:
         self.plot_data.extend(axe.plot(tab_x, tab_y, tab_z, self.color, linewidth=1., label=self.title))

   def update(self):
      pass


class AxeBase (object):
   """
   A abstract base class for an Axe containing Line instances
   """
   def __init__(self, title, **kwargs):
      """
      Initialization of an Axe with its title

      Parameters
      ----------
      title : string
         Title of the Repere

      Tests
      -----
      >>> rep = AxeBase('Temperature')

      """
      self.title = title
      self.lines = []
      self.kwargs = kwargs

   def addLine(self, line):
      """
      Method wich registers a Line for rendering

      Parameters
      ----------
      line : Courbe or Courbe3D
         Line to plot

      Tests
      -----
      >>> line = Line('Sample Line', [0.], [0.])
      >>> axe = AxeBase('Sample Axe')
      >>> axe.addLine(line)

      """
      self.lines.append(line)

   def createAxe(self, fig, li,co,num_axe, **kwargs):
      """
      Method wich creates a matplotlib.axes.Axes instance to plot on.

      Parameters
      ----------
      fig : matplotlib.figure.Figure
         Figure the axe will belong to
      li : integer
         Number of rows on the figure
      co : integer
         Number of columns on the figure
      num_axe : integer
         Number of the axe. Number 1 will be in the upper left corner, number 2 will be at its right, etc
      **kwargs : Dictionnary
         Arguments passed to create the matplotlib.figure.Figure instance.
         It is documented in help(matplotlib.figure.Figure.add_subplot)

      Tests
      -----

      """
      self.axe = fig.add_subplot(li,co,num_axe, **kwargs)

   def render(self, fig, li,co,num_axe):
      """
      Main method of the AxeBase class to render the AxeBase on Board.
      Should not be called by the user. It is called automatically by the Board class.

      Parameters
      ----------
      fig : matplotlib.figure.Figure
         The matplotlib figure we will plot the axe on.
      li : integer
         Number of rows on the figure
      co : integer
         Number of columns on the figure
      num_axe : integer
         Number of the axe. Number 1 will be in the upper left corner, number 2 will be at its right, etc

      Tests
      -----

      """
      self.createAxe(fig, li,co,num_axe, **self.kwargs)

      for cb in self.lines:
         cb.render(self.axe)
         self.axe.set_title(self.title)
         self.axe.grid('on')

   def update(self):
      x_min = 1.0
      x_max = 0.
      y_min = 1.0
      y_max = 0.
      res = False
      for cb in self.lines:
         cb_up = cb.update()
         res = res or cb_up
         if cb.type == 'line2d' and cb_up:
            x_min_cb, y_min_cb = cb.get_min()
            x_max_cb, y_max_cb = cb.get_max()
            x_min=min(x_min,x_min_cb)
            y_min=min(y_min,y_min_cb)
            x_max=max(x_max,x_max_cb)
            y_max=max(y_max,y_max_cb)
      if res:
         self.axe.set_xbound(x_min,x_max)
         self.axe.set_ybound(y_min,y_max)
      return res


class Axe (AxeBase):
   """
   A concrete base class for an Axe containing Line instances
   """
   def __init__(self, title):
      AxeBase.__init__(self, title)


class Axe3D (AxeBase):
   """
   A concrete base class for an Axe containing Line3D instances
   """
   def __init__(self, title):
      AxeBase.__init__(self, title, projection = '3d')


class Map (AxeBase):
   """
   Specialized Axe which allows to plot on a map.
   """
   def __init__(self, title, **kwargs):
      """
      Initializer of the Map class.

      Parameters
      ----------
      title : string
         The title of the map
      **kwargs : dictionnary
         Optionnal arguments passed to mpl_toolkits.basemap.Basemap

      """
      self.proj = ccrs.Mercator(central_longitude=0.0, min_latitude=-80.0, max_latitude=84.0)
      kwargs['projection'] = self.proj
      AxeBase.__init__(self, title, **kwargs)

   def render(self, fig, li,co,num_axe):
      """
      Main method of the Map class to render the Map on Board.
      Should not be called by the user. It is called automatically by the Board class.

      Parameters
      ----------
      fig : matplotlib.figure.Figure
         The matplotlib figure we will plot the axe on.
      li : integer
         Number of rows on the figure
      co : integer
         Number of columns on the figure
      num_axe : integer
         Number of the axe. Number 1 will be in the upper left corner, number 2 will be at its right, etc

      Tests
      -----

      """
      AxeBase.render(self, fig, li,co,num_axe)
      self.axe.coastlines(resolution='110m')
      self.axe.gridlines()


class Board(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.parent = parent

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.axes = []
        
    def addAxe(self, axe):
        self.axes.append(axe)

    def render(self):
        """
        Main method of the Board class to render.
        Should not be called by the user. It is called automatically by the Window class.

        """
        li, co = auto_layout(len(self.axes))
        num_axe = 0
        for axe in self.axes:
           num_axe += 1
           axe.render(self.fig, li,co,num_axe)
        # self.fig.subplots_adjust(bottom=0.05, left=0.05, right=0.95, top=0.95, wspace=0, hspace=0)
        return self.fig

    def update(self):
        res = False
        for axe in self.axes:
           res = res or axe.update()
        # self.draw()
        return res


def test():
   import doctest

   doctest.testmod()


if __name__ == '__main__':
    test()
