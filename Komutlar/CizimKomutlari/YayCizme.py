from Komutlar.CizimKomutlari.AnaKomut import AnaKomutCizim
from Komutlar.Elemanlar.Yay import UcNoktaYay
from Komutlar.Yardimcilar import Islemler,OnIzleme
from PyQt5.QtCore import QPointF

class UcNoktaYayCiz(AnaKomutCizim):
     def __init__(self,tahta,gv,komutPanel,parent=None):
          AnaKomutCizim.__init__(self,gv,tahta,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.komutPanel=komutPanel

     def onIzlemeBasla(self):
          pass
     
     def onIzlemeGuncelle(self):
          pass
     
     def onIzlemeBitir(self):
          pass

     def noktaEkle(self,nokta):
          #Aci Yakalam Daha Sonra Ekle == olucak ozmana
          if len(self.noktaListesi)>=0:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
               self.komutYaziIkinciNokta()
          else:
               pass
               # if len(self.yakalamaNoktasi)!=0:
               #      self.noktaListesi.append(self.yakalamaNoktasi[1])
               # elif len(self.aciYakalamaNoktasi)!=0:
               #      self.noktaListesi.append(self.aciYakalamaNoktasi[0])
               # else:
               #      self.noktaListesi.append(nokta)

     def noktaEkleKoordinat(self,koordinat):
          if len(self.noktaListesi)==0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIlkNokta()
          elif len(self.noktaListesi)!=0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIkinciNokta()
          if len(self.noktaListesi)==3:
               self.yayCizimSon()
     
     def noktaEkleUzunluk(self,uzunluk):
          if len(self.noktaListesi)!=0:
               if len(self.aciYakalamaNoktasi)!=0:
                    uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.aciYakalamaNoktasi[0])
                    self.noktaListesi.append(uzunluktakinokta)
                    self.komutYaziIkinciNokta()
                    if len(self.noktaListesi)==3:
                         self.yayCizimSon()
               else:
                    if self.fareN==None:
                         pass
                    else:
                         uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.fareN)
                         self.noktaListesi.append(uzunluktakinokta)
                         self.komutYaziIkinciNokta()
                         if len(self.noktaListesi)==3:
                              self.yayCizimSon()

     def komutYaziIlkNokta(self):
          self.komutYazi.addItem(f"İlk Nokta: x:{self.noktaListesi[0].x()},y:{self.noktaListesi[0].y()}")
          self.komutYazi.addItem(f"Noktayı Seciniz veya Uzunluk Giriniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()

     def komutYaziIkinciNokta(self):
          self.komutYazi.addItem(f"Nokta: x:{self.noktaListesi[-1].x()},y:{self.noktaListesi[-1].y()}")
          self.komutYazi.scrollToBottom()

     def yayCizimSon(self):
          if len(self.noktaListesi)==3:
               self.yayEkle(self.noktaListesi[0],self.noktaListesi[1],self.noktaListesi[2])
               self.onIzlemeBitir() 
               self.fareTakipBitir()
               self.tahta.sahneGuncelleme()

     def yayEkle(self,p1,p2,p3):
          self.yay=UcNoktaYay(self.tahta,p1,p2,p3)
          self.tahta.elemanEkle(self.yay)
          self.tahta.seciliKatmanElemanEkle(self.yay)
          self.tahta.secimObjesi.secimAcik=True
          self.komutPanel.komusBasladi=False
     
     def yakalamaNoktasiAl(self,ev,ynokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=ynokta

          #OnizlemeGuncelle Ekle
          self.onIzlemeGuncelle()

          # if len(self.noktaListesi)==1:
          #      self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[0],ev)

          self.tahta.sahneGuncelleme()
     
     
     def tiklamaNoktaAl(self,nokta):
          if len(self.noktaListesi)<=2:
               self.noktaEkle(nokta)
               
          self.yayCizimSon()
