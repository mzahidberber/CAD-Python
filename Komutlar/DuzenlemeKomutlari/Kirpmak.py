from Komutlar.DuzenlemeKomutlari.AnaKomut import AnaKomutDuzenleme
from PyQt5.QtCore import *
from Komutlar.Elemanlar import *
from Komutlar.Yardimcilar import Islemler

class Kirpma(AnaKomutDuzenleme):
    def __init__(self,gv,gs,komutPanel):
        AnaKomutDuzenleme.__init__(self, gv, gs, komutPanel)
        self.gs=gs
        self.gv=gv
        self.komutPanel=komutPanel