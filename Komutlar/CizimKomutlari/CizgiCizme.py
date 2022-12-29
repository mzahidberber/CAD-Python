from Komutlar.CizimKomutlari.AnaKomut import AnaKomutCizim
from Komutlar.Elemanlar.Cizgi import Cizgi
from Komutlar.Yardimcilar import OnIzleme,Islemler
from PyQt5.QtCore import QPointF

class CizgiCiz(AnaKomutCizim):
     def __init__(self,gv,tahta,komutPanel,parent=None):
          AnaKomutCizim.__init__(self,gv,tahta,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.komutPanel=komutPanel
     
     def onIzlemeBasla(self):
          self.onizleme=OnIzleme.OnIzlemeCizgi(self.tahta,QPointF(),QPointF())
          self.tahta.addItem(self.onizleme)
     
     def onIzlemeGuncelle(self,p1,p2):
          self.onizleme.noktalariYenile(p1,p2)
     
     def onIzlemeBitir(self):
          self.onizleme.noktalariYenile(QPointF(),QPointF())
          self.tahta.removeItem(self.onizleme)

     def komutYaziIlkNokta(self):
          self.komutYazi.addItem(f"İlk Nokta: x:{self.noktaListesi[0].x()},y:{self.noktaListesi[0].y()}")
          self.komutYazi.addItem(f"İkinci Noktayı Seciniz veya Uzunluk Giriniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()

     def komutYaziIkinciNokta(self):
          self.komutYazi.addItem(f"İkinci Nokta: x:{self.noktaListesi[1].x()},y:{self.noktaListesi[1].y()}")
          self.komutYazi.scrollToBottom()

     def noktaEkleKoordinat(self,koordinat):
          if len(self.noktaListesi)==0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIlkNokta()
          
          elif len(self.noktaListesi)!=0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIkinciNokta()
               self.cizgiCizSon()
     
     def noktaEkleUzunluk(self,uzunluk):
          if len(self.noktaListesi)!=0:
               if len(self.aciYakalamaNoktasi)!=0:
                    uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[0], uzunluk, self.aciYakalamaNoktasi[0])
                    self.noktaListesi.append(uzunluktakinokta)
                    self.cizgiCizSon()
               else:
                    if self.fareN==None:
                         pass
                    else:
                         uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[0], uzunluk, self.fareN)
                         self.noktaListesi.append(uzunluktakinokta)
                         self.komutYaziIkinciNokta()
                         self.cizgiCizSon()
               
     
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

     def cizgiEkle(self,p1,p2):
          self.cizgi=Cizgi(self.tahta,p1,p2)
          self.tahta.elemanEkle(self.cizgi)
          self.tahta.seciliKatmanElemanEkle(self.cizgi)
          self.tahta.secimObjesi.secimAcik=True
          self.komutPanel.komusBasladi=False

     def cizgiCizSon(self):
          self.cizgiEkle(self.noktaListesi[0],self.noktaListesi[1])
          self.onIzlemeBitir()
          self.fareTakipBitir()
          self.tahta.sahneGuncelleme()
          
     
     def yakalamaNoktasiAl(self,ev,ynokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=ynokta
          
          if len(self.noktaListesi)==1:
               self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[0],ev)
               if len(self.aciYakalamaNoktasi)!=0:
                    self.onIzlemeGuncelle(self.noktaListesi[0],self.aciYakalamaNoktasi[0])
               else:
                    self.onIzlemeGuncelle(self.noktaListesi[0],self.fareN)
          
          self.tahta.sahneGuncelleme()
     
     def tiklamaNoktaAl(self,tnokta):
          if len(self.noktaListesi)<=1:
               self.noktaEkle(tnokta)
               
          if len(self.noktaListesi)==2:
               self.cizgiCizSon()