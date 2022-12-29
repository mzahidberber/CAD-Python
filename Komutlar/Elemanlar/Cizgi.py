from PyQt5.QtWidgets import QGraphicsItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Ayarlar,Katman,OnIzleme,Islemler
from Komutlar.Elemanlar.AnaEleman import CizimElemani 

class Cizgi(CizimElemani):
     
     def __init__(self,tahta,p1,p2,parent=None):
          CizimElemani.__init__(self,tahta,parent)
          self.tahta=tahta
          self.p1=p1
          self.p2=p2
          
          self.eBilgi={
               "tip":"Cizgi",
               "noktalar":[self.p1,self.p2],
               "tutamaclar":None,
               "merkez":None,
               "yaricap":None,
               "bbAci":None,
               "kare":None,
               "katman":self.seciliKatman,
               "kalem":None
          }

     def boyutlandirmaYeniNoktaBul(self,bnokta,oran):
          uzunluk2=Islemler.cizgiUzunlukBul(bnokta,self.eBilgi["noktalar"][0])
          uzunluk3=Islemler.cizgiUzunlukBul(bnokta,self.eBilgi["noktalar"][1])
          yeniuzunluk1=uzunluk2*oran
          yeniuzunluk2=uzunluk3*oran
          yeniNokta1=Islemler.uzunluktakiNoktayiBul(bnokta, yeniuzunluk1, self.eBilgi["noktalar"][0])
          yeniNokta2=Islemler.uzunluktakiNoktayiBul(bnokta, yeniuzunluk2, self.eBilgi["noktalar"][1])
          return yeniNokta1,yeniNokta2
     
     def boyutlandirma(self,boyutlandirmaNoktasi,oran):
          noktalar=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.bilgiNoktalariGuncelle(noktalar[0],noktalar[1])

     def dondurmeYeniNoktaBul(self,dnokta,derece,p):
          noktanerde=Islemler.noktaHangiBolgedeBul(dnokta,p)
          uzunluk=Islemler.cizgiUzunlukBul(dnokta, p)
          egim=Islemler.dogruEgimBulma(dnokta, p)
          aci=Islemler.dogruAciBulma(egim)
          yeniaci=float
          if aci>0:
               if noktanerde==1:
                    yeniaci=aci+derece
               elif noktanerde==3:
                    yeniaci=aci+180+derece
               elif noktanerde==5:
                    return dnokta
          else:
               if noktanerde==2:
                    yeniaci=-aci+90+derece
               elif noktanerde==4:
                    yeniaci=-aci+270+derece
               elif noktanerde==5:
                    return dnokta
          ryeniaci=Islemler.dereceyiRadyanaCevirme(yeniaci)
          yeniegim=Islemler.acidanEgimBulma(ryeniaci)
          yeniNokta=Islemler.uzunlukNoktalariniBul(dnokta, uzunluk, yeniegim)
          #print(f"bölge:{noktanerde},uzunluk:{uzunluk},egim:{egim}\nderece:{derece},aci:{aci},yeniaci:{yeniaci},ryeniaci:{ryeniaci},yeniegim:{yeniegim}\nyeniNokta:{yeniNokta}")
          #print("------------------------------------")
          if 0<=yeniaci<=90 or 270<=yeniaci<=360:
               return yeniNokta[0]
          elif 90<=yeniaci<=180 or 180<=yeniaci<=270:
               return yeniNokta[1]
          else:
               return dnokta

     def dondurme(self,dnokta,derece):
          yenip1=self.dondurmeYeniNoktaBul(dnokta, derece, self.eBilgi["noktalar"][0])
          yenip2=self.dondurmeYeniNoktaBul(dnokta, derece, self.eBilgi["noktalar"][1])
          self.bilgiNoktalariGuncelle(yenip1,yenip2)
     
     def kopyalama(self,x,y):
          yeniCizgi=Cizgi(self.tahta,self.eBilgi["noktalar"][0] ,self.eBilgi["noktalar"][1])
          yeniCizgi.katmanGuncelle(self.eBilgi["katman"])
          self.tahta.elemanEkle(yeniCizgi)
          yeniCizgi.tasima(x, y)

     def tasima(self,x,y):
          yenip1=self.eBilgi["noktalar"][0]+QPointF(x,y)
          yenip2=self.eBilgi["noktalar"][1]+QPointF(x,y)
          self.bilgiNoktalariGuncelle(yenip1,yenip2)

     def onIzlemeBasla(self):
          self.onizleme=OnIzleme.OnIzlemeCizgi(self.tahta,QPointF(),QPointF())
          self.onizleme.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          self.tahta.addItem(self.onizleme)

     def onIzlemeGuncelleBoyutlandirma(self,boyutlandirmaNoktasi,oran):
          self.onizleme.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          noktalar=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.onizleme.noktalariYenile(noktalar[0],noktalar[1])

     def onIzlemeGuncelleDondurme(self,dnokta,derece):
          yenip1=self.dondurmeYeniNoktaBul(dnokta, derece, self.eBilgi["noktalar"][0])
          yenip2=self.dondurmeYeniNoktaBul(dnokta, derece, self.eBilgi["noktalar"][1])
          self.onizleme.noktalariYenile(yenip1,yenip2) 
     
     def onIzlemeGuncelleTasimaveKopyalama(self,x,y):
          self.onizleme.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          yenip1=self.eBilgi["noktalar"][0]+QPointF(x,y)
          yenip2=self.eBilgi["noktalar"][1]+QPointF(x,y)
          self.onizleme.noktalariYenile(yenip1,yenip2)
     
     def onIzlemeBitir(self):
          self.onizleme.noktalariYenile(QPointF(),QPointF())
          self.tahta.removeItem(self.onizleme)
     
     def bilgiNoktalariGuncelle(self,p1,p2):
          self.eBilgi["noktalar"]=[p1,p2]

     def tutamaclariEkle(self):
          if self.eBilgi["tutamaclar"]==None:
               self.uc1T=self.normalTutamacEkle(self.eBilgi["noktalar"][0],"uc")
               self.uc1T.eBilgi["id"]=0
               self.uc1T.hareketSinyal.connect(self.tutamacSinyalTakip)
               self.uc2T=self.normalTutamacEkle(self.eBilgi["noktalar"][1],"uc")
               self.uc2T.eBilgi["id"]=1
               self.uc2T.hareketSinyal.connect(self.tutamacSinyalTakip)
          self.eBilgi["tutamaclar"]=[self.uc1T.eBilgi,self.uc2T.eBilgi]

     def tutamacSinyalTakip(self,bilgiler):
          self.bilgiNoktalariGuncelle(self.uc1T.eBilgi["noktalar"],self.uc2T.eBilgi["noktalar"])
     
     def tutamaclariSil(self):
          if self.eBilgi["tutamaclar"]!=None:
               self.bilgiNoktalariGuncelle(self.eBilgi["tutamaclar"][0]["noktalar"],self.eBilgi["tutamaclar"][1]["noktalar"])
               self.tahta.removeItem(self.uc1T)
               self.tahta.removeItem(self.uc2T)
          self.eBilgi["tutamaclar"]=None
          
     def paint(self, painter,option, widget):
          painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)

          self.kalemAyari(painter)

          if self.eBilgi["tutamaclar"]!=None:
               painter.drawLine(self.eBilgi["tutamaclar"][0]["noktalar"],self.eBilgi["tutamaclar"][1]["noktalar"])
          else:
               painter.drawLine(self.eBilgi["noktalar"][0],self.eBilgi["noktalar"][1])
          # painter.drawPath(self.shape())
          
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          painterStrock=QPainterPathStroker()
          painterStrock.setWidth(Ayarlar.cizgiBoundMesafe)
          p=QPainterPath()

          if self.eBilgi["tutamaclar"]!=None:
               p.moveTo(self.eBilgi["tutamaclar"][0]["noktalar"].x(),self.eBilgi["tutamaclar"][0]["noktalar"].y())
               p.lineTo(self.eBilgi["tutamaclar"][1]["noktalar"].x(),self.eBilgi["tutamaclar"][1]["noktalar"].y())
          else:
               p.moveTo(self.eBilgi["noktalar"][0].x(),self.eBilgi["noktalar"][0].y())
               p.lineTo(self.eBilgi["noktalar"][1].x(),self.eBilgi["noktalar"][1].y())
          
          path1=painterStrock.createStroke(p)
          
          return path1     