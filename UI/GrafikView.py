from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Islemler,Ayarlar

class GrafikVieww(QGraphicsView):
     def __init__(self,gs,*args,**kwargs):
          super().__init__(gs,*args,**kwargs)
          self.gs=gs
          
          self.scale(1.0,-1.0) #koordinatların düzelmesi için
     
          self.pan=bool
          self.panBaslamaX=0
          self.panBaslamaY=0
          self.setMouseTracking(True)
          #self.verticalScrollBar().setValue(-500)
          self.pixelBoyutBul()
          

     
     
     def pixelBoyutBul(self):
          pos1=QPoint(0,0)
          pos2=QPoint(1,0)
          nokta1=self.mapToScene(pos1)
          nokta2=self.mapToScene(pos2)
          pixelboyut=Islemler.cizgiUzunlukBul(nokta1,nokta2)
          Ayarlar.cizgiBoundMesafe=int(pixelboyut*Ayarlar.cizgiBoundMesafeAyar)
          Ayarlar.tutamacYaricap=int(pixelboyut*Ayarlar.tutamacYaricapAyar)
          Ayarlar.nYakalamaYaricap=int(pixelboyut*Ayarlar.nYakalamaYaricapAyar)
          return pixelboyut
     
     def wheelEvent(self, event):
          zoomInFactor = 1.05
          zoomOutFactor = 0.95
          

          if event.angleDelta().y() > 0:
              zoomFactor = zoomInFactor
              pixelboyut=self.pixelBoyutBul()
          else:
              zoomFactor = zoomOutFactor
              pixelboyut=self.pixelBoyutBul()
          self.scale(zoomFactor, zoomFactor)
          
     def mousePressEvent(self, event):
          QGraphicsView.mousePressEvent(self,event)
          if event.button()==Qt.MidButton:
               self.pan=True
               self.panBaslamaX=event.x()
               self.panBaslamaY=event.y()
          else:
               self.pan=False
     def mouseReleaseEvent(self, event):
          QGraphicsView.mouseReleaseEvent(self,event)
          self.pan=False

     def mouseMoveEvent(self, event):
          QGraphicsView.mouseMoveEvent(self,event)
          if self.pan==True:
               self.horizontalScrollBar().setValue(self.horizontalScrollBar().value()-(event.x()-self.panBaslamaX))  
               self.verticalScrollBar().setValue(self.verticalScrollBar().value()-(event.y()-self.panBaslamaY))  
               self.panBaslamaX=event.x()
               self.panBaslamaY=event.y()
          else:
               self.pan=False
          