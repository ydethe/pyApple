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

import wx

from pyApple.graph_elem import *
import time


class AppleFrame(wx.Frame):
   """
   This is the main widget embedded in the app's windows.
   It inherits from wx.Frame.
   The user should not manipulate it, because this is handled by the AppleWindow class.
   """
   def __init__(self, app, *args, **kwds):
      """
      Initializes an instance of AppleFrame.
      Should not be called by the user.
      The arguments are the same as in wx.Frame's constructor.

      """
      kwds["style"] = wx.DEFAULT_FRAME_STYLE
      wx.Frame.__init__(self, *args, **kwds)

      self.app = app

      self.Bind(wx.EVT_SIZE, self.OnSize)
      self.Bind(wx.EVT_MOVE, self.OnMove)
      self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
      self.Bind(wx.EVT_IDLE, self.OnIdle)

      self.notebook = wx.Notebook(self, -1, style=0)

      self.__set_properties()
      self.__do_layout()

      self.__boards = []

   def __set_properties(self):
      self.SetTitle("pyApple")

   def __do_layout(self):
      main_sizer = wx.BoxSizer(wx.HORIZONTAL)
      sizer_1 = wx.BoxSizer(wx.VERTICAL)
      main_sizer.Add(self.notebook, 1, wx.EXPAND, 0)
      self.SetSizer(main_sizer)
      main_sizer.Fit(self)
      self.Layout()

   def createBoard(self, titre):
      pl = Board(self.notebook, -1, name=titre)
      self.notebook.AddPage(pl,titre)
      self.__boards.append(pl)
      return pl

   def render(self):
      for pl in self.__boards:
         pl.render()

   def update(self):
      res = False
      for pl in self.__boards:
         res = res or pl.update()
      return res

   def OnCloseWindow(self, event):
      self.app.keepGoing = False
      self.Destroy()

   def OnIdle(self, event):
      pass

   def OnSize(self, event):
      size = event.GetSize()
      # self.sizeCtrl.SetValue("%s, %s" % (size.width, size.height))
      event.Skip()

   def OnMove(self, event):
      pos = event.GetPosition()
      # self.posCtrl.SetValue("%s, %s" % (pos.x, pos.y))


class AppleWindow(wx.PySimpleApp):
   """
   This is the object describing the app's windows.
   It inherits from wx.PySimpleApp.
   The user creates boards from it, and does not have to instanciate a Board instance manually.
   """
   def OnInit(self):
      """
      This method is automatically called by wxPython before displaying the window.
      It sets up the AppleFrame. The user never calls it himself.
      """
      print("Creation AppleFrame")
      self.frame = AppleFrame(self, None, -1, "pyApple")
      self.frame.Show(True)
      self.SetTopWindow(self.frame)

      self.keepGoing = True

      return True

   def createBoard(self, titre):
      """
      This method creates a new board, with given title.

      Parameters
      ----------
      titre : string
         Title of the new board

      Returns
      -------
      bd : Board
         An empty Board instance

      """
      return self.frame.createBoard(titre)

   def display(self):
      """
      This method displays the application.
      It should not be called before all the boards, axes and lines are set up.

      """
      self.frame.render()

      self.frame.Maximize()
      self.MainLoop()

   def MainLoop(self):
      # Create an event loop and make it active.  If you are
      # only going to temporarily have a nested event loop then
      # you should get a reference to the old one and set it as
      # the active event loop when you are done with this one...
      evtloop = wx.EventLoop()
      old = wx.EventLoop.GetActive()
      wx.EventLoop.SetActive(evtloop)

      # This outer loop determines when to exit the application,
      # for this example we let the main frame reset this flag
      # when it closes.
      while self.keepGoing:
         # At this point in the outer loop you could do
         # whatever you implemented your own MainLoop for.  It
         # should be quick and non-blocking, otherwise your GUI
         # will freeze.

         # t1 = time.time()
         self.frame.update()
         # t2 = time.time()
         # print 'Frame updated in ',(t2-t1),'s'

         # This inner loop will process any GUI events
         # until there are no more waiting.
         while evtloop.Pending():
             evtloop.Dispatch()

         # Send idle events to idle handlers.  You may want to
         # throttle this back a bit somehow so there is not too
         # much CPU time spent in the idle handlers.  For this
         # example, I'll just snooze a little...
         time.sleep(0.10)
         self.ProcessIdle()

      wx.EventLoop.SetActive(old)



def test():
   import doctest

   doctest.testmod()


if __name__ == '__main__':
    test()
