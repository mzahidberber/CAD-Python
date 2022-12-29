from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import *
from Komutlar.Yardimcilar import OnIzleme,Islemler

class AnaKomutCizim(QGraphicsObject):
     def __init__(self,gv,tahta,komutPanel,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.tahta=tahta
          self.gv=gv
          self.komutPanel=komutPanel

          self.komutYazi=self.komutPanel.komutYazi

          self.yakalamaNoktasi=self.tahta.yakalamaNoktasiBilgi()
          self.aciYakalamaNoktasi=[]
          #self.fareN=None

          self.fareTakipBasla()
          self.onIzlemeBasla()

          self.noktaListesi=[]
          
          self.tahta.secimObjesi.secimAcik=False

     def fareTakipBasla(self):
          self.tahta.addItem(self)
          self.tahta.fareHareketKoordinat.connect(self.yakalamaNoktasiAl)
          self.tahta.fareTiklamaKoordinat.connect(self.tiklamaNoktaAl)

     def fareTakipBitir(self):
          self.tahta.fareHareketKoordinat.disconnect(self.yakalamaNoktasiAl)
          self.tahta.fareTiklamaKoordinat.disconnect(self.tiklamaNoktaAl)
          self.tahta.removeItem(self)

     def onIzlemeBasla(self):pass
     def onIzlemeGuncelle(self,p1,p2):pass
     def onIzlemeBitir(self):pass

     def komutYaziIptal(self):
          self.komutYazi.addItem(f"Komut Iptal Edildi.")
          self.komutYazi.scrollToBottom()
          self.komutPanel.komusBasladi=False

     def komutIptal(self):
          self.onIzlemeBitir()
          self.fareTakipBitir()
          self.tahta.sahneGuncelleme()
          self.komutYaziIptal()

     def yakalamaNoktasiAl(self,ev,ynokta):pass
     def tiklamaNoktaAl(self,tnokta):pass
     def paint(self, painter,option, widget):pass
     def boundingRect(self):return QRectF(0,0,0,0)  