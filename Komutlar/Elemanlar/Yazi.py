from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Ayarlar
from Komutlar.Elemanlar.AnaEleman import CizimElemani 


class Yazi(CizimElemani):
     def __init__(self,p1,metin,parent=None):
          CizimElemani.__init__(self,parent)


     def paint(self, painter,option, widget):
          painter.setPen(self.kalem)
          
          painter.drawText()
          painter.drawPath(self.shape())
          
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          painterStrock=QPainterPathStroker()
          painterStrock.setWidth(Ayarlar.cizgiBoundMesafe)
          p=QPainterPath()
          
          p.moveTo(self.p1.x(),self.p1.y())
          
          path1=painterStrock.createStroke(p)
          
          return path1 