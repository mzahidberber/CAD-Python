from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Ayarlar
from Komutlar.Elemanlar.AnaEleman import CizimElemani 


class Olcu(CizimElemani):
     def __init__(self,p1,p2,mesafe,parent=None):
          CizimElemani.__init__(self,parent)

          self.p1=p1
          self.p2=p2
          self.mesafe=mesafe

          self.kalem=Ayarlar.olcuCizgiKalem
          self.yazi=Ayarlar.olcuYaziKalem

     def paint(self, painter,option, widget):
          painter.setPen(self.kalem)
          
          
          painter.drawPath(self.shape())
          
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          painterStrock=QPainterPathStroker()
          painterStrock.setWidth(Ayarlar.cizgiBoundMesafe)
          p=QPainterPath()
          
          p.moveTo(self.p1.x(),self.p1.y())
          p.arcTo(self.kare,-self.baslagicAci,-self.bitisAci)
          
          path1=painterStrock.createStroke(p)
          
          return path1 