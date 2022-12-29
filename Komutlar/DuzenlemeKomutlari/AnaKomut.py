from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import OnIzleme,Islemler

class AnaKomutDuzenleme(QGraphicsObject):
     def __init__(self,gv,tahta,komutPanel,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.tahta=tahta
          self.gv=gv
          self.komutPanel=komutPanel

          self.komutYazi=self.komutPanel.komutYazi

          self.secimObjesi=self.tahta.secimObjesi

          self.yakalamaNoktasi=self.tahta.yakalamaNoktasiBilgi()
          self.aciYakalamaNoktasi=[]
          self.fareN=None

          self.noktaListesi=[]

          self.fareTakipBasla()

          self.secimOnay=False
          self.elemanSecmeOnayVer()

     def paint(self, painter,option, widget):pass
     def boundingRect(self):return QRectF(0,0,0,0) 

     def elemanlarOnIzlemeBasla(self):
          for i in self.gs.secimObjesi.secilenElemanlar:i.onIzlemeBasla()
     def elemanlarOnIzlemeBitir(self):
          for i in self.gs.secimObjesi.secilenElemanlar:i.onIzlemeBitir()
     def elemanlarOnIzlemeGuncelleTasimaveKopyalama(self,x,y):
          for i in self.gs.secimObjesi.secilenElemanlar:i.onIzlemeGuncelleTasimaveKopyalama(x,y)
     def elemanlarOnIzlemeBoyutlandirmaGuncelle(self,boyutlandirmaNokta,oran):
          for i in self.gs.secimObjesi.secilenElemanlar:i.onIzlemeGuncelleBoyutlandirma(boyutlandirmaNokta,oran)
     def elemanlarOnIzlemeDondurmeGuncelle(self,dnokta,derece):
          for i in self.gs.secimObjesi.secilenElemanlar:i.onIzlemeGuncelleDondurme(dnokta,derece)

     def fareTakipBasla(self):
          self.tahta.addItem(self)
          self.tahta.fareHareketKoordinat.connect(self.yakalamaNoktasiAl)
          self.tahta.fareTiklamaKoordinat.connect(self.tiklamaNoktaAl)

     def fareTakipBitir(self):
          self.tahta.fareHareketKoordinat.disconnect(self.yakalamaNoktasiAl)
          self.tahta.fareTiklamaKoordinat.disconnect(self.tiklamaNoktaAl)
          self.tahta.removeItem(self)

     def komutYaziIptal(self):
          self.komutYazi.addItem(f"Komut Iptal Edildi.")
          self.komutYazi.scrollToBottom()
          self.komutPanel.komusBasladi=False
          self.secimObjesi.secimAc()

     def komutIptal(self):
          self.fareTakipBitir()
          self.tahta.sahneGuncelleme()
          self.komutYaziIptal()
          self.elemanlarOnIzlemeBitir()

     def komutBitti(self):
          self.fareTakipBitir()
          self.komutPanel.komusBasladi=False
          self.secimObjesi.secimAc()
          self.tahta.sahneGuncelleme()
          self.elemanlarOnIzlemeBitir()

     def komutSatiriYazi(self,yazi):
          self.komutYazi.addItem(f"{yazi}")
          self.komutYazi.scrollToBottom()

     def elemanSecmeOnayVer(self):
          if len(self.secimObjesi.secilenElemanlar)!=0:
               self.secimOnay=True
               self.komutSatiriYazi("Tasima Noktasi Seciniz veya Koordinat Giriniz")
               self.secimObjesi.secimKapat()
               self.secimObjesi.secilenElemanlarTutamacSil()
          else:
               self.komutSatiriYazi("Eleman Seciniz")

     def elemanSecmeOnayKapat(self):
          self.secimOnay=False

     def yakalamaNoktasiAl(self,ev,ynokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=ynokta

          if len(self.noktaListesi)==1:
               self.aciYakalamaNoktasi=self.gs.ay.aciYakalama(self.noktaListesi[0],ev)
          
          if len(self.noktaListesi)==1:
               if len(self.aciYakalamaNoktasi)!=0:
                    xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.aciYakalamaNoktasi[0])
               else:
                    xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.fareN)
               
               self.elemanlarOnIzlemeGuncelleTasimaveKopyalama(xy[0], xy[1])
          
          self.tahta.sahneGuncelleme()
     
     def tiklamaNoktaAl(self,tnokta):
          if len(self.secimObjesi.secilenElemanlar)!=0 and self.secimOnay==False:
               self.komutSatiriYazi("Secimi Onaylayiniz")
          if self.secimOnay==True:
               if len(self.noktaListesi)==0:
                    self.noktaEkle(tnokta)
               elif len(self.noktaListesi)==1:
                    self.noktaEkle(tnokta)
               if len(self.noktaListesi)==2:
                    xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.noktaListesi[1])
                    self.komutBasla(xy[0], xy[1])
     
     def veriKoordinat(self,koordinat):
          if len(self.secimObjesi.secilenElemanlar)!=0 and self.secimOnay==False:
               self.komutSatiriYazi("Secimi Onaylayiniz")
          if self.secimOnay==True:
               if len(self.noktaListesi)==0:
                    self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
                    self.komutSatiriYazi("Yerlesme Noktasi Seciniz veya Koordinat veya Ölcü Giriniz")
                    self.elemanlarOnIzlemeBasla()

               elif len(self.noktaListesi)!=0:
                    self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
                    xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.noktaListesi[1])
                    self.komutBasla(xy[0], xy[1])

     def veriUzunluk(self,uzunluk):
          if len(self.noktaListesi)!=0:
               if len(self.aciYakalamaNoktasi)!=0:
                    uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[0], uzunluk, self.aciYakalamaNoktasi[0])
                    self.noktaListesi.append(uzunluktakinokta)
                    xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.noktaListesi[1])
                    self.komutBasla(xy[0], xy[1])
               else:
                    if self.fareN==None:
                         pass
                    else:
                         uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[0], uzunluk, self.fareN)
                         self.noktaListesi.append(uzunluktakinokta)
                         xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.noktaListesi[1])
                         self.komutBasla(xy[0], xy[1])

     def noktaEkle(self,nokta):
          if len(self.noktaListesi)==0:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
               self.komutSatiriYazi("Yerlesme Noktasi Seciniz veya Koordinat veya Ölcü Giriniz")
               self.elemanlarOnIzlemeBasla()
          else:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               elif len(self.aciYakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.aciYakalamaNoktasi[0])
               else:
                    self.noktaListesi.append(nokta)