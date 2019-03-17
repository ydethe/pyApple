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

from pyApple.base_reader import *


class Simple_Reader (ReaderBase):
   __slots__ = ['data']
   def __init__(self, filename):
      ReaderBase.__init__(self)

      file = open(filename, 'r')

      line = file.readline()
      # Saut entete
      while line[0] == '#':
         line = file.readline()

      # Lecture des données
      self.data['t'] = Datagram()
      self.data['x'] = Datagram()
      self.data['y'] = Datagram()
      self.data['z'] = Datagram()
      self.data['vx'] = Datagram()
      self.data['vy'] = Datagram()
      self.data['vz'] = Datagram()
      self.data['lat'] = Datagram()
      self.data['lon'] = Datagram()
      self.data['alt'] = Datagram()
      self.data['vit'] = Datagram()
      self.data['pen'] = Datagram()
      self.data['azi'] = Datagram()
      while line != '':
         elem = line.strip().split(' ')
         while '' in elem:
            elem.remove('')
         dat = [float(x) for x in elem]
         ind = 0
         self.data['t'].append(dat[ind]); ind += 1
         self.data['x'].append(dat[ind]); ind += 1
         self.data['y'].append(dat[ind]); ind += 1
         self.data['z'].append(dat[ind]); ind += 1
         self.data['vx'].append(dat[ind]); ind += 1
         self.data['vy'].append(dat[ind]); ind += 1
         self.data['vz'].append(dat[ind]); ind += 1
         self.data['lat'].append(dat[ind]); ind += 1
         self.data['lon'].append(dat[ind]); ind += 1
         self.data['alt'].append(dat[ind]); ind += 1
         self.data['vit'].append(dat[ind]); ind += 1
         self.data['pen'].append(dat[ind]); ind += 1
         self.data['azi'].append(dat[ind]); ind += 1
         line = file.readline()

      file.close()
