from Komutlar.CizimKomutlari.AnaKomut import AnaKomutCizim
from Komutlar.Elemanlar.Elips import Elips
from Komutlar.Yardimcilar import Islemler,OnIzleme
from PyQt5.QtCore import QPointF

class ElipsCizme(AnaKomutCizim):
     def __init__(self,tahta,gv,komutPanel,parent=None):
          AnaKomutCizim.__init__(self,gv,tahta,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.komutPanel=komutPanel

     def onIzlemeBasla(self):
          self.onIzlemeElips=OnIzleme.OnIzlemeElips(self.tahta,QPointF(),0,0)
          self.tahta.addItem(self.onIzlemeElips)
     
     def onIzlemeGuncelle1(self,p1,p2):
          r1=Islemler.cizgiUzunlukBul(p1,QPointF(p2.x(),p1.y()))
          self.onIzlemeElips.noktalariYenile(p1,r1,r1)
     
     def onIzlemeGuncelle2(self,p1,p2,p3):
          r1=Islemler.cizgiUzunlukBul(p1,QPointF(p2.x(),p1.y()))
          r2=Islemler.cizgiUzunlukBul(p1,QPointF(p1.x(),p3.y()))
          self.onIzlemeElips.noktalariYenile(p1,r1,r2)
     
     def onIzlemeBitir(self):
          self.onIzlemeElips.noktalariYenile(QPointF(),0,0)
          self.tahta.removeItem(self.onIzlemeElips)

     def noktaEkleKoordinat(self,koordinat):
          if len(self.noktaListesi)==0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIlkNokta()
          elif len(self.noktaListesi)!=0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIkinciNokta()
          if len(self.noktaListesi)==3:
               self.elipsCizimSon()
     
     def noktaEkleUzunluk(self,uzunluk):
          if len(self.noktaListesi)!=0:
               if len(self.aciYakalamaNoktasi)!=0:
                    uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.aciYakalamaNoktasi[0])
                    self.noktaListesi.append(uzunluktakinokta)
                    self.komutYaziIkinciNokta()
                    if len(self.noktaListesi)==3:
                         self.elipsCizimSon()
               else:
                    if self.fareN==None:
                         pass
                    else:
                         uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.fareN)
                         self.noktaListesi.append(uzunluktakinokta)
                         self.komutYaziIkinciNokta()
                         if len(self.noktaListesi)==3:
                              self.elipsCizimSon()

     def noktaEkle(self,nokta):
          if len(self.noktaListesi)==0:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
               self.komutYaziIlkNokta()
          else:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               elif len(self.aciYakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.aciYakalamaNoktasi[0])
               else:
                    self.noktaListesi.append(nokta)
               self.komutYaziIkinciNokta()
     
     def komutYaziIlkNokta(self):
          self.komutYazi.addItem(f"İlk Nokta: x:{self.noktaListesi[0].x()},y:{self.noktaListesi[0].y()}")
          self.komutYazi.addItem(f"Noktayı Seciniz veya Uzunluk Giriniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()

     def komutYaziIkinciNokta(self):
          self.komutYazi.addItem(f"Nokta: x:{self.noktaListesi[1].x()},y:{self.noktaListesi[1].y()}")
          self.komutYazi.scrollToBottom()

     def elipsCizimSon(self):
          if len(self.noktaListesi)==3:
               self.elipsEkle(self.noktaListesi[0],self.noktaListesi[1],self.noktaListesi[2])
               self.onIzlemeBitir()
               self.fareTakipBitir()
               self.tahta.sahneGuncelleme()

     def elipsEkle(self,p1,p2,p3):
          r1=Islemler.cizgiUzunlukBul(p1,QPointF(p2.x(),p1.y()))
          r2=Islemler.cizgiUzunlukBul(p1,QPointF(p1.x(),p3.y()))
          self.elips=Elips(self.tahta,p1,r1,r2)
          self.tahta.elemanEkle(self.elips) 
          self.tahta.seciliKatmanElemanEkle(self.elips)
          self.tahta.secimObjesi.secimAcik=True
          self.komutPanel.komusBasladi=False
     
     def yakalamaNoktasiAl(self,ev,nokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=nokta
          
          if len(self.noktaListesi)==1:
               self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[0],ev)
               if len(self.aciYakalamaNoktasi)!=0:
                    self.onIzlemeGuncelle1(self.noktaListesi[0],self.aciYakalamaNoktasi[0])
               else:
                    self.onIzlemeGuncelle1(self.noktaListesi[0],self.fareN)
          elif len(self.noktaListesi)==2:
               self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[0],ev)
               if len(self.aciYakalamaNoktasi)!=0:
                    self.onIzlemeGuncelle2(self.noktaListesi[0],self.noktaListesi[1],self.aciYakalamaNoktasi[0])
               else:
                    self.onIzlemeGuncelle2(self.noktaListesi[0],self.noktaListesi[1],self.fareN)
               
     
          self.tahta.sahneGuncelleme()
     
     def tiklamaNoktaAl(self,nokta):
          if len(self.noktaListesi)<=2:
               self.noktaEkle(nokta)
          
          self.elipsCizimSon()
     