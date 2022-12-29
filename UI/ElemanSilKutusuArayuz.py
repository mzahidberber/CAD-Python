from UI.ElemanSilKutusuUI import Ui_KatmanSil
from PyQt5.QtWidgets import *

class ElemanSilKutusu(QDialog):
     def __init__(self,katmanObjesi,silinenKatmanlar):
          super(ElemanSilKutusu,self).__init__()
          self.ui=Ui_KatmanSil()
          self.ui.setupUi(self)
          self.katmanObjesi=katmanObjesi
          self.silinenKatmanlar=silinenKatmanlar
          
          self.ui.Aktar.setChecked(True)
          
          self.ui.Aktar.toggled.connect(self.secim)
          self.ui.Sil.toggled.connect(self.secim)
          self.ui.katmanListesi.itemClicked.connect(self.secilenKatmanBilgi)
          self.ui.sonuc.clicked.connect(self.onaylandi)

          self.secilenKatmanAdi=None
          self.secimBilgi=None
          self.ui.sonuc.button(QDialogButtonBox.Ok).setEnabled(False)

          self.katmanListesiKatmanGoster()
          for i in self.silinenKatmanlar:
               silinenKatmanIndex=self.katmanListesi.index(i)
               self.silinenKatmanGizle(silinenKatmanIndex)

     def katmanListesiKatmanGoster(self):
          self.katmanListesi=self.katmanObjesi.katmanListesiBilgi()
          for i in self.katmanListesi:self.ui.katmanListesi.addItem(i.eBilgi["katmanAdi"])

     def silinenKatmanGizle(self,silinenKatmanIndex):
          self.ui.katmanListesi.item(silinenKatmanIndex).setHidden(True)
     
     def secim(self):
          secilen=self.sender()
          if secilen.isChecked():
               if secilen.text()=="Elemanları Katmana Aktar" and self.secilenKatmanAdi!=None:
                    self.secimBilgi="Aktar"
               elif secilen.text()=="Elemanları Sil":
                    self.secimBilgi="Sil"
                    self.ui.sonuc.button(QDialogButtonBox.Ok).setEnabled(True)
               else:
                    self.ui.sonuc.button(QDialogButtonBox.Ok).setEnabled(False)
     
     def secilenKatmanBilgi(self,ev):
          self.secilenKatmanAdi=ev.text()
          self.secimBilgi="Aktar"
          self.ui.sonuc.button(QDialogButtonBox.Ok).setEnabled(True)

     def onaylandi(self,ev):
          if ev.text()=="OK":
               if self.secimBilgi=="Aktar":
                    for i in self.katmanListesi:
                         if i.eBilgi["katmanAdi"]==self.secilenKatmanAdi:
                              self.secilenKatman=i
                              break
                    
                    elemanListesi=[]
                    for i in self.silinenKatmanlar:
                         elemanListesi.extend(i.elemanListesiBilgi())
                         self.katmanObjesi.katmanSil(i)
                    for i in elemanListesi:i.katmanGuncelle(self.secilenKatman)
               
               elif self.secimBilgi=="Sil":
                    elemanListesi=[]
                    for i in self.silinenKatmanlar:
                         elemanListesi.extend(i.elemanListesiBilgi())
                         self.katmanObjesi.katmanSil(i)
                    for i in elemanListesi:i.kendiniSil()
               else:
                    pass
          else:
               pass