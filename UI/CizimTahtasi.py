from PyQt5.QtWidgets import QGraphicsScene,QGraphicsRectItem,QShortcut
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import NoktaYakalama,Ayarlar,AciYakalama,Katman
from Komutlar.Yardimcilar.ElemanSecme import Secme,SecimKutusuCizim
from Kayit import Kayit,DXF
import math,sys

class CizimTahtasii(QGraphicsScene):

     fareTiklamaKoordinat = pyqtSignal(object)
     fareHareketKoordinat = pyqtSignal(object,object)
     
     def __init__(self,arayuz,*args, **kwargs):
          super().__init__(*args, **kwargs)
          self.arayuz=arayuz
          self.setSceneRect(-10000,-10000,20000,20000)
          #sys.setrecursionlimit(1100)

          self.cizilenElemanListesi=[]
          
          self.ny=NoktaYakalama.NoktaYakalama(self)
          self.yn=None
          self.ay=AciYakalama.AciYakalama(self.arayuz,self)
          self.katman=Katman.KatmanDuzenle(self.arayuz,self)
          self.kayit=Kayit.Yazma(self)
          self.dxfKayit=DXF.DXFOkuma(self)

          
          self.xykalem=Ayarlar.XYAksKalem
          self.gridkalem=Ayarlar.gridKalem
          self.gridtarama=Ayarlar.gridTarama

          self.secimObjesi=Secme(self)
     
     def elemanEkle(self,eleman):
          self.addItem(eleman)
          self.cizilenElemanListesi.append(eleman)

     def elemanSil(self,eleman):
          self.removeItem(eleman)
          self.cizilenElemanListesi.remove(eleman)

     def cizilenElemanListesiBilgi(self):
          return self.cizilenElemanListesi
     
     def sahneGuncelleme(self):
          #sahneBoyut=self.itemsBoundingRect()
          sahneBoyut=self.sceneRect()
          self.update(sahneBoyut)
          self.elemanBilgiListeDuzenle()
          
     def arkaplanGrid(self,p1,p2):
          ekranYatayUzunluk=p2.x()-p1.x()
          logYU=math.log10(ekranYatayUzunluk)
          x1,y1,x2,y2=p1.x(),p1.y(),p2.x(),p2.y()
          deger,deger1,deger2=10**(int(logYU)+1),10**(int(logYU)),10**(int(logYU)-1)
          
          ax1=(int(x1/deger1)-deger2)*deger1  
          ax2=(int(x2/deger1)+deger2)*deger1  
          ay1=(int(y1/deger1)-deger2)*deger1  
          ay2=(int(y2/deger1)+deger2)*deger1

          xListesi,yListesi,x1Listesi,y1Listesi=[],[],[],[]
          
          if deger1>1:
               if ekranYatayUzunluk<=deger:
                    for i in range(ax1,ax2,deger1):
                         xListesi.append(QLineF(x1,i,x2,i))
                    for i in range(ay1,ay2,deger1):
                         yListesi.append(QLineF(i,y1,i,y2))
                    if deger2>=1:
                         for i in range(ax1,ax2,deger2):
                              x1Listesi.append(QLineF(x1,i,x2,i))
                         for i in range(ay1,ay2,deger2):
                              y1Listesi.append(QLineF(i,y1,i,y2))
          return (xListesi,yListesi,x1Listesi,y1Listesi)
     
     def drawBackground(self, painter, rect):
          painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
          painter.fillRect(rect,self.gridtarama)
          painter.setPen(self.gridkalem)
          painter.setOpacity(0.25)
          
          koordinat=rect.getCoords()
          x1,y1,x2,y2=koordinat[0],koordinat[1],koordinat[2],koordinat[3]
          p1=QPointF(x1,y1)
          p2=QPointF(x2,y2)
          listeler=self.arkaplanGrid(p1,p2)
          for i in listeler:painter.drawLines(i)

          #xveyAksları
          painter.setOpacity(0.5)
          painter.setPen(self.xykalem)
          painter.drawLine(0,int(y1),0,int(y2))
          painter.drawLine(int(x1),0,int(x2),0)

     def taramaAlani(self,fareNoktasi):
          taramaAlani=QPainterPath()
          taramaAlani.moveTo(fareNoktasi-QPointF(5,5))
          taramaAlani.lineTo(fareNoktasi+QPointF(5,-5))
          taramaAlani.lineTo(fareNoktasi+QPointF(5,5))
          taramaAlani.lineTo(fareNoktasi+QPointF(-5,5))
          taramaAlani.lineTo(fareNoktasi+QPointF(-5,-5))
          self.setSelectionArea(taramaAlani)
     
     def elemanBilgiListeDuzenle(self):
          if len(self.secimObjesi.secilenElemanlar)==1:
               self.arayuz.ui.elemanBilgiListesi.clear()
               self.arayuz.ui.elemanBilgiListesi.addItem(f"Tip:{self.secimObjesi.secilenElemanlar[0].eBilgi['tip']}")
               for i in self.secimObjesi.secilenElemanlar[0].eBilgi["noktalar"]:
                    self.arayuz.ui.elemanBilgiListesi.addItem(f"Nokta:{i.x(),i.y()}")
               self.arayuz.ui.elemanBilgiListesi.addItem(f"Merkez:{self.secimObjesi.secilenElemanlar[0].eBilgi['merkez']}")
               self.arayuz.ui.elemanBilgiListesi.addItem(f"Yaricap:{self.secimObjesi.secilenElemanlar[0].eBilgi['yaricap']}")
               self.arayuz.ui.elemanBilgiListesi.addItem(f"bbAci:{self.secimObjesi.secilenElemanlar[0].eBilgi['bbAci']}")
               self.arayuz.ui.elemanBilgiListesi.addItem(f"Kare:{self.secimObjesi.secilenElemanlar[0].eBilgi['kare']}")
               self.arayuz.ui.elemanBilgiListesi.addItem(f"Kalem:{self.secimObjesi.secilenElemanlar[0].eBilgi['kalem']}")
               self.arayuz.ui.elemanBilgiListesi.addItem(f"Katman:{self.secimObjesi.secilenElemanlar[0].eBilgi['katman'].eBilgi['katmanAdi']}")
          
          elif len(self.secimObjesi.secilenElemanlar)==0:
               self.arayuz.ui.elemanBilgiListesi.clear()
          elif len(self.secimObjesi.secilenElemanlar)>=2:
               self.arayuz.ui.elemanBilgiListesi.clear()
               self.arayuz.ui.elemanBilgiListesi.addItem("Tek Eleman Secildiğinde Calisir!!")
               
     
     def mousePressEvent(self, event):
          QGraphicsScene.mousePressEvent(self,event)
          if event.button()==Qt.LeftButton:
               if event.modifiers()==Qt.ControlModifier:
                    self.taramaAlani(event.scenePos())
                    self.secimObjesi.listedenElemanCikar(self.selectedItems())
                    
               elif event.modifiers()==Qt.ShiftModifier:
                    self.secikutusu=SecimKutusuCizim(self)
               else:
                    self.taramaAlani(event.scenePos())
                    self.secimObjesi.listeyeElemanEkle(self.selectedItems())
               
               self.fareTiklamaKoordinat.emit(event.scenePos())
          elif event.button()==Qt.MidButton:pass
          elif event.button()==Qt.RightButton:pass


     def mouseMoveEvent(self, event):
          QGraphicsScene.mouseMoveEvent(self,event)
          self.yn=self.ny.yakalamaNoktasi(event)
          self.fareHareketKoordinat.emit(event,self.yn)
     
     def yakalamaNoktasiBilgi(self):
          if self.yn==None:
               self.yn=[]
          return self.yn

     def katmanObjesi(self):
          return self.katman  

     def seciliKatmanElemanEkle(self,eleman):
          seciliKatman=self.katman.seciliKatmanBilgi()
          seciliKatman.elemanEkle(eleman) 