from PyQt5 import QtGui,QtCore


RENKLER={
          "b":QtGui.QColor(255,255,255),
          "k":QtGui.QColor(211,0,0),
          "t":QtGui.QColor(255,127,0),
          "m":QtGui.QColor(99,184,255),
          "s":QtGui.QColor(0,0,0),
          "g":QtGui.QColor(153,153,153),
          "y":QtGui.QColor(74,128,77),
     }

KALEMTIPLERI={
     "duz":QtCore.Qt.SolidLine,
     "kesikli":QtCore.Qt.DashLine,
     "noktali":QtCore.Qt.DotLine,
     "noktalikesikli":QtCore.Qt.DashDotLine,
     "ikinoktalikesikli":QtCore.Qt.DashDotDotLine
}

def Kalem(kalinlik,renk:QtGui.QColor,tip):
     # color=QtGui.QColor()
     # for i in RENKLER:
     #      if i==renk:
     #           color=RENKLER[i]
     for i in KALEMTIPLERI:
          if i==tip:
               kalemTipi=KALEMTIPLERI[i]
     kalem=QtGui.QPen()
     kalem.setWidthF(kalinlik)
     kalem.setColor(renk)
     kalem.setStyle(kalemTipi)
     kalem.setCosmetic(True)

     return kalem

def Tarama(renk:QtGui.QColor):
     # color=QtGui.QColor()
     # for i in RENKLER:
     #      if i==renk:
     #           color=RENKLER[i]
     tarama=QtGui.QBrush()
     tarama.setColor(renk)
     tarama.setStyle(QtCore.Qt.SolidPattern)

     return tarama
 