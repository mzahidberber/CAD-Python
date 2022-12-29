from Komutlar.CizimKomutlari.AnaKomut import AnaKomutCizim
from Komutlar.Elemanlar.SurekliCizgi import SurekliCizgi,Dikdortgen
from Komutlar.Yardimcilar import OnIzleme,Islemler
from PyQt5.QtCore import QPointF

class SCizgiCiz(AnaKomutCizim):
     def __init__(self,tahta,gv,komutPanel,parent=None):
          AnaKomutCizim.__init__(self,gv,tahta,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.komutPanel=komutPanel

     def yakalamaNoktasiAl(self,ev,nokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=nokta
          
          if len(self.noktaListesi)>=1:
               self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[-1],ev)
               if len(self.aciYakalamaNoktasi)!=0:
                    self.onIzlemeGuncelle(self.noktaListesi[-1],self.aciYakalamaNoktasi[0])
               else:
                    self.onIzlemeGuncelle(self.noktaListesi[-1],self.fareN)
          
          self.tahta.sahneGuncelleme()
     
     def tiklamaNoktaAl(self,nokta):
          if len(self.noktaListesi)>=0:
               self.noktaEkle(nokta)
     
     def onIzlemeBasla(self):
          self.onizleme=OnIzleme.OnIzlemeCizgi(self.tahta,QPointF(),QPointF())
          self.tahta.addItem(self.onizleme)
     
     def onIzlemeGuncelle(self,p1,p2):
          self.onizleme.noktalariYenile(p1,p2)
     
     def onIzlemeBitir(self):
          self.onizleme.noktalariYenile(QPointF(),QPointF())
          self.tahta.removeItem(self.onizleme)

     def noktaEkle(self,nokta):
          if len(self.noktaListesi)==0:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
          elif len(self.noktaListesi)==1:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
               self.cizgiEkle(self.noktaListesi)
          else:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               elif len(self.aciYakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.aciYakalamaNoktasi[0])
               else:
                    self.noktaListesi.append(nokta)

          self.komutYaziNokta()
                    
          if len(self.noktaListesi)>2:
               self.cizgiGuncelle(self.noktaListesi)


     def noktaEkleKoordinat(self,koordinat):
          if len(self.noktaListesi)==0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziNokta()
          elif len(self.noktaListesi)!=0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziNokta()

          if len(self.noktaListesi)==2:
               self.cizgiEkle(self.noktaListesi)
          elif len(self.noktaListesi)>2:
               self.cizgiGuncelle(self.noktaListesi)
     
     def noktaEkleUzunluk(self,uzunluk):
          if len(self.noktaListesi)!=0:
               if len(self.aciYakalamaNoktasi)!=0:
                    uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.aciYakalamaNoktasi[0])
                    self.noktaListesi.append(uzunluktakinokta)
                    self.komutYaziNokta()
                    
                    if len(self.noktaListesi)==2:
                         self.cizgiEkle(self.noktaListesi)
               else:
                    if self.fareN==None:
                         pass
                    else:
                         uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.fareN)
                         self.noktaListesi.append(uzunluktakinokta)
                         self.komutYaziNokta()

                         if len(self.noktaListesi)==2:
                              self.cizgiEkle(self.noktaListesi)
          
          if len(self.noktaListesi)>2:
               self.cizgiGuncelle(self.noktaListesi)

          
     
     def komutYaziNokta(self):
          self.komutYazi.addItem(f"Nokta: x:{self.noktaListesi[-1].x()},y:{self.noktaListesi[-1].y()}")
          self.komutYazi.addItem(f"Noktayı Seciniz veya Uzunluk Giriniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()

     def cizgiGuncelle(self,liste):
          self.scizgi.bilgiNoktalariGuncelle(liste)
          self.tahta.sahneGuncelleme()

     def cizgiCizimSon(self):
          self.onIzlemeBitir()
          self.fareTakipBitir()
          self.tahta.sahneGuncelleme()
          self.tahta.secimObjesi.secimAcik=True
          self.komutPanel.komusBasladi=False

     def komutIptal(self):
          try:
               self.scizgi.kendiniSil()
          except Exception as ex:
               pass
          self.onIzlemeBitir()
          self.fareTakipBitir()
          self.tahta.sahneGuncelleme()
          self.komutYaziIptal()
     
     def cizgiEkle(self,liste):
          if len(self.noktaListesi)>=2:
               self.scizgi=SurekliCizgi(self.tahta,liste)
               self.tahta.elemanEkle(self.scizgi)
               self.tahta.seciliKatmanElemanEkle(self.scizgi)
               
class DikdortgenCiz(SCizgiCiz):
     def __init__(self,tahta,gv,komutPanel,parent=None):
          SCizgiCiz.__init__(self,tahta,gv,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.komutPanel=komutPanel

     def onIzlemeBasla(self):
          self.onIzlemeDik=OnIzleme.OnIzlemeDikdortgen(self.tahta,[])
          self.tahta.addItem(self.onIzlemeDik)
     
     def onIzlemeGuncelle(self,p1,p2):
          nListesi=self.nListesi(p1,p2)
          self.onIzlemeDik.noktalariYenile(nListesi)
     
     def onIzlemeBitir(self):
          self.onIzlemeDik.noktalariYenile([])
          self.tahta.removeItem(self.onIzlemeDik)

     def cizgiEkle(self,liste):
          if len(self.noktaListesi)>=2:
               self.dikdorgen=Dikdortgen(self.tahta,liste)
               self.tahta.elemanEkle(self.dikdorgen)
               self.tahta.seciliKatmanElemanEkle(self.dikdorgen)
               self.onIzlemeBitir()
               self.fareTakipBitir()
               self.tahta.sahneGuncelleme()
               self.tahta.secimObjesi.secimAcik=True
               self.komutPanel.komusBasladi=False

     def noktaEkleKoordinat(self,koordinat):
          if len(self.noktaListesi)==0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIlkNokta()
          elif len(self.noktaListesi)!=0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIkinciNokta()
               self.dikdortgenCizimSon()
     
     def noktaEkleUzunluk(self,uzunluk):
          if len(self.noktaListesi)!=0:
               if len(self.aciYakalamaNoktasi)!=0:
                    uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.aciYakalamaNoktasi[0])
                    self.noktaListesi.append(uzunluktakinokta)
                    self.komutYaziIkinciNokta()
                    self.dikdortgenCizimSon()
               else:
                    if self.fareN==None:
                         pass
                    else:
                         uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.fareN)
                         self.noktaListesi.append(uzunluktakinokta)
                         self.komutYaziIkinciNokta()
                         self.dikdortgenCizimSon()

     def noktaEkle(self,nokta):
          if len(self.noktaListesi)==0:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
          elif len(self.noktaListesi)==2:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
               self.cizgiEkle(self.noktaListesi)
          else:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               elif len(self.aciYakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.aciYakalamaNoktasi[0])
               else:
                    self.noktaListesi.append(nokta)

          self.komutYaziNokta()
                    
          if len(self.noktaListesi)>2:
               self.cizgiGuncelle(self.noktaListesi)

     

     def komutYaziIlkNokta(self):
          self.komutYazi.addItem(f"İlk Nokta: x:{self.noktaListesi[0].x()},y:{self.noktaListesi[0].y()}")
          self.komutYazi.addItem(f"İkinci Noktayı Seciniz veya Uzunluk Giriniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()

     def komutYaziIkinciNokta(self):
          self.komutYazi.addItem(f"İkinci Nokta: x:{self.noktaListesi[1].x()},y:{self.noktaListesi[1].y()}")
          self.komutYazi.scrollToBottom()
          
     def yakalamaNoktasiAl(self,ev,nokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=nokta
          
          if len(self.noktaListesi)>=1:
               self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[0],ev)
               if len(self.aciYakalamaNoktasi)!=0:
                    self.onIzlemeGuncelle(self.noktaListesi[0],self.aciYakalamaNoktasi[0])
               else:
                    self.onIzlemeGuncelle(self.noktaListesi[0],self.fareN)
          
          self.tahta.sahneGuncelleme()

     def dikdortgenCizimSon(self):
          if len(self.noktaListesi)==2:
               nListesi=self.nListesi(self.noktaListesi[0],self.noktaListesi[1])
               self.cizgiEkle(nListesi)
          
     def tiklamaNoktaAl(self,nokta):
          if len(self.noktaListesi)<=1:
               self.noktaEkle(nokta)
          
          self.dikdortgenCizimSon()

     def nListesi(self,p1,p2):
          dListe=[]
          dListe.append(QPointF(p1.x(),p1.y()))
          dListe.append(QPointF(p2.x(),p1.y()))
          dListe.append(QPointF(p2.x(),p2.y()))
          dListe.append(QPointF(p1.x(),p2.y()))
          dListe.append(QPointF(p1.x(),p1.y()))
          return dListe