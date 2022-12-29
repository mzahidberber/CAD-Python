from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import Ayarlar,OnIzleme,Islemler
from Komutlar.Elemanlar.AnaEleman import CizimElemani 


class SurekliCizgi(CizimElemani):
     def __init__(self,tahta,noktaListesi,parent=None):
          CizimElemani.__init__(self,tahta,parent)
          self.tahta=tahta
          self.noktaListesi=noktaListesi

          self.eBilgi={
               "tip":"SCizgi",
               "noktalar":self.noktaListesi,
               "tutamaclar":None,
               "merkez":None,
               "yaricap":None,
               "bbAci":None,
               "kare":None,
               "katman":self.seciliKatman,
               "kalem":None
          }

     def boyutlandirmaYeniNoktaBul(self,bnokta,oran):
          yeniListe=[]
          for i in self.eBilgi["noktalar"]:
               uzunluk=Islemler.cizgiUzunlukBul(bnokta,i)
               yeniuzunluk=uzunluk*oran
               yeniNokta=Islemler.uzunluktakiNoktayiBul(bnokta, yeniuzunluk, i)
               yeniListe.append(yeniNokta)
          return yeniListe
     
     def boyutlandirma(self,boyutlandirmaNoktasi,oran):
          yeniListe=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.bilgiNoktalariGuncelle(yeniListe)
     
     def kopyalama(self,x,y):
          yeniScizgi=SurekliCizgi(self.tahta, self.eBilgi["noktalar"])
          yeniScizgi.katmanGuncelle(self.eBilgi["katman"])
          self.tahta.elemanEkle(yeniScizgi)
          yeniScizgi.tasima(x, y)

     def tasima(self,x,y):
          yeniListe=[i+QPointF(x,y) for i in self.eBilgi["noktalar"]]
          self.bilgiNoktalariGuncelle(yeniListe)

     def onIzlemeBasla(self):
          self.onIzlemesCizgi=OnIzleme.OnIzlemeSCizgi(self.tahta,[])
          self.onIzlemesCizgi.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          self.tahta.addItem(self.onIzlemesCizgi)

     def onIzlemeGuncelleBoyutlandirma(self,boyutlandirmaNoktasi,oran):
          self.onIzlemesCizgi.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          yeniListe=self.boyutlandirmaYeniNoktaBul(boyutlandirmaNoktasi,oran)
          self.onIzlemesCizgi.noktalariYenile(yeniListe)
     
     def onIzlemeGuncelleTasimaveKopyalama(self,x,y):
          self.onIzlemesCizgi.kalemDegistir(self.eBilgi["katman"].eBilgi["kalem"])
          yeniListe=[i+QPointF(x,y) for i in self.eBilgi["noktalar"]]
          self.onIzlemesCizgi.noktalariYenile(yeniListe)
     
     def onIzlemeBitir(self):
          self.onIzlemesCizgi.noktalariYenile([])
          self.tahta.removeItem(self.onIzlemesCizgi)

     def tutamacSinyalTakip(self,bilgiler):
          liste=[]
          for i in self.eBilgi["tutamaclar"]:
               liste.append(i.eBilgi["noktalar"])
          self.bilgiNoktalariGuncelle(liste)

     def bilgiNoktalariGuncelle(self,noktalistesi):
          self.eBilgi["noktalar"]=noktalistesi

     def tutamaclariEkle(self):
          if self.eBilgi["tutamaclar"]==None:
               self.tListesi=[]
               i=0
               while i<len(self.eBilgi["noktalar"]):
                    self.tutamac=self.normalTutamacEkle(self.eBilgi["noktalar"][i],"uc")
                    self.tutamac.eBilgi["id"]=i
                    self.tutamac.hareketSinyal.connect(self.tutamacSinyalTakip)
                    self.tListesi.append(self.tutamac)
                    i+=1
          self.eBilgi["tutamaclar"]=self.tListesi
     
     def tutamaclariSil(self):
          if self.eBilgi["tutamaclar"]!=None:
               yeniNoktaListesi=[]
               for i in self.eBilgi["tutamaclar"]:
                    yeniNoktaListesi.append(i.eBilgi["noktalar"]) 
                    self.tahta.removeItem(i)
               
               self.bilgiNoktalariGuncelle(yeniNoktaListesi)
          self.eBilgi["tutamaclar"]=None

     def paint(self, painter,option, widget):
          painter.setRenderHints(QPainter.Antialiasing | QPainter.HighQualityAntialiasing)
          self.kalemAyari(painter)
          cizgiListesi=[]
          
          if self.eBilgi["tutamaclar"]!=None:
               i=0
               while i<len(self.eBilgi["tutamaclar"])-1:
                    cizgiListesi.append((self.eBilgi["tutamaclar"][i].eBilgi["noktalar"],self.eBilgi["tutamaclar"][i+1].eBilgi["noktalar"]))
                    i+=1
               
          else:
               i=0
               while i<len(self.eBilgi["noktalar"])-1:
                    cizgiListesi.append((self.eBilgi["noktalar"][i],self.eBilgi["noktalar"][i+1]))
                    i+=1
               
          
          for i in cizgiListesi:
               line=QLineF(i[0],i[1])
               painter.drawLine(line)

          #painter.drawPath(self.shape())
          
     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          painterStrock=QPainterPathStroker()
          
          painterStrock.setWidth(Ayarlar.cizgiBoundMesafe)
          p=QPainterPath()
          
          if self.eBilgi["tutamaclar"]!=None:
               p.moveTo(self.eBilgi["tutamaclar"][0].eBilgi["noktalar"])
               for i in self.eBilgi["tutamaclar"]:
                    if i==self.eBilgi["tutamaclar"][0]:
                         continue
                    p.lineTo(i.eBilgi["noktalar"])
          else:
               p.moveTo(self.eBilgi["noktalar"][0])
               for i in self.eBilgi["noktalar"]:
                    if i==self.eBilgi["noktalar"][0]:
                         continue
                    p.lineTo(i)
          
          p1=painterStrock.createStroke(p)
          
          return p1

class Dikdortgen(SurekliCizgi):
     def __init__(self,tahta,noktaListesi,parent=None):
          SurekliCizgi.__init__(self,tahta,noktaListesi,parent)
          self.tahta=tahta
          self.noktaListesi=noktaListesi

          self.eBilgi={
               "tip":"Dikdortgen",
               "noktalar":self.noktaListesi,
               "tutamaclar":None,
               "merkez":None,
               "yaricap":None,
               "bbAci":None,
               "kare":None,
               "katman":self.seciliKatman,
               "kalem":None
          }

     def shape(self):
          painterStrock=QPainterPathStroker()
          
          painterStrock.setWidth(Ayarlar.cizgiBoundMesafe)
          p=QPainterPath()
          
          if self.eBilgi["tutamaclar"]!=None:
               p.moveTo(self.eBilgi["tutamaclar"][0].eBilgi["noktalar"])
               for i in self.eBilgi["tutamaclar"]:
                    if i==self.eBilgi["tutamaclar"][0]:
                         continue
                    p.lineTo(i.eBilgi["noktalar"])
               p.lineTo(self.eBilgi["tutamaclar"][-1].eBilgi["noktalar"])
          else:
               p.moveTo(self.eBilgi["noktalar"][0])
               for i in self.eBilgi["noktalar"]:
                    if i==self.eBilgi["noktalar"][0]:
                         continue
                    p.lineTo(i)
               p.lineTo(self.eBilgi["noktalar"][-1])
          
          p1=painterStrock.createStroke(p)
          
          return p1


     