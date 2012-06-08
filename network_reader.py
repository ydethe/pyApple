# -*- coding: latin-1 -*-

from base_reader import *
from socket import *


class NetDatagram (Datagram):
   def __init__(self, reader):
      list.__init__(self)
      self.reader = reader
      
   def update(self):
      self.reader.update()
      

class NetworkReader (ReaderBase):
   def __init__(self, server):
      ReaderBase.__init__(self)

      self.socket = socket(AF_INET,SOCK_STREAM,0)
      self.socket.connect(server)
      self.socket.send('var_list')
      txt = self.socket.recv(255)
      self.var = txt.strip().split(',')
      for var in self.var:
         self.data[var] = NetDatagram(self)

      self.finished = False
      
   def start(self):
      self.socket.send('start')
      self.socket.setblocking(False)

   def update(self):
      if self.finished:
         return
      
      try:
         txt = self.socket.recv(8196)
      except:
         # Cas ou aucune donnee n'est presente dans le buffer
         return
      
      if txt == 'finished':
         self.finished = True
         self.socket.close()
         return
         
      lines = txt.strip().split('\n')
      for line in lines:
         dat = line.strip().split(',')
         dat = map(float,dat)

         for k, v in zip(self.var, dat):
            self.data[k].append(v)



