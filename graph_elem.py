# -*- coding: latin-1 -*-

from math import *
import numpy as np

import matplotlib
matplotlib.use('WXAgg')
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import Axes3D

from matplotlib.figure import Figure

import wx

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg
from matplotlib.backends.backend_wx import NavigationToolbar2Wx


def calc_repart_auto(nb_axes):
   li = int(round(sqrt(nb_axes)))
   co = int(ceil(float(nb_axes)/float(li)))
   # return li, co
   return co, li

   
def moy_pond(moys,ponds):
   tot = sum(ponds)
   moy = 0.
   for y, p in zip(moys, ponds):
      moy += y*p/tot
   return moy

class Courbe (object):
   def __init__(self, titre, var_x, var_y, couleur='b', formule_x=None, formule_y=None):
      self.titre = titre

      self.x = map(formule_x, var_x)
      self.y = map(formule_y, var_y)

      self.couleur = couleur
      if formule_x <> None:
         self.formule_x = formule_x
      else:
         self.formule_x = id
      if formule_y <> None:
         self.formule_y = formule_y
      else:
         self.formule_y = id

   def get_min(self):
      min_x = min(filter(lambda x:x>-999,self.x))
      min_y = min(filter(lambda x:x>-999,self.y))
      return min_x, min_y

   def get_max(self):
      max_x = max(filter(lambda x:x>-999,self.x))
      max_y = max(filter(lambda x:x>-999,self.y))
      return max_x, max_y

   def trace(self, axe, transf=None):
      tab_x = []
      tab_y = []
      for x, y in zip(self.x, self.y):
         if y < -999:
            if transf <> None:
               tab_x, tab_y = transf(tab_x, tab_y)
            axe.plot(tab_x, tab_y, self.couleur, linewidth=1., label=self.titre)
            tab_x = []
            tab_y = []
         else:
            tab_x.append(x)
            tab_y.append(y)
      if tab_x <> []:
         if transf <> None:
            tab_x, tab_y = transf(tab_x, tab_y)
         axe.plot(tab_x, tab_y, self.couleur, linewidth=1., label=self.titre)
         
   def moyenne(self, meth='trap', fct=id):
      """
      Calcul de la moyenne de la courbe.
      
      Le calcul est fait en intégrant la courbe, puis en divisant par la largeur de l'axe x.
      Une hypothese de calcul est que les valeurs de l'axe X sont croissantes. Si ce n'est pas le cas, la methode retourne -9999999
      
      L'argument meth designe la methode d(integration, et peut valoir :
      - 'trap' : integration par trapezes
      - 'gauche' : integration par rectangles de hauteur la valeur a gauche
      - 'droite' : integration par rectangles de hauteur la valeur a droite
      """
      tab_x = []
      tab_y = []
      moys = []
      ponds = []
      
      val_conv_data = -999.
      
      fin = len(tab_x)-1
      
      for x, y in zip(self.x, self.y):
         if y < val_conv_data:
            # Traitement ici
            if [tab_x[i+1]-tab_x[i] for i in range(len(tab_x)-1) if tab_x[i+1]-tab_x[i] < 0.] <> []:
               return -9999999
            integrale = 0.
            for i in range(fin):
               if meth == 'trap':
                  integrale += (tab_y[i] + tab_y[i+1])/2.*(tab_x[i+1] - tab_x[i])
               if meth == 'gauche':
                  integrale += tab_y[i]*(tab_x[i+1] - tab_x[i])
               if meth == 'droite':
                  integrale += tab_y[i+1]*(tab_x[i+1] - tab_x[i])
               if meth == 'simps':
                  x1 = tab_x[i]
                  x2 = tab_x[i+1]
                  x3 = tab_x[i+2]
                  y1 = tab_y[i]
                  y2 = tab_y[i+1]
                  y3 = tab_y[i+2]
                  a = (-x1*(y2-y3)+x2*(y1-y3)-x3*(y1-y2))/((x1-x3)*(x1-x2)*(x2-x3))
                  b = (x1**2*(y2-y3)-x2**2*(y1-y3)+x3**2*(y1-y2))/((x1-x3)*(x1-x2)*(x2-x3))
                  c = (x1**2*(x2*y3-x3*y2)-x1*(x2**2*y3-x3**2*y2)+x2*(x2-x3)*x3*y1)/((x1-x3)*(x1-x2)*(x2-x3))
                  integrale += a*(x2**3/3-x1**3/3) + b*(x2**2/2-x1**2/2) + c*(x2-x1)
            moys.append(integrale)
            ponds.append(max(tab_x) - min(tab_x))
            tab_x = []
            tab_y = []
         else:
            tab_x.append(x)
            tab_y.append(fct(y))
      if tab_x <> []:
         if tab_x[-1] < val_conv_data:
            tab_x = tab_x[:-1]
         # Traitement ici
         if [tab_x[i+1]-tab_x[i] for i in range(len(tab_x)-1) if tab_x[i+1]-tab_x[i] < 0.] <> []:
            return -9999999
         integrale = 0.
         for i in range(fin):
            if meth == 'trap':
               integrale += (tab_y[i] + tab_y[i+1])/2.*(tab_x[i+1] - tab_x[i])
            if meth == 'gauche':
               integrale += tab_y[i]*(tab_x[i+1] - tab_x[i])
            if meth == 'droite':
               integrale += tab_y[i+1]*(tab_x[i+1] - tab_x[i])
         moys.append(integrale)
         ponds.append(max(tab_x) - min(tab_x))
         
      return moy_pond(moys,ponds)
      
   def variance(self, meth='trap'):
      """
      Calcul de la variance de la courbe.
      
      Le calcul est fait en intégrant la courbe, puis en divisant par la largeur de l'axe x.
      Une hypothese de calcul est que les valeurs de l'axe X sont croissantes. Si ce n'est pas le cas, la methode retourne -9999999
      
      L'argument meth designe la methode d(integration, et peut valoir :
      - 'trap' : integration par trapezes
      - 'gauche' : integration par rectangles de hauteur la valeur a gauche
      - 'droite' : integration par rectangles de hauteur la valeur a droite
      """
      
      return self.moyenne(meth, lambda x:x**2) - self.moyenne(meth)**2


class Courbe3D (object):
   def __init__(self, titre, var_x, var_y, var_z, couleur='b', formule_x=None, formule_y=None, formule_z=None):
      self.titre = titre

      self.x = map(formule_x, var_x)
      self.y = map(formule_y, var_y)
      self.z = map(formule_z, var_z)

      self.couleur = couleur
      if formule_x <> None:
         self.formule_x = formule_x
      else:
         self.formule_x = id

      if formule_y <> None:
         self.formule_y = formule_y
      else:
         self.formule_y = id

      if formule_z <> None:
         self.formule_z = formule_z
      else:
         self.formule_z = id

   def get_min(self):
      min_x = min(filter(lambda x:x>-9999999,self.x))
      min_y = min(filter(lambda x:x>-9999999,self.y))
      min_z = min(filter(lambda x:x>-9999999,self.z))
      return min_x, min_y, min_z

   def get_max(self):
      max_x = max(filter(lambda x:x>-9999999,self.x))
      max_y = max(filter(lambda x:x>-9999999,self.y))
      max_z = max(filter(lambda x:x>-9999999,self.z))
      return max_x, max_y, max_z

   def trace(self, axe, transf=None):
      tab_x = []
      tab_y = []
      tab_z = []
      for x, y, z in zip(self.x, self.y, self.z):
         if y < -9999999:
            if transf <> None:
               tab_x, tab_y, tab_z = transf(tab_x, tab_y, tab_z)
            print tab_x
            print tab_y
            print tab_z
            axe.plot(tab_x, tab_y, tab_z, self.couleur, linewidth=1., label=self.titre)
            tab_x = []
            tab_y = []
            tab_z = []
         else:
            tab_x.append(x)
            tab_y.append(y)
            tab_z.append(z)
      if tab_x <> []:
         if transf <> None:
            tab_x, tab_y, tab_z = transf(tab_x, tab_y, tab_z)
         axe.plot(tab_x, tab_y, tab_z, self.couleur, linewidth=1., label=self.titre)


class RepereBase (object):
   def __init__(self, titre):
      self.titre = titre
      self.courbes = []
      self.projection = 'rectilinear'

   def ajCourbe(self, courbe):
      self.courbes.append(courbe)
      
   def creerAxe(self, li,co,num_axe, fig, **kwargs):
      self.axe = fig.add_subplot(li,co,num_axe, **kwargs)
      self.axe
      
   def trace(self, li,co,num_axe, fig):
      self.creerAxe(li,co,num_axe, fig, projection=self.projection)

      for cb in self.courbes:
         cb.trace(self.axe)
         self.axe.set_title(self.titre)
         self.axe.grid('on')
      
      
class Repere (RepereBase):
   def __init__(self, titre):
      RepereBase.__init__(self, titre)


class Repere3D (RepereBase):
   def __init__(self, titre):
      RepereBase.__init__(self, titre)
      self.projection = '3d'


# Options : llcrnrlon=None, llcrnrlat=None, urcrnrlon=None, urcrnrlat=None, llcrnrx=None, llcrnry=None, urcrnrx=None, urcrnry=None, width=None, height=None, projection='cyl', resolution='c', area_thresh=None, rsphere=6370997.0, lat_ts=None, lat_1=None, lat_2=None, lat_0=None, lon_0=None, lon_1=None, lon_2=None, no_rot=False, suppress_ticks=True, satellite_height=35786000, boundinglat=None, fix_aspect=True, anchor='C', celestial=False, ax=None)

# The desired projection is set with the proj keyword. Default is ``cyl``.
# Supported values for the projection keyword are:

# ==============   ====================================================
# Value            Description
# ==============   ====================================================
# aeqd             Azimuthal Equidistant
# poly             Polyconic
# gnom             Gnomonic
# moll             Mollweide
# tmerc            Transverse Mercator
# nplaea           North-Polar Lambert Azimuthal
# gall             Gall Stereographic Cylindrical
# mill             Miller Cylindrical
# merc             Mercator
# stere            Stereographic
# npstere          North-Polar Stereographic
# hammer           Hammer
# geos             Geostationary
# nsper            Near-Sided Perspective
# vandg            van der Grinten
# laea             Lambert Azimuthal Equal Area
# mbtfpq           McBryde-Thomas Flat-Polar Quartic
# sinu             Sinusoidal
# spstere          South-Polar Stereographic
# lcc              Lambert Conformal
# npaeqd           North-Polar Azimuthal Equidistant
# eqdc             Equidistant Conic
# cyl              Cylindrical Equidistant
# omerc            Oblique Mercator
# aea              Albers Equal Area
# spaeqd           South-Polar Azimuthal Equidistant
# ortho            Orthographic
# cass             Cassini-Soldner
# splaea           South-Polar Lambert Azimuthal
# robin            Robinson

# ==============   ====================================================
class Carte (RepereBase):
   def __init__(self, titre, auto, **kwargs):
      RepereBase.__init__(self, titre)
      self.args = kwargs
      self.auto = auto

   def trace(self, li,co,num_axe, fig):

      self.creerAxe(li,co,num_axe, fig)

      if self.auto:
         lat_min = 360.
         lat_max = -360.
         lon_min = 360
         lon_max = -360.
         for cb in self.courbes:
            lon_min_cb, lat_min_cb = cb.get_min()
            lon_max_cb, lat_max_cb = cb.get_max()

            lat_min = min(lat_min,lat_min_cb)
            lat_max = max(lat_max,lat_max_cb)
            lon_min = min(lon_min,lon_min_cb)
            lon_max = max(lon_max,lon_max_cb)

         rnd = 10.0
         self.args['llcrnrlat'] = rnd*floor(lat_min/rnd)
         self.args['urcrnrlat'] = rnd*ceil(lat_max/rnd)
         self.args['llcrnrlon'] = rnd*floor(lon_min/rnd)
         self.args['urcrnrlon'] = rnd*ceil(lon_max/rnd)
         # self.args['width'] = (lon_max-lon_min)*pi/180.*6378137.*0.5
         # self.args['height'] = (lat_max-lat_min)*pi/180.*6378137.*0.5
         self.args['lon_0'] = -40
         self.args['lat_1'] = 30

      self.args['rsphere'] = (6378137., 6356752.3142)
      self.args['ax'] = self.axe
      carte = Basemap(**self.args)

      # draw coastlines, country boundaries, fill continents.
      carte.drawcoastlines()
      carte.drawcountries()
      carte.fillcontinents(color='coral')

      # draw the edge of the map projection region (the projection limb)
      carte.drawmapboundary()

      # draw lat/lon grid lines every 10 degrees.
      carte.drawmeridians(np.arange(-180, 180, 10),labels=[0,0,0,1])
      carte.drawparallels(np.arange(-90, 90, 10),labels=[1,0,0,0])

      for cb in self.courbes:
         cb.trace(carte, carte)
         self.axe.set_title(self.titre)
         # self.axe.grid('on')


class Planche (wx.Panel):
   def __init__(self, *args, **kwd):
      wx.Panel.__init__(self, *args, **kwd)

      self.fig = Figure((19,12), 75)
      self.canvas = FigureCanvasWxAgg(self, -1, self.fig)
      self.canvas.mpl_connect('motion_notify_event', self.on_move)
      self.canvas.mpl_connect('button_release_event', self.on_mouse_release)
      self.toolbar = NavigationToolbar2Wx(self.canvas)
      self.toolbar.Realize()

      # On Windows, default frame size behaviour is incorrect
      # you don't need this under Linux
      tw, th = self.toolbar.GetSizeTuple()
      fw, fh = self.canvas.GetSizeTuple()
      self.toolbar.SetSize(wx.Size(fw, th))

      self.mouse_pos_label = wx.StaticText(self, -1, "")
      
      # Create a figure manager to manage things

      # Now put all into a sizer
      sizer = wx.BoxSizer(wx.VERTICAL)
      sizer_nav = wx.FlexGridSizer(1, 3, 0, 0)

      # This way of adding to sizer allows resizing
      sizer.Add(self.canvas, 1, wx.LEFT|wx.TOP|wx.GROW)
      sizer.Add(sizer_nav, 0, wx.GROW)
      
      # Best to allow the toolbar to resize!
      sizer_nav.Add(self.toolbar, 0, wx.ALL, 4)
      sizer_nav.Add(wx.Panel(self,-1), 0, wx.ALL, 4)
      sizer_nav.Add(self.mouse_pos_label, 0, wx.ALL, 4)
      sizer_nav.Fit(self)
      sizer_nav.AddGrowableCol(1)
      self.SetSizer(sizer)
      self.Fit()

      self.reperes = []

   def on_move(self, event):
      if event.ydata <> None:
         self.mouse_pos_label.SetLabel('x='+str(event.xdata)+', y='+str(event.ydata))
      
   def on_mouse_release(self, event):
      print event.button
   
   def GetToolBar(self):
      # You will need to override GetToolBar if you are using an
      # unmanaged toolbar in your frame
      return self.toolbar

   def onEraseBackground(self, evt):
      # this is supposed to prevent redraw flicker on some X servers...
      pass

   def ajRepere(self, repere):
      self.reperes.append(repere)

   def trace(self):
      li, co = calc_repart_auto(len(self.reperes))
      num_axe = 0
      for rep in self.reperes:
         num_axe += 1
         rep.trace(li,co,num_axe, self.fig)
      # self.fig.subplots_adjust(bottom=0.05, left=0.05, right=0.95, top=0.95, wspace=0, hspace=0)
      return self.fig









