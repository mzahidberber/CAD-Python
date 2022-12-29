from PyQt5.QtWidgets import QGraphicsObject
from Komutlar.Yardimcilar import Tutamaclar

class CizimElemani(QGraphicsObject):
     def __init__(self,tahta,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.tahta=tahta

          self.setFlag(QGraphicsObject.ItemSendsGeometryChanges)
          self.setFlag(QGraphicsObject.ItemIsFocusable)

          katmanDuzenleme=self.tahta.katmanObjesi()
          self.seciliKatman=katmanDuzenleme.seciliKatman

          self.elemanSecimAcik()
     
     def boyutlandirma(self,boyutlandirmaNoktasi,oran):pass
     def dondurme(self,derece,dnokta):pass
     def tasima(self,x,y):pass
     def kopyalama(self,x,y):pass
     def onIzlemeBasla(self):pass
     def onIzlemeGuncelleTasimaveKopyalama(self,p1,p2):pass
     def onIzlemeGuncelleBoyutlandirma(self,ilkNokta,oran):pass
     def onIzlemeBitir(self):pass

     def kendiniSil(self):
          katman=self.eBilgi["katman"]
          katman.elemanCikar(self)
          self.tahta.removeItem(self)
     
     def katmanGuncelle(self,katman):
          self.eBilgi["katman"]=katman
          katman.elemanEkle(self)

     def katmanKalemi(self):
          self.katmanKalem=self.eBilgi["katman"].katmanKalemiBilgi()
          return self.katmanKalem
          
     def kendiKalemi(self):
          self.kendiKalem=self.eBilgi["kalem"]
          return self.kendiKalem

     def kendiKalemNoneYap(self):self.eBilgi["kalem"]=None

     def kalemAyari(self,painter):
          kendiKalemi=self.kendiKalemi()
          katmanKalemi=self.katmanKalemi()
          if kendiKalemi!=None:
               painter.setPen(kendiKalemi)
          else:
               painter.setPen(katmanKalemi)

     def elemanGizle(self):self.hide()
     def elemanGoster(self):self.show()
     def elemanSecimKapali(self):self.setFlag(QGraphicsObject.ItemIsSelectable,False)
     def elemanSecimAcik(self):self.setFlag(QGraphicsObject.ItemIsSelectable,True)

     def normalTutamacEkle(self,nokta,konum:str):
          tutamacIsim=Tutamaclar.Tutamac(self.tahta,nokta)
          tutamacIsim.setParentItem(self)
          if konum=="uc":
               tutamacIsim.eBilgi["konum"]="uc"
          elif konum=="mrkz":
               tutamacIsim.eBilgi["konum"]="mrkz"
          elif konum=="ortan":
               tutamacIsim.eBilgi["konum"]="ortan"
          return tutamacIsim
     
     def boyutlandirmaTutamacEkle(self,nokta,konum:str):
          tutamacIsim=Tutamaclar.BoyutlandirmaTutamac(self.tahta,nokta)
          tutamacIsim.setParentItem(self)
          if konum=="uc":
               tutamacIsim.eBilgi["konum"]="uc"
          elif konum=="mrkz":
               tutamacIsim.eBilgi["konum"]="mrkz"
          elif konum=="ortan":
               tutamacIsim.eBilgi["konum"]="ortan"
          return tutamacIsim

     def itemChange(self, change , value):

          if change == self.ItemPositionChange and self.scene():
               pass

          elif change==self.ItemRotationChange and self.scene():
               pass

          elif change==self.ItemScaleChange and self.scene():
               pass

          elif change==self.ItemTransformOriginPointChange and self.scene():
               pass
          
          elif change==self.ItemSelectedChange and self.scene():
               pass
          
          return super(CizimElemani, self).itemChange(change, value)
     
     def paint(self, painter,option, widget):pass
     def boundingRect(self):pass

     
