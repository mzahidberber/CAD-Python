from UI.ArayuzUI import Ui_MainWindow
from UI.KatmanKutusuArayuz import KatmanKutusuArayuz

from PyQt5.QtWidgets import *

from .CizimTahtasi import CizimTahtasii

from Komutlar.DuzenlemeKomutlari import *
from Komutlar.CizimKomutlari import *
from Komutlar import KomutPanel

import time,threading

class View(QMainWindow):
     def __init__(self):
          super(View,self).__init__()
          self.ui=Ui_MainWindow()
          self.ui.setupUi(self)
          
          self.cizimTahtasi=CizimTahtasii(self)
          self.grafikGorunum=self.ui.grafikGorunum
          #Bu komuta tekrar bak bunu sinifta yazinca mouse hareketlerini almıyor
          self.grafikGorunum.setMouseTracking(True)

          self.grafikGorunum.setScene(self.cizimTahtasi)

          self.komutPaneli=KomutPanel.KomutPanel(self, self.cizimTahtasi, self.grafikGorunum)
          
          self.butonBaglantilari()

          self.komutPaneli.komutSatiri.setFocus()

          #Koordinat Yazi
          self.cizimTahtasi.fareHareketKoordinat.connect(self.fareKoordinatYazma)
          #Otomatik Sahne Yenileme
          #self.threadBaslat()
          
          self.komutSatiriTik=False
          self.gorunmezler()

          self.katmanKutusuu()
          
     def gorunmezler(self):
          self.ui.acikutu.hide()
          self.ui.ElemanBilgi.hide()

     def threadBaslat(self):
          thread=threading.Thread(target=self.otomatikSahneGuncelleme,args=("1"))
          thread.start()
     
     def otomatikSahneGuncelleme(self,thread):
          i=0
          while True:
               #print(f"Sahne Guncellendi:{i}")
               i+=1
               time.sleep(0.5)
               self.cizimTahtasi.sahneGuncelleme()
     
     def fareKoordinatYazma(self,ev):
          tarananN=ev.scenePos()
          self.ui.xkoordinat.setText(f"{round(tarananN.x(),4)}")
          self.ui.ykoordinat.setText(f"{round(tarananN.y(),4)}")
          self.cizimTahtasi.sahneGuncelleme()

     def keyPressEvent(self, event):
          QMainWindow.keyPressEvent(self,event) 
          self.komutPaneli.komutAl(event)

     def butonBaglantilari(self):   
          self.ui.actionCizgi.triggered.connect(self.cizgiButon)
          self.ui.actionSurekliCizgi.triggered.connect(self.sCizgiButon)
          self.ui.actionDikDortgen.triggered.connect(self.dikdortgenButon)
          self.ui.actionCember.triggered.connect(self.merkezNoktaCemberButon)
          self.ui.actionUcNoktaCember.triggered.connect(self.ucNoktaCemberButon)
          self.ui.actionIkiNoktaCember.triggered.connect(self.ikiNoktaCemberButon)
          self.ui.actionElips.triggered.connect(self.elipsButon)
          self.ui.actionYay.triggered.connect(self.ucNoktaYayButon)
          self.ui.actionMerkez_Yaricap_Cember.triggered.connect(self.merkezYaricapCemberButon)

          self.ui.actionTasima.triggered.connect(self.tasimaButon)
          self.ui.actionKopyala.triggered.connect(self.kopyalamaButon)
          self.ui.actionBoyutlandir.triggered.connect(self.boyutlandirButon)
          # self.ui.actionDondur.triggered.connect(self.dondurmeButon)
          # self.ui.actionOfset.triggered.connect(self.ofsetButon)
          # self.ui.actionAynala.triggered.connect(self.aynalamaButon)
          
          self.ui.actionUcNoktaYakalama.triggered.connect(self.ucNoktaYakalamaButon)
          self.ui.actionOrta_Nokta_Yakalama.triggered.connect(self.ortaNoktaYakalamaButon)
          self.ui.actionMerkez_Nokta_Yakalama.triggered.connect(self.merkezNoktaYakalamaButon)
          self.ui.actionKesi_im_Nokta_Yakalama.triggered.connect(self.kesisimNoktaYakalamaButon)

          self.ui.actionDik_Kisitlama.triggered.connect(self.dikKisitlamaButon)
          self.ui.actionAciKisitlama.triggered.connect(self.aciKisitlamaButon)
          
          self.ui.actionEleman_Bilgi.triggered.connect(self.elemanBilgiButon)
          self.ui.actionKomut_Sat_r.triggered.connect(self.komutSatiriButon)

          self.ui.actionKaydet.triggered.connect(self.kaydet)
          self.ui.actionFarkl_Kaydet.triggered.connect(self.farkliKaydet)
          self.ui.actionA.triggered.connect(self.dosyaOku)
          self.ui.actionYeni.triggered.connect(self.yeniDosya)
          self.ui.actioniceAktar.triggered.connect(self.iceAktar)
          self.ui.actionDisaAktar.triggered.connect(self.disaAktar)

          self.ui.katmanButon.clicked.connect(self.katmanDuzenlemeButon)
          self.ui.katmanlar.currentTextChanged.connect(self.katmanDegistirme)

     def elemanBilgiButon(self):self.ui.ElemanBilgi.show()
     def yeniDosya(self):self.komutPaneli.komutBasla("yenidosya")
     def dosyaOku(self):self.komutPaneli.komutBasla("ac")
     def farkliKaydet(self):self.komutPaneli.komutBasla("farklikaydet")
     def kaydet(self):self.komutPaneli.komutBasla("kaydet")
     def iceAktar(self):self.komutPaneli.komutBasla("iceaktar")
     def disaAktar(self):self.komutPaneli.komutBasla("disaaktar")
     def kopyalamaButon(self):self.komutPaneli.komutBasla("kopyala")
     def tasimaButon(self):self.komutPaneli.komutBasla("tasima")
     def boyutlandirButon(self):self.komutPaneli.komutBasla("boyutlandirma")
     # def dondurmeButon(self):self.komutPaneli.komutBasla("dondurme")
     def ofsetButon(self):self.komutPaneli.komutBasla("ofset")
     def aynalamaButon(self):self.komutPaneli.komutBasla("aynalama")
     def cizgiButon(self):self.komutPaneli.komutBasla("cizgi")
     def sCizgiButon(self):self.komutPaneli.komutBasla("sureklicizgi")
     def dikdortgenButon(self):self.komutPaneli.komutBasla("dikdortgen")
     def merkezNoktaCemberButon(self):self.komutPaneli.komutBasla("cembermn")
     def ucNoktaCemberButon(self):self.komutPaneli.komutBasla("cember3n")
     def ikiNoktaCemberButon(self):self.komutPaneli.komutBasla("cember2n")
     def merkezYaricapCemberButon(self):self.komutPaneli.komutBasla("cembermy")
     def elipsButon(self):self.komutPaneli.komutBasla("elips")
     def ucNoktaYayButon(self):self.komutPaneli.komutBasla("yay3n")
     
     def ucNoktaYakalamaButon(self):self.komutPaneli.komutBasla("ucnoktayakalama")
     def ortaNoktaYakalamaButon(self):self.komutPaneli.komutBasla("ortanoktayakalama")
     def merkezNoktaYakalamaButon(self):self.komutPaneli.komutBasla("merkeznoktayakalama")
     def kesisimNoktaYakalamaButon(self):self.komutPaneli.komutBasla("kesisimnoktayakalama")
     
     def aciKisitlamaButon(self,ev):self.komutPaneli.komutBasla("acikisitlama")
     def dikKisitlamaButon(self):self.komutPaneli.komutBasla("dikkisitlama")
     
     def katmanListesiGuncelle(self):self.katmanKutusu.katmanlariGuncelle()
     def katmanDegistirme(self,secilenKatman):self.katmanDuzenleme.seciliKatmanDegistir(secilenKatman)

     def katmanKutusuu(self):
          self.katmanDuzenleme=self.cizimTahtasi.katmanObjesi()
          self.katmanListesi=self.katmanDuzenleme.katmanListesiBilgi()
          katmanAdiListesi=[]
          for i in self.katmanListesi:
               katmanAdi=i.eBilgi["katmanAdi"]
               katmanAdiListesi.append(katmanAdi)
          self.ui.katmanlar.addItems(katmanAdiListesi)

     def katmanKutusuuBilgiGncell(self):
          secilikutu=self.ui.katmanlar.currentIndex()
          self.ui.katmanlar.clear()
          katmanAdiListesi=[]
          for i in self.katmanListesi:
               katmanAdi=i.eBilgi["katmanAdi"]
               katmanAdiListesi.append(katmanAdi)
          self.ui.katmanlar.addItems(katmanAdiListesi)
          self.ui.katmanlar.setCurrentIndex(secilikutu)
     
     def katmanDuzenlemeButon(self):
          self.katmanKutusu=KatmanKutusuArayuz(self.katmanDuzenleme)
          self.katmanListesiGuncelle()
          self.katmanKutusu.show()
          self.katmanKutusu.exec_()
          self.katmanKutusuuBilgiGncell()
     
     def komutSatiriButon(self):
          if self.komutSatiriTik==False:
               self.ui.KomutSatiriBox.hide()
               self.komutSatiriTik=True
          else:
               self.ui.KomutSatiriBox.show()
               self.komutSatiriTik=False  