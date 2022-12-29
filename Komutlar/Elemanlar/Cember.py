from PyQt5.QtWidgets import QGraphicsObject,QGraphicsItem
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Ayarlar,Islemler,Katman,OnIzleme
from Komutlar.Elemanlar.AnaEleman import CizimElemani 


class Cember(CizimElemani):
     def __init__(self,tahta,merkez,r,parent=None):
          CizimElemani.__init__(self,tahta,parent)
          self.tahta=tahta
          self.merkez=merkez
          self.r=r

          self.eBilgi={
               "tip":"Cember",
               "noktalar":None,
               "tutamaclar":None,
               "merkez":self.merkez,
               "yaricap":self.r,
               "bbAci":None,
               "kare":None,
               "katman":self.seciliKatman,
               "kalem":None
          }
          self.ucNoktalarGuncelle()

     def boyutlandirmaYeniNoktaBul(self,bnokta,oran):
          merkezuzunluk=Islemler.cizgiUzunlukBul(bnokta,self.eBilgi["merkez"])
          yenimerkezuzunluk=merkezuzunluk*oran
          yeniMerkez=Islemler.uzunluktakiNoktayiBul(bnokta, yenimerkezuzunluk, self.eBilgi["merkez"])
          yeniyaricap=self.eBilgi["yaricap"]*oran
          return yeniMerkez,yeniyaricap
     
     def boyutlandirma(self,boyutlandirmaNoktasi,oran):
          merkezveyaricap=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.bilgiMerkezveYaricapGuncelle(merkezveyaricap[0], merkezveyaricap[1])

     def kopyalama(self,x,y):
          yenicember=Cember(self.tahta, self.eBilgi["merkez"], self.eBilgi["yaricap"])
          yenicember.katmanGuncelle(self.eBilgi["katman"])
          self.tahta.elemanEkle(yenicember)
          yenicember.tasima(x, y)

     def tasima(self,x,y):
          yenimerkez=self.eBilgi["merkez"]+QPointF(x,y)
          self.bilgiMerkezGuncelle(yenimerkez)

     def onIzlemeBasla(self):
          self.onizlemeCember=OnIzleme.OnIzlemeCember(self.tahta,QPointF(),0)
          self.onizlemeCember.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          self.tahta.addItem(self.onizlemeCember)

     def onIzlemeGuncelleBoyutlandirma(self,boyutlandirmaNoktasi,oran):
          self.onizlemeCember.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          merkezveYaricap=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.onizlemeCember.noktalariYenile(merkezveYaricap[0], merkezveYaricap[1])
     
     def onIzlemeGuncelleTasimaveKopyalama(self,x,y):
          self.onizlemeCember.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          yenimerkez=self.eBilgi["merkez"]+QPointF(x,y)
          self.onizlemeCember.noktalariYenile(yenimerkez,self.eBilgi["yaricap"])
     
     def onIzlemeBitir(self):
          self.onizlemeCember.noktalariYenile(QPointF(),0)
          self.tahta.removeItem(self.onizlemeCember)
     
     def bilgiMerkezGuncelle(self,merkez):
          self.eBilgi["merkez"]=merkez
          self.ucNoktalarGuncelle()
     
     def bilgiYaricapGuncelle(self,yaricap):
          self.eBilgi["yaricap"]=yaricap
          self.ucNoktalarGuncelle()
          
     def bilgiMerkezveYaricapGuncelle(self,merkez,yaricap):
          self.eBilgi["merkez"]=merkez
          self.eBilgi["yaricap"]=yaricap
          self.ucNoktalarGuncelle()
     
     def ucNoktalarGuncelle(self):
          p1=self.eBilgi["merkez"]+QPointF(self.eBilgi["yaricap"],0)
          p2=self.eBilgi["merkez"]+QPointF(0,self.eBilgi["yaricap"])
          p3=self.eBilgi["merkez"]+QPointF(-self.eBilgi["yaricap"],0)
          p4=self.eBilgi["merkez"]+QPointF(0,-self.eBilgi["yaricap"])
          self.eBilgi["noktalar"]=[p1,p2,p3,p4]

     
     def tutamaclariSil(self):
          if self.eBilgi["tutamaclar"]!=None:
               self.bilgiMerkezveYaricapGuncelle(self.eBilgi["merkez"],self.eBilgi["yaricap"])
               self.ucNoktalarGuncelle()
               self.tahta.removeItem(self.mrkzT)
               self.tahta.removeItem(self.uc1T)
               self.tahta.removeItem(self.uc2T)
               self.tahta.removeItem(self.uc3T)
               self.tahta.removeItem(self.uc4T)
          self.eBilgi["tutamaclar"]=None

     
     
     def tutamaclariEkle(self):
          if self.eBilgi["tutamaclar"]==None:
               self.mrkzT=self.normalTutamacEkle(self.eBilgi["merkez"],"mrkz")
               self.mrkzT.eBilgi["id"]=4
               self.mrkzT.hareketSinyal.connect(self.tutamacMerkezMesafe)
               
               self.uc1T=self.boyutlandirmaTutamacEkle(self.eBilgi["merkez"]+QPointF(self.eBilgi["yaricap"],0),"uc")
               self.uc1T.eBilgi["id"]=0
               self.uc1T.hareketSinyal.connect(self.tutamacMerkezMesafe)
               
               self.uc2T=self.boyutlandirmaTutamacEkle(self.eBilgi["merkez"]+QPointF(0,self.eBilgi["yaricap"]),"uc")
               self.uc2T.eBilgi["id"]=1
               self.uc2T.hareketSinyal.connect(self.tutamacMerkezMesafe)
               
               self.uc3T=self.boyutlandirmaTutamacEkle(self.eBilgi["merkez"]+QPointF(-self.eBilgi["yaricap"],0),"uc")
               self.uc3T.eBilgi["id"]=2
               self.uc3T.hareketSinyal.connect(self.tutamacMerkezMesafe)
               
               self.uc4T=self.boyutlandirmaTutamacEkle(self.eBilgi["merkez"]+QPointF(0,-self.eBilgi["yaricap"]),"uc")
               self.uc4T.eBilgi["id"]=3
               self.uc4T.hareketSinyal.connect(self.tutamacMerkezMesafe)

          self.eBilgi["tutamaclar"]=[self.mrkzT.eBilgi,self.uc1T.eBilgi,self.uc2T.eBilgi,self.uc3T.eBilgi,self.uc4T.eBilgi]
          self.ucNoktalarGuncelle()

     def tutamacOrtaNGuncelle(self):
          self.uc1T.eBilgi["noktalar"]=self.eBilgi["merkez"]+(QPointF(self.eBilgi["yaricap"],0))
          self.uc1T.ortaN=self.eBilgi["merkez"]+(QPointF(self.eBilgi["yaricap"],0))
          self.uc1T.setPos(0,0)
          self.uc2T.eBilgi["noktalar"]=self.eBilgi["merkez"]+(QPointF(0,self.eBilgi["yaricap"]))
          self.uc2T.ortaN=self.eBilgi["merkez"]+(QPointF(0,self.eBilgi["yaricap"]))
          self.uc2T.setPos(0,0)
          self.uc3T.eBilgi["noktalar"]=self.eBilgi["merkez"]+(QPointF(-self.eBilgi["yaricap"],0))
          self.uc3T.ortaN=self.eBilgi["merkez"]+(QPointF(-self.eBilgi["yaricap"],0))
          self.uc3T.setPos(0,0)
          self.uc4T.eBilgi["noktalar"]=self.eBilgi["merkez"]+(QPointF(0,-self.eBilgi["yaricap"]))
          self.uc4T.ortaN=self.eBilgi["merkez"]+(QPointF(0,-self.eBilgi["yaricap"]))
          self.uc4T.setPos(0,0)
          self.ucNoktalarGuncelle()
     
     def tutamacMerkezMesafe(self,bilgi):
          if bilgi[0]==0:
               self.eBilgi["yaricap"]=Islemler.cizgiUzunlukBul(self.eBilgi["merkez"],QPointF(self.uc1T.eBilgi["noktalar"].x(),self.eBilgi["merkez"].y()))
               self.tutamacOrtaNGuncelle()
          elif bilgi[0]==1:
               self.eBilgi["yaricap"]=Islemler.cizgiUzunlukBul(self.eBilgi["merkez"],QPointF(self.eBilgi["merkez"].x(),self.uc2T.eBilgi["noktalar"].y()))
               self.tutamacOrtaNGuncelle()
          elif bilgi[0]==2:
               self.eBilgi["yaricap"]=Islemler.cizgiUzunlukBul(self.eBilgi["merkez"],QPointF(self.uc3T.eBilgi["noktalar"].x(),self.eBilgi["merkez"].y()))
               self.tutamacOrtaNGuncelle()
          elif bilgi[0]==3:
               self.eBilgi["yaricap"]=Islemler.cizgiUzunlukBul(self.eBilgi["merkez"],QPointF(self.eBilgi["merkez"].x(),self.uc4T.eBilgi["noktalar"].y()))
               self.tutamacOrtaNGuncelle()
          elif bilgi[0]==4:
               self.eBilgi["merkez"]=self.mrkzT.eBilgi["noktalar"]
               self.tutamacOrtaNGuncelle()

     def paint(self, painter,option, widget):
          painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
          self.kalemAyari(painter)
          painter.drawEllipse(self.kare)
          # painter.drawPath(self.shape())
          
     def boundingRect(self):
          return self.shape().boundingRect()


     def shape(self):
          painterStrock=QPainterPathStroker()
          painterStrock.setWidth(Ayarlar.cizgiBoundMesafe)
          p=QPainterPath()
          
          if self.eBilgi["tutamaclar"]!=None:
               baslagicnn=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(self.eBilgi["yaricap"],0)
               p.moveTo(baslagicnn.x(),baslagicnn.y())
               baslagicn=self.eBilgi["tutamaclar"][0]["noktalar"]-QPointF(self.eBilgi["yaricap"],self.eBilgi["yaricap"])
               bitisn=self.eBilgi["tutamaclar"][0]["noktalar"]+QPointF(self.eBilgi["yaricap"],self.eBilgi["yaricap"])
               self.kare=QRectF(baslagicn,bitisn)
               p.arcTo(self.kare,0,360)
          else:
               baslagicnn=self.eBilgi["merkez"]+QPointF(self.eBilgi["yaricap"],0)
               p.moveTo(baslagicnn.x(),baslagicnn.y())
               baslagicn=self.eBilgi["merkez"]-QPointF(self.eBilgi["yaricap"],self.eBilgi["yaricap"])
               bitisn=self.eBilgi["merkez"]+QPointF(self.eBilgi["yaricap"],self.eBilgi["yaricap"])
               self.kare=QRectF(baslagicn,bitisn)
               p.arcTo(self.kare,0,360)
          
          path1=painterStrock.createStroke(p)
          
          return path1