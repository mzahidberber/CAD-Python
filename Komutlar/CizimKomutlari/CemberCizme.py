from Komutlar.CizimKomutlari.AnaKomut import AnaKomutCizim
from Komutlar.Elemanlar.Cember import Cember
from Komutlar.Yardimcilar import Islemler,OnIzleme
from PyQt5.QtCore import QPointF

class MerkezNoktaCemberCiz(AnaKomutCizim):
     def __init__(self,pencere,tahta,gv,komutPanel,parent=None):
          AnaKomutCizim.__init__(self,gv,tahta,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.pencere=pencere
          self.komutPanel=komutPanel

     def onIzlemeBasla(self):
          self.onizlemeCember=OnIzleme.OnIzlemeCember(self.tahta,QPointF(),0)
          self.tahta.addItem(self.onizlemeCember)
     
     def onIzlemeGuncelleMerkezNokta(self,p1,p2):
          r=Islemler.cizgiUzunlukBul(p1,p2)
          self.onizlemeCember.noktalariYenile(p1,r)
     
     def onIzlemeBitir(self):
          self.onizlemeCember.noktalariYenile(QPointF(),0)
          self.tahta.removeItem(self.onizlemeCember)

     def noktaEkleKoordinat(self,koordinat):
          if len(self.noktaListesi)==0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIlkNokta()
          elif len(self.noktaListesi)!=0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIkinciNokta()
               self.cemberCizimSon()
     
     def noktaEkleUzunluk(self,uzunluk):
          if len(self.noktaListesi)!=0:
               if len(self.aciYakalamaNoktasi)!=0:
                    uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.aciYakalamaNoktasi[0])
                    self.noktaListesi.append(uzunluktakinokta)
                    self.komutYaziIkinciNokta()
                    self.cemberCizimSon()
               else:
                    if self.fareN==None:
                         pass
                    else:
                         uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.fareN)
                         self.noktaListesi.append(uzunluktakinokta)
                         self.komutYaziIkinciNokta()
                         self.cemberCizimSon()

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
          self.komutYazi.addItem(f"İkinci Noktayı Seciniz veya Uzunluk Giriniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()

     def komutYaziIkinciNokta(self):
          self.komutYazi.addItem(f"İkinci Nokta: x:{self.noktaListesi[1].x()},y:{self.noktaListesi[1].y()}")
          self.komutYazi.scrollToBottom()

     def cemberCizimSon(self):
          if len(self.noktaListesi)==2:
               self.cemberEkle(self.noktaListesi[0],self.noktaListesi[1])
               self.onIzlemeBitir()
               self.fareTakipBitir()
               self.tahta.sahneGuncelleme()

     def cemberEkle(self,p1,p2):
          r=Islemler.cizgiUzunlukBul(p1,p2)
          self.cember=Cember(self.tahta,p1,r)
          self.tahta.elemanEkle(self.cember)
          self.tahta.seciliKatmanElemanEkle(self.cember)
          self.tahta.secimObjesi.secimAcik=True
          self.komutPanel.komusBasladi=False
     
     def yakalamaNoktasiAl(self,ev,ynokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=ynokta
          
          if len(self.noktaListesi)==1:
               self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[0],ev)
               if len(self.aciYakalamaNoktasi)!=0:
                    self.onIzlemeGuncelleMerkezNokta(self.noktaListesi[0],self.aciYakalamaNoktasi[0])
               else:
                    self.onIzlemeGuncelleMerkezNokta(self.noktaListesi[0],self.fareN)
          
          self.tahta.sahneGuncelleme()
     
     def tiklamaNoktaAl(self,nokta):
          
          if len(self.noktaListesi)<=1:
               self.noktaEkle(nokta)
               
          self.cemberCizimSon()

class UcNoktaCemberCiz(MerkezNoktaCemberCiz):
     def __init__(self,pencere,tahta,gv,komutPanel,parent=None):
          MerkezNoktaCemberCiz.__init__(self,pencere,tahta,gv,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.pencere=pencere
          self.komutPanel=komutPanel

     def onIzlemeGuncelleUcNokta(self,p1,p2,p3):
          merkezveYaricap=Islemler.merkezveYaricapBul(p1,p2,p3)
          merkez=QPointF(merkezveYaricap[0][0],merkezveYaricap[0][1])
          yaricap=merkezveYaricap[1]
          self.onizlemeCember.noktalariYenile(merkez,yaricap)  

     def komutYaziIlkNokta(self):
          self.komutYazi.addItem(f"İlk Nokta: x:{self.noktaListesi[0].x()},y:{self.noktaListesi[0].y()}")
          self.komutYazi.addItem(f"Noktayı Seciniz veya Uzunluk Giriniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()

     def komutYaziIkinciNokta(self):
          self.komutYazi.addItem(f"Nokta: x:{self.noktaListesi[-1].x()},y:{self.noktaListesi[-1].y()}")
          self.komutYazi.scrollToBottom()

     def noktaEkleKoordinat(self,koordinat):
          if len(self.noktaListesi)==0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIlkNokta()
          elif len(self.noktaListesi)!=0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIkinciNokta()
          if len(self.noktaListesi)==3:
               self.cemberCizimSon()
     
     def noktaEkleUzunluk(self,uzunluk):
          if len(self.noktaListesi)!=0:
               if len(self.aciYakalamaNoktasi)!=0:
                    uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.aciYakalamaNoktasi[0])
                    self.noktaListesi.append(uzunluktakinokta)
                    self.komutYaziIkinciNokta()
                    if len(self.noktaListesi)==3:
                         self.cemberCizimSon()
               else:
                    if self.fareN==None:
                         pass
                    else:
                         uzunluktakinokta=Islemler.uzunluktakiNoktayiBul(self.noktaListesi[-1], uzunluk, self.fareN)
                         self.noktaListesi.append(uzunluktakinokta)
                         self.komutYaziIkinciNokta()
                         if len(self.noktaListesi)==3:
                              self.cemberCizimSon()

     def cemberCizimSon(self):
          if len(self.noktaListesi)==3:
               self.cemberEkleUcNokta(self.noktaListesi[0],self.noktaListesi[1],self.noktaListesi[2])
               self.onIzlemeBitir()
               self.fareTakipBitir()
               self.tahta.sahneGuncelleme()
     
     def cemberEkleUcNokta(self,p1,p2,p3):
          merkezveYaricap=Islemler.merkezveYaricapBul(p1,p2,p3)
          merkez=QPointF(merkezveYaricap[0][0],merkezveYaricap[0][1])
          yaricap=merkezveYaricap[1]
          self.cember=Cember(self.tahta,merkez,yaricap)
          self.tahta.elemanEkle(self.cember)
          self.tahta.seciliKatmanElemanEkle(self.cember)
          self.tahta.secimObjesi.secimAcik=True
          self.komutPanel.komusBasladi=False

     def noktaEkle(self,nokta):
          if len(self.noktaListesi)==0:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
               self.komutYaziIlkNokta()
          elif len(self.noktaListesi)==1:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
               self.komutYaziIkinciNokta()
          else:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               elif len(self.aciYakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.aciYakalamaNoktasi[0])
               else:
                    self.noktaListesi.append(nokta)
               self.komutYaziIkinciNokta()

     
     
     def yakalamaNoktasiAl(self,ev,ynokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=ynokta
          if len(self.noktaListesi)==2:
               self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[0],ev)
               if len(self.aciYakalamaNoktasi)!=0:
                    self.onIzlemeGuncelleUcNokta(self.noktaListesi[0],self.noktaListesi[1],self.aciYakalamaNoktasi[0])
               else:
                    self.onIzlemeGuncelleUcNokta(self.noktaListesi[0],self.noktaListesi[1],self.fareN)
     
          self.tahta.sahneGuncelleme()
     
     def tiklamaNoktaAl(self,nokta):
          if len(self.noktaListesi)<=2:
               self.noktaEkle(nokta)
          
          self.cemberCizimSon()

class IkiNoktaCemberCiz(MerkezNoktaCemberCiz):
     def __init__(self,pencere,tahta,gv,komutPanel,parent=None):
          MerkezNoktaCemberCiz.__init__(self,pencere,tahta,gv,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.pencere=pencere
          self.komutPanel=komutPanel

     def cemberCizimSon(self):
          if len(self.noktaListesi)==2:
               self.cemberEkleIkiNokta(self.noktaListesi[0],self.noktaListesi[1])
               self.onIzlemeBitir()
               self.fareTakipBitir()
               self.tahta.sahneGuncelleme()

     def onIzlemeGuncelleIkiNokta(self,p1,p2):
          merkez=Islemler.cizgiOrtaNokta(p1,p2)
          yaricap=Islemler.cizgiUzunlukBul(p1,merkez)
          self.onizlemeCember.noktalariYenile(merkez,yaricap)
     
     def cemberEkleIkiNokta(self,p1,p2):
          merkez=Islemler.cizgiOrtaNokta(p1,p2)
          yaricap=Islemler.cizgiUzunlukBul(p1,merkez)
          self.cember=Cember(self.tahta,merkez,yaricap)
          self.tahta.elemanEkle(self.cember)
          self.tahta.seciliKatmanElemanEkle(self.cember)
          self.tahta.secimObjesi.secimAcik=True
          self.komutPanel.komusBasladi=False
          
     def yakalamaNoktasiAl(self,ev,ynokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=ynokta
          
          if len(self.noktaListesi)==1:
               self.aciYakalamaNoktasi=self.tahta.ay.aciYakalama(self.noktaListesi[0],ev)
               if len(self.aciYakalamaNoktasi)!=0:
                    self.onIzlemeGuncelleIkiNokta(self.noktaListesi[0],self.aciYakalamaNoktasi[0])
               else:
                    self.onIzlemeGuncelleIkiNokta(self.noktaListesi[0],self.fareN)
          
          self.tahta.sahneGuncelleme()
     
     def tiklamaNoktaAl(self,nokta):
          if len(self.noktaListesi)<=1:
               self.noktaEkle(nokta)
          
          self.cemberCizimSon()
                      

class MerkezYaricapCemberCiz(MerkezNoktaCemberCiz):
     def __init__(self,pencere,tahta,gv,komutPanel,parent=None):
          MerkezNoktaCemberCiz.__init__(self,pencere,tahta,gv,komutPanel,parent)
          self.tahta=tahta
          self.gv=gv
          self.pencere=pencere
          self.komutPanel=komutPanel

          

     def onIzlemeGuncelleMerkezYaricap(self,merkez,yaricap):
          self.onizlemeCember.noktalariYenile(merkez,yaricap)

     def komutYaziIlkNokta(self):
          self.komutYazi.addItem(f"Merkez: x:{self.noktaListesi[0].x()},y:{self.noktaListesi[0].y()}")
          self.komutYazi.scrollToBottom()

     def komutYaziYaricap(self):
          self.komutYazi.addItem(f"Yaricap:{self.komutPanel.varsayilanMYCYaricap}")
          self.komutYazi.addItem(f"Merkez Noktayi Seciniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()

     def noktaEkleKoordinat(self,koordinat):
          if len(self.noktaListesi)==0:
               self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
               self.komutYaziIlkNokta()
               self.cemberCizimSon()
     
     def noktaEkleUzunluk(self,uzunluk):
          self.komutPanel.MYCemberVarsayilanYaricapGuncelle(uzunluk)
          self.komutYaziYaricap()

     def cemberCizimSon(self):
          if len(self.noktaListesi)==1:
               yaricap=self.komutPanel.varsayilanMYCYaricap
               self.cemberEkleMerkezYaricap(self.noktaListesi[0],yaricap)
               self.onIzlemeBitir()
               self.fareTakipBitir()
               self.tahta.sahneGuncelleme()  
     
     def cemberEkleMerkezYaricap(self,merkez,yaricap):
          self.cember=Cember(self.tahta,merkez,yaricap)
          self.tahta.elemanEkle(self.cember)
          self.tahta.seciliKatmanElemanEkle(self.cember)
          self.tahta.secimObjesi.secimAcik=True
          self.komutPanel.komusBasladi=False
          
     def yakalamaNoktasiAl(self,ev,ynokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=ynokta
          
          if len(self.noktaListesi)==0:
               yaricap=self.komutPanel.varsayilanMYCYaricap
               self.onIzlemeGuncelleMerkezYaricap(self.fareN,yaricap)
          
          self.tahta.sahneGuncelleme()
     
     def tiklamaNoktaAl(self,nokta):
          if len(self.noktaListesi)==0:
               self.noktaEkle(nokta)

          self.cemberCizimSon()
          
             