from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Ayarlar,Islemler


class Tutamac(QGraphicsObject):
     hareketSinyal=pyqtSignal(object)
     def __init__(self,tahta,ortaN,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.tahta=tahta
          self.ortaN=ortaN
          self.eBilgi={
               "id":int,
               "tip":"Tutamac",
               "konum":None,
               "noktalar":None,
               "katman":None,
               "kalem":Ayarlar.tutamacKalem,
               "tarama":Ayarlar.tutamacTarama,
               "yaricap":Ayarlar.tutamacYaricap
          }
          self.eBilgi["noktalar"]=self.ortaN
          self.ynoktasi=[]
          self.setFlag(QGraphicsObject.ItemIsMovable)
          #self.setFlag(QGraphicsObject.ItemSendsScenePositionChanges)

     def paint(self, painter,option, widget):
          painter.setPen(self.eBilgi["kalem"])
          painter.setBrush(self.eBilgi["tarama"])
          painter.drawEllipse(self.shape().boundingRect())
          #painter.drawRect(self.shape().boundingRect())
     
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          p=QPainterPath()
          if Ayarlar.tutamacYaricap<1:
               Ayarlar.tutamacYaricap=1
          self.eBilgi["yaricap"]=Ayarlar.tutamacYaricap
          self.kp1=self.ortaN+QPointF(-Ayarlar.tutamacYaricap,-Ayarlar.tutamacYaricap)
          self.kp2=self.ortaN+QPointF(Ayarlar.tutamacYaricap,-Ayarlar.tutamacYaricap)
          self.kp3=self.ortaN+QPointF(Ayarlar.tutamacYaricap,Ayarlar.tutamacYaricap)
          self.kp4=self.ortaN+QPointF(-Ayarlar.tutamacYaricap,Ayarlar.tutamacYaricap)
          p.moveTo(self.kp1)
          p.lineTo(self.kp2)
          p.lineTo(self.kp3)
          p.lineTo(self.kp4)
          p.lineTo(self.kp1)
          return p

     def hoverLeaveEvent(self, event):
          QGraphicsObject.hoverLeaveEvent(self,event)
          self.eBilgi["tarama"]=Ayarlar.tutamacTarama
          self.eBilgi["kalem"]=Ayarlar.tutamacKalem
     
     def hoverEnterEvent(self, event):
          QGraphicsObject.hoverEnterEvent(self,event)
          self.eBilgi["tarama"]=Ayarlar.tutamacIsaretlemeTar
          self.eBilgi["kalem"]=Ayarlar.tutamacIsaretlemeKal

     def mousePressEvent(self,event):
          QGraphicsObject.mousePressEvent(self,event)
          self.fareTakipBasla()

     def mouseReleaseEvent(self, event):
          QGraphicsObject.mouseReleaseEvent(self,event)
          if len(self.ynoktasi)!=0:
               self.eBilgi["noktalar"]=self.ynoktasi[1]
          else:
               self.eBilgi["noktalar"]=self.shapeOrtaNoktaBulma()
          self.hareketSinyal.emit([self.eBilgi["id"],self.eBilgi["konum"],self.eBilgi["noktalar"]])
          self.fareTakipBitir()
     
     def mouseMoveEvent(self, event):
          QGraphicsObject.mouseMoveEvent(self,event)
          self.eBilgi["noktalar"]=self.shapeOrtaNoktaBulma()
          self.hareketSinyal.emit([self.eBilgi["id"],self.eBilgi["konum"],self.eBilgi["noktalar"]])

     def shapeOrtaNoktaBulma(self):
          pozisyonKare=self.mapRectToScene(self.shape().boundingRect())
          koordinatlar=pozisyonKare.getCoords()
          x1,y1,x2,y2=koordinatlar[0],koordinatlar[1],koordinatlar[2],koordinatlar[3]
          ortaNokta=QPointF(x1+self.eBilgi["yaricap"],y1+self.eBilgi["yaricap"])
          return ortaNokta

     def yakalamaNoktasiAl(self,ev,ynokta):
          self.ynoktasi=ynokta
     
     def fareTakipBasla(self):
          self.tahta.fareHareketKoordinat.connect(self.yakalamaNoktasiAl)

     def fareTakipBitir(self):
          self.tahta.fareHareketKoordinat.disconnect(self.yakalamaNoktasiAl)

class BoyutlandirmaTutamac(Tutamac):
     def __init__(self,tahta,ortaN,parent=None):
          Tutamac.__init__(self,tahta,ortaN,parent)
          self.tahta=tahta
          self.ortaN=ortaN
     
     def mouseReleaseEvent(self, event):
          QGraphicsObject.mouseReleaseEvent(self,event)
          if len(self.ynoktasi)!=0:
               self.eBilgi["noktalar"]=self.ynoktasi[1]
          else:
               self.eBilgi["noktalar"]=event.scenePos()
          self.hareketSinyal.emit([self.eBilgi["id"],self.eBilgi["konum"]])
     
     def mouseMoveEvent(self, event):
          QGraphicsObject.mouseMoveEvent(self,event)
          self.eBilgi["noktalar"]=event.scenePos()
          self.hareketSinyal.emit([self.eBilgi["id"],self.eBilgi["konum"]])