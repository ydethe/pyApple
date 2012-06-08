# -*- coding: latin-1 -*-

from base_reader import *


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
      while line <> '':
         dat = line.strip().split(' ')
         while '' in dat:
            dat.remove('')
         dat = map(float,dat)
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
      
