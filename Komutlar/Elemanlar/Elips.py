from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Ayarlar,OnIzleme,Islemler
from Komutlar.Elemanlar.AnaEleman import CizimElemani 

class Elips(CizimElemani):
     
     def __init__(self,tahta,merkez,r1,r2,parent=None):
          CizimElemani.__init__(self,tahta,parent)
          self.tahta=tahta
          self.merkez=merkez
          self.r1=r1
          self.r2=r2

          self.eBilgi={
               "tip":"Elips",
               "noktalar":None,
               "merkez":self.merkez,
               "yaricap":[self.r1,self.r2],
               "r1":self.r1,
               "r2":self.r2,
               "bbAci":None,
               "kare":None,
               "tutamaclar":None,
               "katman":self.seciliKatman,
               "kalem":None
          }
          self.ucNoktalarGuncelle()

     def boyutlandirmaYeniNoktaBul(self,bnokta,oran):
          merkezuzunluk=Islemler.cizgiUzunlukBul(bnokta,self.eBilgi["merkez"])
          yenimerkezuzunluk=merkezuzunluk*oran
          yeniMerkez=Islemler.uzunluktakiNoktayiBul(bnokta, yenimerkezuzunluk, self.eBilgi["merkez"])
          yenir1=self.eBilgi["r1"]*oran
          yenir2=self.eBilgi["r2"]*oran
          return yeniMerkez,yenir1,yenir2
     
     def boyutlandirma(self,boyutlandirmaNoktasi,oran):
          merkezveyaricap=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.bilgiNoktalariGuncelle(merkezveyaricap[0], merkezveyaricap[1],merkezveyaricap[2])

     def kopyalama(self,x,y):
          yenielips=Elips(self.tahta, self.eBilgi["merkez"], self.eBilgi["r1"],self.eBilgi["r2"])
          yenielips.katmanGuncelle(self.eBilgi["katman"])
          self.tahta.elemanEkle(yenielips)
          yenielips.tasima(x, y)

     def tasima(self,x,y):
          yenimerkez=self.eBilgi["merkez"]+QPointF(x,y)
          self.bilgiMerkezGuncelle(yenimerkez)

     def onIzlemeBasla(self):
          self.onIzlemeElips=OnIzleme.OnIzlemeElips(self.tahta,QPointF(),0,0)
          self.onIzlemeElips.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          self.tahta.addItem(self.onIzlemeElips)

     def onIzlemeGuncelleBoyutlandirma(self,boyutlandirmaNoktasi,oran):
          self.onIzlemeElips.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          merkezveYaricap=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.onIzlemeElips.noktalariYenile(merkezveYaricap[0], merkezveYaricap[1],merkezveYaricap[2])
     
     def onIzlemeGuncelleTasimaveKopyalama(self,x,y):
          self.onIzlemeElips.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          yenimerkez=self.eBilgi["merkez"]+QPointF(x,y)
          self.onIzlemeElips.noktalariYenile(yenimerkez,self.eBilgi["r1"],self.eBilgi["r2"])
     
     def onIzlemeBitir(self):
          self.onIzlemeElips.noktalariYenile(QPointF(),0,0)
          self.tahta.removeItem(self.onIzlemeElips)

     def tutamacSinyalTakip(self,bilgiler):
          self.bilgiNoktalariGuncelle(self.mrkzT.eBilgi["noktalar"],self.eBilgi["r1"],self.eBilgi["r2"])
     
     def ucNoktalarGuncelle(self):
          p1=self.eBilgi["merkez"]+QPointF(self.eBilgi["r1"],0)
          p2=self.eBilgi["merkez"]+QPointF(0,self.eBilgi["r2"])
          p3=self.eBilgi["merkez"]+QPointF(-self.eBilgi["r1"],0)
          p4=self.eBilgi["merkez"]+QPointF(0,-self.eBilgi["r2"])
          self.eBilgi["noktalar"]=[p1,p2,p3,p4]
     
     def bilgiNoktalariGuncelle(self,merkez,r1,r2):
          self.eBilgi["merkez"]=merkez
          self.eBilgi["r1"]=r1
          self.eBilgi["r2"]=r2

     def bilgiMerkezGuncelle(self,merkez):
          self.eBilgi["merkez"]=merkez
          self.ucNoktalarGuncelle()

     def tutamaclariEkle(self):
          if self.eBilgi["tutamaclar"]==None:
               self.mrkzT=self.normalTutamacEkle(self.eBilgi["merkez"],"mrkz")
               self.mrkzT.eBilgi["id"]=0
               self.mrkzT.hareketSinyal.connect(self.tutamacSinyalTakip)
          self.eBilgi["tutamaclar"]=[self.mrkzT.eBilgi]
          self.ucNoktalarGuncelle()
     
     def tutamaclariSil(self):
          if self.eBilgi["tutamaclar"]!=None:
               self.bilgiNoktalariGuncelle(self.eBilgi["tutamaclar"][0]["noktalar"],self.eBilgi["r1"],self.eBilgi["r2"])
               self.tahta.removeItem(self.mrkzT)
          self.eBilgi["tutamaclar"]=None
          self.ucNoktalarGuncelle()


     def paint(self, painter,option, widget):
          painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
          self.kalemAyari(painter)

          if self.eBilgi["tutamaclar"]!=None:
               painter.drawEllipse(self.eBilgi["tutamaclar"][0]["noktalar"],self.eBilgi["r1"],self.eBilgi["r2"])
          else:
               painter.drawEllipse(self.eBilgi["merkez"],self.eBilgi["r1"],self.eBilgi["r2"])
          #painter.drawPath(self.shape())
          
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          painterStrock=QPainterPathStroker()
          painterStrock.setWidth(Ayarlar.cizgiBoundMesafe)
          p=QPainterPath()
          
          if self.eBilgi["tutamaclar"]!=None:
               baslagicnn=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(self.eBilgi["r1"],0)
               n1=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(self.eBilgi["r1"],self.eBilgi["r2"])
               n2=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(0,self.eBilgi["r2"])
               n3=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(-self.eBilgi["r1"],self.eBilgi["r2"])
               n4=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(-self.eBilgi["r1"],0)
               n5=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(-self.eBilgi["r1"],-self.eBilgi["r2"])
               n6=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(0,-self.eBilgi["r2"])
               n7=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(self.eBilgi["r1"],-self.eBilgi["r2"])
          else:
               baslagicnn=self.eBilgi["merkez"]+QPointF(self.eBilgi["r1"],0)
               n1=self.eBilgi["merkez"]+QPointF(self.eBilgi["r1"],self.eBilgi["r2"])
               n2=self.eBilgi["merkez"]+QPointF(0,self.eBilgi["r2"])
               n3=self.eBilgi["merkez"]+QPointF(-self.eBilgi["r1"],self.eBilgi["r2"])
               n4=self.eBilgi["merkez"]+QPointF(-self.eBilgi["r1"],0)
               n5=self.eBilgi["merkez"]+QPointF(-self.eBilgi["r1"],-self.eBilgi["r2"])
               n6=self.eBilgi["merkez"]+QPointF(0,-self.eBilgi["r2"])
               n7=self.eBilgi["merkez"]+QPointF(self.eBilgi["r1"],-self.eBilgi["r2"])
          
          p.moveTo(baslagicnn)
          p.quadTo(n1.x(),n1.y(),n2.x(),n2.y())
          p.quadTo(n3.x(),n3.y(),n4.x(),n4.y())
          p.quadTo(n5.x(),n5.y(),n6.x(),n6.y())
          p.quadTo(n7.x(),n7.y(),baslagicnn.x(),baslagicnn.y())
          path1=painterStrock.createStroke(p)
          
          return path1