from Komutlar.CizimKomutlari import CizgiCizme,CemberCizme,ElipsCizme,YayCizme,SCizgiCizme
from Komutlar.DuzenlemeKomutlari import Tasima,Kopyalama,Boyutlandirma,Dondurme,Aynalama,Ofset
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.Qt import *

class KomutPanel:
     def __init__(self,pencere,gs,gv):
          self.pencere=pencere
          self.gs=gs
          self.gv=gv
          
          self.komutYazi=self.pencere.ui.komutYazi
          
          self.komutSatiri=self.pencere.ui.komutSatiri
          self.komutSatiri.komutSinyal.connect(self.komutBasla)
          self.komutSatiri.koordinatSinyal.connect(self.koordinatBasla)
          self.komutSatiri.uzunlukSinyal.connect(self.uzunlukBasla)

          self.varsayilanMYCYaricap=50

          self.cizimObjeTipleri=(CizgiCizme.CizgiCiz,
          SCizgiCizme.SCizgiCiz,SCizgiCizme.DikdortgenCiz,
          CemberCizme.MerkezNoktaCemberCiz,CemberCizme.UcNoktaCemberCiz,
          CemberCizme.IkiNoktaCemberCiz,CemberCizme.MerkezYaricapCemberCiz,
          ElipsCizme.ElipsCizme,YayCizme.UcNoktaYayCiz)
          
          self.duzenlemeObjeTipleri=(Tasima.Tasima,Kopyalama.Kopyalama,Boyutlandirma.Boyutlandirma,Dondurme.Dondurme,
          Aynalama.Aynalama,Ofset.Ofset)

          self.komusBasladi=False

          self.ucNoktaYakalama=False
          self.ortaNoktaYakalama=False
          self.kesisimNoktaYakalama=False
          self.merkezNoktaYakalama=False
          self.dikKisitlama=False
          self.aciKisitlama=False
          
          self.komutListesi=[]
          self.komutListesi1=[]

          self.kisayollar()

     def MYCemberVarsayilanYaricapGuncelle(self,yaricap):
          self.varsayilanMYCYaricap=yaricap
     
     def kisayollar(self):
          self.delete=QShortcut(QKeySequence('Delete'),self.pencere)
          self.delete.activated.connect(self.deleteKisayol)

          self.escape=QShortcut(QKeySequence('Escape'),self.pencere)
          self.escape.activated.connect(self.escapeKisayol)

          # self.space=QShortcut(QKeySequence('Space'),self.pencere)
          # self.space.activated.connect(self.scapeKisayol)
     
     def deleteKisayol(self):
          if len(self.gs.secimObjesi.secilenElemanlar)!=0:
               for i in self.gs.secimObjesi.secilenElemanlar:
                    self.gs.elemanSil(i)
               self.gs.secimObjesi.secimTemizle()

     def escapeKisayol(self):
          self.komutSatiri.clear()
          self.komutSatiri.setFocus()
          self.komutIptal()
          self.gs.secimObjesi.secimTemizle()


     def cizimCiz(self,tip,yaricap=None):
          komutyazi=tip.title()
          self.komutYazi.addItem(f"Komut:{komutyazi}")
          if yaricap==True:
               self.komutYazi.addItem(f"Bir Nokta Seciniz veya Koordinat Giriniz Yaricap:{self.varsayilanMYCYaricap}")
          else:
               self.komutYazi.addItem("Bir Nokta Seciniz veya Koordinat Giriniz")
          self.komutYazi.scrollToBottom()
          self.komutListesi.append(tip)
          self.komusBasladi=True

     def duzenlemeKomut(self,tip,komut):
          komutyazi=tip.title()
          self.komutYazi.addItem(f"Komut:{komutyazi}")
          self.komutYazi.addItem("Elemanları Seciniz")
          if len(self.gs.secimObjesi.secilenElemanlar)!=0:
               komut.komutSatiriYazi("Tasima Noktasi Seciniz")
          self.komutYazi.scrollToBottom()
          self.komutListesi.append(tip)
          self.komusBasladi=True

     def komutIptal(self):
          if self.komusBasladi==True:
               self.komutListesi1[-1].komutIptal()

     def koordinatBasla(self,ev):
          if self.komusBasladi==True:
               if type(self.komutListesi1[-1]) in self.cizimObjeTipleri:
                    self.komutListesi1[-1].noktaEkleKoordinat(ev)
               elif type(self.komutListesi1[-1]) in self.duzenlemeObjeTipleri:
                    self.komutListesi1[-1].veriKoordinat(ev)

     def uzunlukBasla(self,ev):
          if self.komusBasladi==True:
               if type(self.komutListesi1[-1]) in self.cizimObjeTipleri:
                    self.komutListesi1[-1].noktaEkleUzunluk(ev)
               elif type(self.komutListesi1[-1]) in self.duzenlemeObjeTipleri:
                    self.komutListesi1[-1].veriUzunluk(ev)
     
     def komutBasla(self,ev):
          komut=ev.lower()
          if komut=="cizgi" and self.komusBasladi==False:self.cizgi(komut)
          elif komut=="sureklicizgi" and self.komusBasladi==False:self.surekliCizgi(komut)
          elif komut=="dikdortgen" and self.komusBasladi==False:self.dikdorgen(komut)
          elif komut=="cembermn" and self.komusBasladi==False:self.cemberMN(komut)
          elif komut=="cember3n" and self.komusBasladi==False:self.cember3N(komut)
          elif komut=="cember2n" and self.komusBasladi==False:self.cember2N(komut)
          elif komut=="cembermy" and self.komusBasladi==False:self.cemberMY(komut)
          elif komut=="elips" and self.komusBasladi==False:self.elips(komut)
          elif komut=="yay3n" and self.komusBasladi==False:self.yay3N(komut)
          
          elif komut=="tasima" and self.komusBasladi==False:self.tasima(komut)
          elif komut=="kopyala" and self.komusBasladi==False:self.kopyalama(komut)
          elif komut=="boyutlandirma" and self.komusBasladi==False:self.boyutlandirma(komut)
          elif komut=="dondurme" and self.komusBasladi==False:self.dondurme(komut)
          elif komut=="aynalama" and self.komusBasladi==False:self.aynalama(komut)
          elif komut=="ofset" and self.komusBasladi==False:self.ofset(komut)
          
          elif komut=="ac" and self.komusBasladi==False:self.ac(komut)
          elif komut=="kaydet" and self.komusBasladi==False:self.kaydet(komut)
          elif komut=="farklikaydet" and self.komusBasladi==False:self.farkliKaydet(komut)
          elif komut=="yenidosya" and self.komusBasladi==False:self.yeniDosya(komut)
          elif komut=="iceaktar" and self.komusBasladi==False:self.iceAktar(komut)
          elif komut=="disaaktar" and self.komusBasladi==False:self.disaAktar(komut)
          
          elif komut=="ucnoktayakalama":self.ucNoktaAcKapat(komut)
          elif komut=="ortanoktayakalama":self.ortaNoktaAcKapat(komut)
          elif komut=="merkeznoktayakalama":self.merkezNoktaAcKapat(komut)
          elif komut=="kesisimnoktayakalama":self.dikKisitlamaAcKapat(komut)
          
          elif komut=="dikkisitlama":self.dikKisitlamaAcKapat(komut)
          elif komut=="acikisitlama":self.aciKisitlamaAcKapat(komut)

     def komutEkle(self,komut,eleman):
          self.komutListesi1.append(eleman)
          self.cizimCiz(komut)

     def cizgi(self,komut):
          cizgi=CizgiCizme.CizgiCiz(self.gv,self.gs,self)
          self.komutEkle(komut,cizgi)
     
     def surekliCizgi(self,komut):
          sCizgi=SCizgiCizme.SCizgiCiz(self.gs,self.gv,self)
          self.komutEkle(komut,sCizgi)

     def dikdorgen(self,komut):
          dikdorgen=SCizgiCizme.DikdortgenCiz(self.gs,self.gv,self)
          self.komutListesi1.append(dikdorgen)
          self.cizimCiz(komut)

     def cemberMN(self,komut):
          cember=CemberCizme.MerkezNoktaCemberCiz(self.pencere, self.gs, self.gv,self)
          self.komutListesi1.append(cember)
          self.cizimCiz(komut)

     def cember3N(self,komut):
          cember=CemberCizme.UcNoktaCemberCiz(self.pencere, self.gs, self.gv,self)
          self.komutListesi1.append(cember)
          self.cizimCiz(komut)

     def cember2N(self,komut):
          cember=CemberCizme.IkiNoktaCemberCiz(self.pencere, self.gs, self.gv,self)
          self.komutListesi1.append(cember)
          self.cizimCiz(komut)

     def cemberMY(self,komut):
          cember=CemberCizme.MerkezYaricapCemberCiz(self.pencere, self.gs, self.gv,self)
          self.komutListesi1.append(cember)
          self.cizimCiz(komut,yaricap=True)

     def elips(self,komut):
          elips=ElipsCizme.ElipsCizme(self.gs,self.gv,self)
          self.komutListesi1.append(elips)
          self.cizimCiz(komut)

     def yay3N(self,komut):
          yay=YayCizme.UcNoktaYayCiz(self.gs,self.gv,self)
          self.komutListesi1.append(yay)
          self.cizimCiz(komut)

     def tasima(self,komut):
          tasima=Tasima.Tasima(self.gv,self.gs,self)
          self.komutListesi1.append(tasima)
          self.duzenlemeKomut(komut,tasima)

     def kopyalama(self,komut):
          kopyalama=Kopyalama.Kopyalama(self.gv,self.gs,self)
          self.komutListesi1.append(kopyalama)
          self.duzenlemeKomut(komut,kopyalama)

     def boyutlandirma(self,komut):
          boyutlandirma=Boyutlandirma.Boyutlandirma(self.gv,self.gs,self)
          self.komutListesi1.append(boyutlandirma)
          self.duzenlemeKomut(komut,boyutlandirma)

     def dondurme(self,komut):
          dondurme=Dondurme.Dondurme(self.gv,self.gs,self)
          self.komutListesi1.append(dondurme)
          self.duzenlemeKomut(komut,dondurme)
     
     def aynalama(self,komut):
          aynalama=Aynalama.Aynalama(self.gv,self.gs,self)
          self.komutListesi1.append(aynalama)
          self.duzenlemeKomut(komut,aynalama)

     def ofset(self,komut):
          ofset=Ofset.Ofset(self.gv,self.gs,self)
          self.komutListesi1.append(ofset)
          self.duzenlemeKomut(komut,ofset)

     def ac(self,komut):
          self.gs.kayit.okuma(self.komutYazi)
          self.pencere.katmanKutusuuBilgiGncell()

     def kaydet(self,komut):
          self.gs.kayit.dosyaUzerineKaydet(self.komutYazi)
          self.pencere.katmanKutusuuBilgiGncell()

     def farkliKaydet(self,komut):
          self.gs.kayit.dosyaBilgiYazma(self.komutYazi)
          self.pencere.katmanKutusuuBilgiGncell()
     
     def iceAktar(self,komut):
          self.gs.dxfKayit.okuma(self.komutYazi)
          self.pencere.katmanKutusuuBilgiGncell()

     def disaAktar(self,komut):pass

     def yeniDosya(self,komut):
          elemanListesi=self.gs.cizilenElemanListesiBilgi()
          for i in elemanListesi:i.kendiniSil()
          self.pencere.katmanDuzenleme.tumKatmanlariSil()
          self.pencere.katmanKutusuuBilgiGncell()
     
     def ucNoktaAcKapat(self,komut):
          if self.ucNoktaYakalama==False:
               self.gs.ny.eBilgi["ucn"]=True
               self.pencere.ui.actionUcNoktaYakalama.setChecked(True)
               self.komutYazi.addItem("Uc Nokta Yakalama Acildi")
               self.komutYazi.scrollToBottom()
               self.ucNoktaYakalama=True
          else:
               self.gs.ny.eBilgi["ucn"]=False
               self.pencere.ui.actionUcNoktaYakalama.setChecked(False)
               self.komutYazi.addItem("Uc Nokta Yakalama Kapatildi")
               self.komutYazi.scrollToBottom()
               self.ucNoktaYakalama=False
     
     def ortaNoktaAcKapat(self,komut):
          if self.ortaNoktaYakalama==False:
               self.gs.ny.eBilgi["ortan"]=True
               self.pencere.ui.actionOrta_Nokta_Yakalama.setChecked(True)
               self.ortaNoktaYakalama=True
               self.komutYazi.addItem("Orta Nokta Yakalama Acildi")
               self.komutYazi.scrollToBottom()
          else:
               self.gs.ny.eBilgi["ortan"]=False
               self.pencere.ui.actionOrta_Nokta_Yakalama.setChecked(False)
               self.ortaNoktaYakalama=False
               self.komutYazi.addItem("Orta Nokta Yakalama Kapatildi")
               self.komutYazi.scrollToBottom()
     
     def merkezNoktaAcKapat(self,komut):
          if self.merkezNoktaYakalama==False:
               self.gs.ny.eBilgi["merkezn"]=True
               self.pencere.ui.actionMerkez_Nokta_Yakalama.setChecked(True)
               self.merkezNoktaYakalama=True
               self.komutYazi.addItem("Merkez Nokta Yakalama Acildi")
               self.komutYazi.scrollToBottom()
          else:
               self.gs.ny.eBilgi["merkezn"]=False
               self.pencere.ui.actionMerkez_Nokta_Yakalama.setChecked(False)
               self.merkezNoktaYakalama=False
               self.komutYazi.addItem("Merkez Nokta Yakalama Kapatildi")
               self.komutYazi.scrollToBottom()
     
     def kesisimNoktaAcKapat(self,komut):
          if self.kesisimNoktaYakalama==False:
               self.gs.ny.eBilgi["kesisimn"]=True
               self.pencere.ui.actionKesi_im_Nokta_Yakalama.setChecked(True)
               self.kesisimNoktaYakalama=True
               self.komutYazi.addItem("Kesisim Nokta Yakalama Acildi")
               self.komutYazi.scrollToBottom()
          else:
               self.gs.ny.eBilgi["kesisimn"]=False
               self.pencere.ui.actionKesi_im_Nokta_Yakalama.setChecked(False)
               self.kesisimNoktaYakalama=False
               self.komutYazi.addItem("Kesisim Nokta Yakalama Kapatildi")
               self.komutYazi.scrollToBottom()
     
     def dikKisitlamaAcKapat(self,komut):
          if self.dikKisitlama==False:
               if self.aciKisitlama==True:
                    self.komutBasla("acikisitlama")
               self.gs.ay.eBilgi["x"]=True
               self.gs.ay.eBilgi["y"]=True
               self.pencere.ui.actionDik_Kisitlama.setChecked(True)
               self.dikKisitlama=True
               self.komutYazi.addItem("Dik Kisitlama Acildi")
               self.komutYazi.scrollToBottom()
          else:
               self.gs.ay.eBilgi["x"]=False
               self.gs.ay.eBilgi["y"]=False
               self.pencere.ui.actionDik_Kisitlama.setChecked(False)
               self.dikKisitlama=False
               self.komutYazi.addItem("Dik Kisitlama Kapatildi")
               self.komutYazi.scrollToBottom()

     def aciKisitlamaAcKapat(self,komut):
          if self.aciKisitlama==False:
               if self.dikKisitlama==True:
                    self.komutBasla("dikkisitlama")
               self.gs.ay.eBilgi["aci"]=True
               self.pencere.ui.acikutu.show()
               self.pencere.ui.actionAciKisitlama.setChecked(True)
               self.aciKisitlama=True
               self.komutYazi.addItem("Aci Kisitlama Acildi")
               self.komutYazi.scrollToBottom()
          else:
               self.gs.ay.eBilgi["aci"]=False
               self.pencere.ui.acikutu.hide()
               self.pencere.ui.actionAciKisitlama.setChecked(False)
               self.aciKisitlama=False
               self.komutYazi.addItem("Aci Kisitlama Kapatildi")
               self.komutYazi.scrollToBottom()

     def komutAl(self,veri):
          self.komutSatiri.setFocus()
          if veri.key()==Qt.Key_Enter or veri.key()==Qt.Key_Return or veri.key()==Qt.Key_Space:
               if self.komusBasladi==True:
                    if type(self.komutListesi1[-1])==SCizgiCizme.SCizgiCiz:
                         self.komutListesi1[-1].cizgiCizimSon()
                    elif type(self.komutListesi1[-1]) in self.duzenlemeObjeTipleri:
                         self.komutListesi1[-1].elemanSecmeOnayVer()
               elif len(self.komutListesi)!=0:self.komutBasla(self.komutListesi[-1])
          else:
               self.komutSatiri.setText(veri.text())
               self.sonKomut=veri.text()
          
class KomutSatiri(QLineEdit):

     komutSinyal=pyqtSignal(object)
     koordinatSinyal=pyqtSignal(object)
     uzunlukSinyal=pyqtSignal(object)

     def __init__(self,parent):
          QLineEdit.__init__(self,parent=parent)
          self.parent=parent

          self.yaziSinir=QRegExpValidator(QRegExp("^[A-Za-z0-9.,-]+$"),self)
          self.setValidator(self.yaziSinir)
          
          self.tamamlayici()

     def keyPressEvent(self, event):
          QLineEdit.keyPressEvent(self,event)
          if event.key()==Qt.Key_Space or event.key()==Qt.Key_Return or event.key()==Qt.Key_Enter:
               self.selectAll()
               
               try:
                    uzunluk=float(self.selectedText())
               except Exception as ex:
                    try:
                         koordinat=self.selectedText().split(",")
                         koordinatx=float(koordinat[0])
                         koordinaty=float(koordinat[1])
                    except Exception as ex:
                         self.komutSinyal.emit(self.selectedText())
                    else:
                         self.koordinatSinyal.emit([koordinatx,koordinaty])
               else:
                    self.uzunlukSinyal.emit(uzunluk)
               
               finally:
                    self.clear()
               
     def tamamlayici(self):
          self.komutIsimListesi=["Cizgi","SurekliCizgi","Dikdortgen","CemberMN",
          "Cember3N","Cember2N","CemberMY","Elips",
          "Yay3N","Tasima","Kopyala","Boyutlandirma","Aynalama","Dondurme","Ofset",
          "Ac","Kaydet","FarkliKaydet","YeniDosya",
          "İceAktar","DisaAktar","UcNoktaYakalama","OrtaNoktaYakalama","KesisimNoktaYakalama",
          "MerkezNoktaYakalama","DikKisitlama","AciKisitlama"]
          
          self.tamamlayici=QCompleter(self.komutIsimListesi)
          self.tamamlayici.setCaseSensitivity(Qt.CaseInsensitive)
          self.tamamlayici.setCompletionMode(QCompleter.InlineCompletion)
          
          self.setCompleter(self.tamamlayici)
               