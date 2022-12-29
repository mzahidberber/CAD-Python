from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Komutlar.Yardimcilar import Ayarlar,Islemler


class AciYakalama:
     def __init__(self,pencere,gs):
          self.gs=gs
          self.pencere=pencere

          self.eBilgi={
               "x":bool,
               "y":bool,
               "aci":bool,
               "acid":float
          }

          self.onIzlemeEkle()
     
     def tarama(self,ev):
          self.taramaN=ev.scenePos()
          #taramaAlan=QRectF((self.taramaN-self.yaricapn).x(),(self.taramaN-self.yaricapn).y(),self.yaricap*2,self.yaricap*2)
          #tarananObjeler=self.gs.items(taramaAlan)
          #return tarananObjeler

     def aciYakalama(self,tiknoktasi,ev):
          dikx=self.xYakalama(tiknoktasi,ev)
          diky=self.yYakalama(tiknoktasi,ev)
          acinokta=self.aciYakalamaBul(tiknoktasi,ev)
          
          enYakinNokta=self.enYakinNoktaBul(dikx+diky+acinokta)
          return enYakinNokta

     def enYakinNoktaBul(self,noktaListesi):
          if len(noktaListesi)!=0:
               uzunlukL=[]
               for i in noktaListesi:
                    uzunluk=Islemler.cizgiUzunlukBul(self.taramaN,i)
                    uzunlukL.append(uzunluk)
               indeks=uzunlukL.index(min(uzunlukL))
               enyakinnokta=[noktaListesi[indeks]]
               return enyakinnokta
          return []

     def onIzlemeCizgiP3Bulma(self,egim,x1,y1):
          a=egim
          b=-1
          c=(-egim*x1)+y1
          p3=Islemler.ikinciDerecedenDenklemCozumu(a,b,c)
          return p3
     def aciYakalamaBul(self,tiklanannokta,ev):
          if self.eBilgi["aci"]==True:
               self.tarama(ev)
               self.eBilgi["acid"]=float(self.pencere.ui.aciYakalamaDerece.value())
               #print(tiklanannokta,self.taramaN)
               # egim=Islemler.dogruEgimBulma(self.taramaN,tiklanannokta)
               # onizlemep2=self.onIzlemeCizgiP3Bulma(egim,tiklanannokta.x(),tiklanannokta.y())
               # print(onizlemep2)
               #self.onIzlemeGuncelle(tiklanannokta,QPointF(onizlemep2[0],onizlemep2[1]))
               return []
          else:
               return []
     
     
     def xYakalama(self,tiklanannokta,ev):
          if self.eBilgi["x"]==True:
               self.tarama(ev)
               xnokta=[QPointF(self.taramaN.x(),tiklanannokta.y())]
               return xnokta
          else:
               return []

     def yYakalama(self,tiklanannokta,ev):
          if self.eBilgi["y"]==True:
               self.tarama(ev)
               ynokta=[QPointF(tiklanannokta.x(),self.taramaN.y())]
               return ynokta
          else:
               return []

     def onIzlemeEkle(self):
          self.onIzlemeCizgi=acOnIzleme(QPointF(),QPointF())
          self.onIzlemeCizgi.setVisible(False)
          self.gs.addItem(self.onIzlemeCizgi)

     def onIzlemeGuncelle(self,p1,p2):
          if self.eBilgi["aci"]==True:
               self.onIzlemeCizgi.setVisible(True)
               self.onIzlemeCizgi.p1=p1
               self.onIzlemeCizgi.p2=p2
     
     def onIzlemeSil(self):
          self.onIzlemeCizgi.p1=QPointF()
          self.onIzlemeCizgi.p2=QPointF()
          self.onIzlemeCizgi.setVisible(False)

class acOnIzleme(QGraphicsObject):
     def __init__(self,p1,p2,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.p1=p1
          self.p2=p2

     def paint(self, painter,option, widget):
          painter.setPen(Ayarlar.aciYKalem)
          painter.drawPath(self.shape())

     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          p=QPainterPath()
          if Ayarlar.nYakalamaYaricap<1:
               Ayarlar.nYakalamaYaricap=1
          p.moveTo(self.p1)
          p.lineTo(self.p2)
          return p

