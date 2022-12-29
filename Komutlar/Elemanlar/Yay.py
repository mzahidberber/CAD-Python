from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Ayarlar,Islemler
from Komutlar.Elemanlar.AnaEleman import CizimElemani 


class Yay(CizimElemani):
     def __init__(self,p1,kare,baslagicAci,bitisAci,parent=None):
          CizimElemani.__init__(self,parent)
          self.p1=p1
          self.kare=kare
          self.baslagicAci=baslagicAci
          self.bitisAci=bitisAci
          

          self.eBilgi={
               "tip":"Yay",
               "tutamaclar":None,
               "katman":None,
               "kalem":Ayarlar.cizgiKalem
          }
          self.kalem=self.eBilgi["kalem"]


     def paint(self, painter,option, widget):
          painter.setPen(self.kalem)
          
          painter.drawArc(self.kare,-self.baslagicAci*16,-self.bitisAci*16)
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

class UcNoktaYay(CizimElemani):
     def __init__(self,tahta,p1,p2,p3,parent=None):
          CizimElemani.__init__(self,tahta,parent)
          self.tahta=tahta
          self.p1=p1
          self.p2=p2
          self.p3=p3

          self.eBilgi={
               "tip":"Yay",
               "noktalar":[self.p1,self.p2,self.p3],
               "merkez":None,
               "yaricap":None,
               "bbAci":None,
               "kare":None,
               "tutamaclar":None,
               "katman":self.seciliKatman,
               "kalem":None
          }
          if self.eBilgi["merkez"]==None:
               self.eBilgi["merkez"]=QPointF()

     def boyutlandirmaYeniNoktaBul(self,bnokta,oran):
          yeniListe=[]
          for i in self.eBilgi["noktalar"]:
               uzunluk=Islemler.cizgiUzunlukBul(bnokta,i)
               yeniuzunluk=uzunluk*oran
               yeniNokta=Islemler.uzunluktakiNoktayiBul(bnokta, yeniuzunluk, i)
               yeniListe.append(yeniNokta)
          return yeniListe
     
     def boyutlandirma(self,boyutlandirmaNoktasi,oran):
          noktalar=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.bilgiNoktalariGuncelle(noktalar[0], noktalar[1],noktalar[2])

     def kopyalama(self,x,y):
          yeniYay=UcNoktaYay(self.tahta, self.eBilgi["noktalar"][0], self.eBilgi["noktalar"][1], self.eBilgi["noktalar"][2])
          yeniYay.katmanGuncelle(self.eBilgi["katman"])
          self.tahta.elemanEkle(yeniYay)
          yeniYay.tasima(x, y)

     def tasima(self,x,y):
          yenip1=self.eBilgi["noktalar"][0]+QPointF(x,y)
          yenip2=self.eBilgi["noktalar"][1]+QPointF(x,y)
          yenip3=self.eBilgi["noktalar"][2]+QPointF(x,y)
          yenimerkez=self.eBilgi["merkez"]+QPointF(x,y)
          self.bilgiNoktalariGuncelle(yenip1,yenip2,yenip3)

     def onIzlemeBasla(self):pass
     def onIzlemeGuncelleBoyutlandirma(self,boyutlandirmaNoktasi,oran):pass
     def onIzlemeGuncelleTasimaveKopyalama(self,x,y):pass
     def onIzlemeBitir(self):pass

     def tutamacSinyalTakip(self,bilgiler):
          self.bilgiNoktalariMGuncelle(self.eBilgi["tutamaclar"][3]["noktalar"],self.eBilgi["tutamaclar"][0]["noktalar"],self.eBilgi["tutamaclar"][1]["noktalar"],self.eBilgi["tutamaclar"][2]["noktalar"])

     def bilgiNoktalariMGuncelle(self,merkez,p1,p2,p3):
          self.eBilgi["noktalar"]=[p1,p2,p3]
          self.eBilgi["merkez"]=merkez

     def bilgiNoktalariGuncelle(self,p1,p2,p3):
          self.eBilgi["noktalar"]=[p1,p2,p3]
     
     def tutamaclariSil(self):
          if self.eBilgi["tutamaclar"]!=None:
               self.bilgiNoktalariMGuncelle(self.eBilgi["tutamaclar"][3]["noktalar"],self.eBilgi["tutamaclar"][0]["noktalar"],self.eBilgi["tutamaclar"][1]["noktalar"],self.eBilgi["tutamaclar"][2]["noktalar"])
               self.tahta.removeItem(self.t1)
               self.tahta.removeItem(self.t2)
               self.tahta.removeItem(self.t3)
               self.tahta.removeItem(self.t4)
          self.eBilgi["tutamaclar"]=None
     
     def tutamaclariEkle(self):
          if self.eBilgi["tutamaclar"]==None:
               self.t1=self.normalTutamacEkle(self.eBilgi["noktalar"][0],"uc")
               self.t1.eBilgi["id"]=0
               self.t1.hareketSinyal.connect(self.tutamacSinyalTakip)
               self.t2=self.normalTutamacEkle(self.eBilgi["noktalar"][1],"uc")
               self.t2.eBilgi["id"]=1
               self.t2.hareketSinyal.connect(self.tutamacSinyalTakip)
               self.t3=self.normalTutamacEkle(self.eBilgi["noktalar"][2],"uc")
               self.t3.eBilgi["id"]=2
               self.t3.hareketSinyal.connect(self.tutamacSinyalTakip)
               self.t4=self.boyutlandirmaTutamacEkle(self.eBilgi["merkez"],"mrkz")
               self.t4.eBilgi["id"]=4
               self.t4.hareketSinyal.connect(self.tutamacSinyalTakip)
          
          self.eBilgi["tutamaclar"]=[self.t1.eBilgi,self.t2.eBilgi,self.t3.eBilgi,self.t4.eBilgi]
     
     def paint(self, painter,option, widget):
          painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
          self.kalemAyari(painter)
          
          painter.drawArc(self.eBilgi["kare"],int(-self.eBilgi["bbAci"][0]*16),-int(self.eBilgi["bbAci"][1]*16))
          #painter.drawPath(self.shape())
          
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          painterStrock=QPainterPathStroker()
          painterStrock.setWidth(Ayarlar.cizgiBoundMesafe)
          p=QPainterPath()

          if self.eBilgi["tutamaclar"]!=None:
               self.merkezveYaricapBul(self.t1.eBilgi["noktalar"],self.t2.eBilgi["noktalar"],self.t3.eBilgi["noktalar"])           
               self.baslagicBitisAcisiBul(self.eBilgi["merkez"],self.t1.eBilgi["noktalar"],self.t2.eBilgi["noktalar"],self.t3.eBilgi["noktalar"])
               karenokta=self.eBilgi["merkez"]-QPointF(self.eBilgi["yaricap"],self.eBilgi["yaricap"])
               self.eBilgi["kare"]=QRectF(karenokta.x(),karenokta.y(),2*self.eBilgi["yaricap"],2*self.eBilgi["yaricap"])

               p.moveTo(self.t1.eBilgi["noktalar"].x(),self.t1.eBilgi["noktalar"].y())
          else:
               self.merkezveYaricapBul(self.eBilgi["noktalar"][0],self.eBilgi["noktalar"][1],self.eBilgi["noktalar"][2])           
               self.baslagicBitisAcisiBul(self.eBilgi["merkez"],self.eBilgi["noktalar"][0],self.eBilgi["noktalar"][1],self.eBilgi["noktalar"][2])
               karenokta=self.eBilgi["merkez"]-QPointF(self.eBilgi["yaricap"],self.eBilgi["yaricap"])
               self.eBilgi["kare"]=QRectF(karenokta.x(),karenokta.y(),2*self.eBilgi["yaricap"],2*self.eBilgi["yaricap"])

               p.moveTo(self.eBilgi["noktalar"][0].x(),self.eBilgi["noktalar"][0].y())


          
          p.arcTo(self.eBilgi["kare"],-self.eBilgi["bbAci"][0],-self.eBilgi["bbAci"][1])
          path1=painterStrock.createStroke(p)
          
          return path1 

     
     def baslagicBitisAcisiBul(self,merkez,p1,p2,p3):
          baslangicAci=Islemler.dogruAciBul(merkez,p1)

          if p1.x()>merkez.x():
               if p1.y()>merkez.y():
                    baslangicAci=baslangicAci
               else:
                    baslangicAci=baslangicAci
          else:
               if p1.y()>merkez.y():
                    baslangicAci=baslangicAci+180
               else:
                    baslangicAci=baslangicAci-180
          
          p3Aci=Islemler.dogruAciBul(merkez,p3)
          if p3.x()>merkez.x():
               if p3.y()>merkez.y():
                    p3Aci=p3Aci
               else:
                    p3Aci=p3Aci+360
          else:
               if p3.y()>merkez.y():
                    p3Aci=p3Aci+180
               else:
                    p3Aci=p3Aci+180

          
          konum=Islemler.NoktaDogrununNeresindeBul(p1,p3,p2)

          if konum=="sag":
               bitisAci=p3Aci-baslangicAci
          elif konum=="sol":
               bitisAci=-(360-(p3Aci-baslangicAci))
          else:
               bitisAci=p3Aci-baslangicAci

          self.eBilgi["bbAci"]=[baslangicAci,bitisAci]

     def merkezveYaricapBul(self,p1,p2,p3):
          merkezyaricap=Islemler.merkezveYaricapBul(p1,p2,p3)
          self.eBilgi["merkez"]=QPointF(merkezyaricap[0][0],merkezyaricap[0][1])
          self.eBilgi["yaricap"]=merkezyaricap[1]
          
          if self.eBilgi["tutamaclar"]!=None:
               self.t4.eBilgi["noktalar"]=self.eBilgi["merkez"]
               self.t4.ortaN=self.eBilgi["merkez"]
               self.t4.setPos(0,0)