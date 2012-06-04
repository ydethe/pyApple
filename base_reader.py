# -*- coding: latin-1 -*-

import numpy as np
import sys
import os
from math import *

def id(x):
   return x
   
def m_to_km(x):
   return x/1000.
   
def rad_to_deg(x):
   return x*180./pi


class ReaderBase (object):
   __slots__ = ['data']
   def __init__(self, filename):
      self.data = {}
      
   def get(self, nom_var, formule=id):
      return map(formule, self.data[nom_var])
      
   def __getitem__(self, nom):
      return self.data[nom]
