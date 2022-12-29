from Komutlar.DuzenlemeKomutlari.AnaKomut import AnaKomutDuzenleme
from PyQt5.QtCore import *
from Komutlar.Elemanlar import *
from Komutlar.Yardimcilar import Islemler,OnIzleme

class Tasima(AnaKomutDuzenleme):
     def __init__(self,gv,gs,komutPanel):
          AnaKomutDuzenleme.__init__(self, gv, gs, komutPanel)
          self.gs=gs
          self.gv=gv
          self.komutPanel=komutPanel

     def komutBasla(self,x,y):
          if len(self.noktaListesi)==0:
               self.komutSatiriYazi("Tasima Noktasi Seciniz veya Koordinat Giriniz")
          elif len(self.noktaListesi)==1:
               self.elemanlariTasima(x,y)
               self.komutSatiriYazi("Nokta Seciniz veya Koordinat Giriniz veya Ölcü Giriniz")
          elif len(self.noktaListesi)==2:
               self.elemanlariTasima(x,y)
               self.noktaListesi.clear()

     def elemanlariTasima(self,x,y):
          for i in self.gs.secimObjesi.secilenElemanlar:i.tasima(x,y)
          self.noktaListesi.clear()
          self.gs.sahneGuncelleme()
          self.komutSatiriYazi("Elemanlar Tasindi")
          self.komutBitti()