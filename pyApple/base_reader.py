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

import numpy as np
import sys
import os
from math import *

from pyApple.aplCommon import *


class Datagram (list):
   def __init__(self, elem=[]):
      list.__init__(self,elem)

   def update(self):
      pass

   def __add__(self, data):
      return [x+y for x,y in zip(self.val,data)]

   def __sub__(self, data):
      return [x-y for x,y in zip(self.val,data)]

   def __mul__(self, data):
      return [x*y for x,y in zip(self.val,data)]

   def __div__(self, data):
      return [x/y for x,y in zip(self.val,data)]

   def __rmul__(self, scal):
      return [x*scal for x,y in self.val]



class ReaderBase (object):
   """
   This class is the base class for any Reader class.
   A Reader class is a class whcih implements the ability of reading files.
   A few rules are to be respected :

   + Each derived class must impliement the actual parsing into the __init__ method
   + All the data available for plotting must be put into the self.data dictionnary
        For example, a data file containing one array for the time ('time'),
        and one array for the temperature ('temp') will fill the self.data dictionnary
        with self.data['time'] = [...our time array...]
        with self.data['temp'] = [...our temp array...]
   + (Optionnal) The values of the dictionnary can be converted from list to np.array.
        This is more convenient when you want for example sum two arrays.

   To read and parse, let's say a csv file which has two columns,
   you will have to declare a derived class CSV_Reader like this :

   ------------------------Example-------------------------------------

   class CSV_Reader (ReaderBase):
      def __init__(self, filename):
         ReaderBase.__init__(self)         # We call the constructor of the mother class

         file = open(filename, 'r')        # We open the file in read mode

         self.data['x'] = []
         self.data['y'] = []
         line = file.readline()            # We read the first line to initiate the main loop
         while line != '':
            vars = line.strip().split(',') # The strip method removes initial spaces, and final spaces and \n
            vars = map(float, vars)        # We convert everything into float
            self.data['x'].append(vars[0]) # We append the float to the data member of the class
            self.data['y'].append(vars[1])
            line = file.readline()         # We read the next line

         self.data['x'] = np.array(self.data['x']) # (Optionnal) We convert the data lists into np.array,
         self.data['y'] = np.array(self.data['y']) #     to ease future manipulations

         file.close()                      # Finally we close the file

   --------------------------------------------------------------------

   """
   __slots__ = ['data']
   def __init__(self):
      """
      Default initializer for the base class ReaderBase

      Tests
      -----
      >>> d = ReaderBase()

      """
      self.data = {}

   def get(self, name, formula=identity):
      """
      Returns the data named name, after applying the function formula
      to all the elements of this data.
      The return type is np.array.

      Parameters
      ----------
      name : string
         Name of the data field

      formula : function
         Function applied to the data field

      Returns
      -------
      data : np.array
         The data field, modified by the formula

      Tests
      -----
      >>> d = CSV_Reader('test.csv')
      >>> d.get('x', m_to_km)
      array([ 0.   ,  0.001,  0.002,  0.003,  0.004])

      """
      return np.array(map(formula, self.data[name]))

   def __getitem__(self, name):
      """
      Returns the data named name.

      Parameters
      ----------
      name : string
         Name of the data field

      Returns
      -------
      data : iterable object
         The data field

      Tests
      -----
      >>> d = CSV_Reader('test.csv')
      >>> d['x']
      array([ 0.,  1.,  2.,  3.,  4.])

      """
      return self.data[name]

   def find(self, name, val, eps=0):
      """
      Looks for val into the data field named name.
      The equality between val and an element of the data field x, is assumed when abs(val-x) <= eps

      Parameters
      ----------
      name : string
         Name of the data field

      val : A numerical value
         Value to look for

      Returns
      -------
      ind : integer
         The index of the value. Returns -1 if the value is not present.

      Tests
      -----
      >>> d = CSV_Reader('test.csv')
      >>> d.find('y', 1., 1.e-4)
      1

      """
      ecarts = map(lambda x: abs(x-val)<=eps, self.data[name])
      return ecarts.index(True)



def test():
   import doctest, os

   global CSV_Reader

   file = open('test.csv', 'w')
   for x in np.arange(0.,5.):
      y = x**2
      file.write(str(x)+', '+str(y)+'\n')
   file.close()

   # Definition d'une classe fille (dErivEe de ReaderBase) pour fournir un exemple d'implEmentation de la mEthode modele.
   class CSV_Reader (ReaderBase):
      def __init__(self, filename):
         ReaderBase.__init__(self)         # We call the constructor of the mother class

         file = open(filename, 'r')        # We open the file in read mode

         self.data['x'] = Datagram()
         self.data['y'] = Datagram()
         line = file.readline()            # We read the first line to initiate the main loop
         while line != '':
            vars = line.strip().split(',') # The strip method removes initial spaces, and final spaces and \n
            vars = map(float, vars)        # We convert everything into float
            self.data['x'].append(vars[0]) # We append the float to the data member of the class
            self.data['y'].append(vars[1])
            line = file.readline()         # We read the next line

         self.data['x'] = np.array(self.data['x']) # (Optionnal) We convert the data lists into np.array,
         self.data['y'] = np.array(self.data['y']) #     to ease future manipulations

         file.close()                      # Finally we close the file


   doctest.testmod()

   os.remove('test.csv')


if __name__ == '__main__':
    test()
