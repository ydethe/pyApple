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

def identity(x):
   """
   Function which doesn't compute anything :-)
   Is used as the default argument of a new Courbe.

   Parameters
   ----------
   x : A numerical value
      A numerical value
   
   Returns
   -------
   y : A numerical value
      The same value than x
   
   Tests
   -----
   >>> identity(3.)
   3.0

   """
   return x
   
def m_to_km(x):
   """
   Conversion from meters to kilometers

   Parameters
   ----------
   x (m) : A numerical value
      x converted in km

   Returns
   -------
   y (km) : A numerical value
      x converted into km
   
   Tests
   -----
   >>> m_to_km(3000.)
   3.0

   """
   return x/1000.
   
def rad_to_deg(x):
   """
   Conversion from radians to degrees

   Parameters
   ----------
   x (rad) : A numerical value
      x converted in degrees

   Returns
   -------
   y (deg) : A numerical value
      x converted into deg
   
   Tests
   -----
   >>> rad_to_deg(pi/3.)
   59.999999999999993

   """
   return x*180./pi
   
   
   
   
def test():
   import doctest

   doctest.testmod()
   

if __name__ == '__main__':
    test()


