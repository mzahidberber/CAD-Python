from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar.Ayarlar import *


class OnIzlemeCizgi(QGraphicsObject):
     def __init__(self,gs,p1,fareN,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.gs=gs
          self.p1=p1
          self.fareN=fareN

          self.katmanObjesi=self.gs.katman

          self.kalem=self.katmanObjesi.seciliKatman.eBilgi["kalem"]

          self.eBilgi={
               "p1":self.p1,
               "fareN":self.fareN,
               "kalem":self.kalem
          }

     def kalemDegistir(self,kalem):
          self.eBilgi["kalem"]=kalem
      
     def noktalariYenile(self,p1,p2):
          self.eBilgi["p1"]=p1
          self.eBilgi["fareN"]=p2
     
     def paint(self, painter,option, widget):
          painter.setPen(self.eBilgi["kalem"])
          painter.drawLine(self.eBilgi["p1"],self.eBilgi["fareN"])
          
     def boundingRect(self):
          self.kare=QRectF(self.eBilgi["p1"],self.eBilgi["fareN"])
          return self.kare

class OnIzlemeSCizgi(QGraphicsObject):
     def __init__(self,gs,noktaL,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.gs=gs
          self.noktaL=noktaL

          self.katmanObjesi=self.gs.katman

          self.kalem=self.katmanObjesi.seciliKatman.eBilgi["kalem"]

          self.eBilgi={
               "noktalar":self.noktaL,
               "kalem":self.kalem
          }

     def kalemDegistir(self,kalem):
          self.eBilgi["kalem"]=kalem
      
     def noktalariYenile(self,noktaL):
          self.eBilgi["noktalar"]=noktaL
     
     def paint(self, painter,option, widget):
          painter.setPen(self.eBilgi["kalem"])
          cizgiListesi=[]
          if len(self.eBilgi["noktalar"])>=1:
               i=0
               while i<len(self.eBilgi["noktalar"])-1:
                    cizgiListesi.append((self.eBilgi["noktalar"][i],self.eBilgi["noktalar"][i+1]))
                    i+=1
               for i in cizgiListesi:
                    line=QLineF(i[0],i[1])
                    painter.drawLine(line)
     
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          p=QPainterPath()
          
          if len(self.eBilgi["noktalar"])>=1:
               p.moveTo(self.eBilgi["noktalar"][0])
               for i in self.eBilgi["noktalar"]:
                    if i==self.eBilgi["noktalar"][0]:
                         continue
                    p.lineTo(i)
          return p

class OnIzlemeCember(QGraphicsObject):
     def __init__(self,gs,merkez,r,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.gs=gs
          self.merkez=merkez
          self.r=r

          self.katmanObjesi=self.gs.katman
          self.kalem=self.katmanObjesi.seciliKatman.eBilgi["kalem"]

          self.eBilgi={
               "merkez":self.merkez,
               "yaricap":self.r,
               "kalem":self.kalem
          }
     def kalemDegistir(self,kalem):
          self.eBilgi["kalem"]=kalem
     
     def noktalariYenile(self,p1,r):
          self.eBilgi["merkez"]=p1
          self.eBilgi["yaricap"]=r
     
     def paint(self, painter,option, widget):
          painter.setPen(self.eBilgi["kalem"])
          painter.drawEllipse(self.kare)
          
     def boundingRect(self):
          p1=self.eBilgi["merkez"]-QPointF(self.eBilgi["yaricap"],self.eBilgi["yaricap"])
          p2=self.eBilgi["merkez"]+QPointF(self.eBilgi["yaricap"],self.eBilgi["yaricap"])
          self.kare=QRectF(p1,p2)
          return self.kare

class OnIzlemeElips(QGraphicsObject):
     def __init__(self,gs,merkez,r1,r2,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.gs=gs
          self.merkez=merkez
          self.r1=r1
          self.r2=r2

          self.katmanObjesi=self.gs.katman

          self.kalem=self.katmanObjesi.seciliKatman.eBilgi["kalem"]

          self.eBilgi={
               "merkez":self.merkez,
               "r1":self.r1,
               "r2":self.r2,
               "kalem":self.kalem
          }

     def kalemDegistir(self,kalem):
          self.eBilgi["kalem"]=kalem
     
     def noktalariYenile(self,p1,r1,r2):
          self.eBilgi["merkez"]=p1
          self.eBilgi["r1"]=r1
          self.eBilgi["r2"]=r2
     
     def paint(self, painter,option, widget):
          painter.setPen(self.eBilgi["kalem"])
          painter.drawEllipse(self.eBilgi["merkez"],self.eBilgi["r1"],self.eBilgi["r2"])
          
     def boundingRect(self):
          p1=self.eBilgi["merkez"]-QPointF(self.eBilgi["r1"],self.eBilgi["r2"])
          p2=self.eBilgi["merkez"]+QPointF(self.eBilgi["r1"],self.eBilgi["r2"])
          self.kare=QRectF(p1,p2)
          return self.kare

class OnIzlemeDikdortgen(QGraphicsObject):
     def __init__(self,gs,noktaL,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.gs=gs
          self.noktaL=noktaL

          self.katmanObjesi=self.gs.katman

          self.kalem=self.katmanObjesi.seciliKatman.eBilgi["kalem"]

          self.eBilgi={
               "noktalar":self.noktaL,
               "kalem":self.kalem
          }
      
     def noktalariYenile(self,noktaL):
          self.noktaL=noktaL
     def paint(self, painter,option, widget):
          painter.setPen(self.eBilgi["kalem"])
          painter.drawPath(self.shape())
     
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          p=QPainterPath()
          
          if len(self.noktaL)>=1:
               p.moveTo(self.noktaL[0])
               for i in self.noktaL:
                    if i==self.noktaL[0]:
                         continue
                    p.lineTo(i)
               p.lineTo(self.noktaL[0])
          return p

class OnIzlemeDikdortgenSecim(QGraphicsObject):
     def __init__(self,noktaL,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.noktaL=noktaL

          self.tarama=onIzlemeDikdortgenTarama
          self.kalem=onIzlemeCizgiKalem
     
     def noktalariYenile(self,noktaL):
          self.noktaL=noktaL
     
     def paint(self, painter,option, widget):
          painter.setPen(self.kalem)
          painter.setBrush(self.tarama)
          painter.setOpacity(0.5)
          painter.drawPath(self.shape())
     
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          p=QPainterPath()
          if len(self.noktaL)>=1:
               p.moveTo(self.noktaL[0])
               for i in self.noktaL:
                    if i==self.noktaL[0]:
                         continue
                    p.lineTo(i)
          return p
