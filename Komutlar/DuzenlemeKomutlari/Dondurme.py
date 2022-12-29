from Komutlar.DuzenlemeKomutlari.AnaKomut import AnaKomutDuzenleme
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QGraphicsObject
from Komutlar.Elemanlar import *
from Komutlar.Yardimcilar import Islemler,KalemOlusturucu

class Dondurme(AnaKomutDuzenleme):
     def __init__(self,gv,gs,komutPanel):
          AnaKomutDuzenleme.__init__(self, gv, gs, komutPanel)
          self.gs=gs
          self.gv=gv
          self.komutPanel=komutPanel

          self.gonye=Gonye(self.gs, QPointF())
          self.gs.elemanEkle(self.gonye)

     def komutBasla(self,derece):
          if len(self.noktaListesi)==0:
               self.komutSatiriYazi("Tasima Noktasi Seciniz veya Koordinat Giriniz")
          elif len(self.noktaListesi)==1:
               self.elemanlariDondur(derece)
               self.noktaListesi.clear()
          elif len(self.noktaListesi)==2:
               self.elemanlariDondur(derece)
               self.noktaListesi.clear()
          elif len(self.noktaListesi)==3:
               self.elemanlariDondur(derece)
               self.noktaListesi.clear()
    
     def komutBasladerece(self,derece):
          if len(self.noktaListesi)==0:
               self.komutSatiriYazi("Tasima Noktasi Seciniz veya Koordinat Giriniz")
          elif len(self.noktaListesi)==1:
               self.elemanlariDondur(derece)
               self.noktaListesi.clear()

     def elemanlariDondur(self,derece):
          for i in self.gs.secimObjesi.secilenElemanlar:i.dondurme(self.noktaListesi[0],derece)
          self.komutSatiriYazi("Elemanlar Döndürüldü.")
          self.gs.elemanSil(self.gonye)
          self.gs.sahneGuncelleme()
          self.komutBitti()

     def komutIptal(self):
          self.fareTakipBitir()
          self.gs.elemanSil(self.gonye)
          self.tahta.sahneGuncelleme()
          self.komutYaziIptal()
          self.elemanlarOnIzlemeBitir()

     def dereceBul(self,dnokta,p2,p1):
          egim1=Islemler.dogruEgimBulma(dnokta, p1)
          egim2=Islemler.dogruEgimBulma(dnokta, p2)
          aci=Islemler.ikiDogruArasiAciBulma(egim1, egim2)
          bolge=Islemler.noktaHangiBolgedeBul(dnokta, p2)
          bolge1=Islemler.noktaHangiBolgedeBul(dnokta, p1)
          yeniaci=aci
          if aci<0:aci=aci+180
          print("----------------------------")
          print(f"egim1:{egim1},egim2:{egim2},aci:{aci},,yeniaci:{yeniaci},bölge:{bolge},bölge1:{bolge1}")
          return aci
          

     def yakalamaNoktasiAl(self,ev,ynokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=ynokta
          if len(self.noktaListesi)==2:
               # if len(self.aciYakalamaNoktasi)!=0:
               #      xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.aciYakalamaNoktasi[0])
               # else:
               #      xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.fareN)
               derece=self.dereceBul(self.noktaListesi[0],self.noktaListesi[1],self.fareN)
               self.gonye.guncelle(self.noktaListesi[0],derece)
               self.elemanlarOnIzlemeDondurmeGuncelle(self.noktaListesi[0], derece)
        
          if len(self.noktaListesi)==1:
               self.aciYakalamaNoktasi=self.gs.ay.aciYakalama(self.noktaListesi[0],ev)
        
          self.tahta.sahneGuncelleme()

    
     def veriKoordinat(self,koordinat):
          if len(self.secimObjesi.secilenElemanlar)!=0 and self.secimOnay==False:
               self.komutSatiriYazi("Secimi Onaylayiniz")
          if self.secimOnay==True:
               if len(self.noktaListesi)==0:
                    self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
                    self.komutSatiriYazi("Yerlesme Noktasi Seciniz veya Derece Giriniz")
                    self.elemanlarOnIzlemeBasla()
                    self.gonye.guncelle(self.noktaListesi[0],0)

            # elif len(self.noktaListesi)!=0:
            #     self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
            #     xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.noktaListesi[1])
            #     self.komutBasla(xy[0], xy[1])

     def veriUzunluk(self,derece):
          if len(self.noktaListesi)!=0:
               self.komutBasla(derece)

     def noktaEkle(self,nokta):
          if len(self.noktaListesi)==0:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               else:
                    self.noktaListesi.append(nokta)
               self.gonye.guncelle(self.noktaListesi[0],0)
               self.komutSatiriYazi("Yerlesme Noktasi Seciniz veya Derece Giriniz")
               self.elemanlarOnIzlemeBasla()
          else:
               if len(self.yakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.yakalamaNoktasi[1])
               elif len(self.aciYakalamaNoktasi)!=0:
                    self.noktaListesi.append(self.aciYakalamaNoktasi[0])
               else:
                    self.noktaListesi.append(nokta)

     def tiklamaNoktaAl(self,tnokta):
          if len(self.secimObjesi.secilenElemanlar)!=0 and self.secimOnay==False:
               self.komutSatiriYazi("Secimi Onaylayiniz")
               
          if self.secimOnay==True:
               if len(self.noktaListesi)<=3:
                    self.noktaEkle(tnokta)
               if len(self.noktaListesi)==3:
                    derece=self.dereceBul(self.noktaListesi[0], self.noktaListesi[1], self.noktaListesi[2])
                    self.komutBasla(derece)


class Gonye(QGraphicsObject):
     def __init__(self,gs,merkez:QPointF,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.gs=gs
          self.merkez=merkez

          self.guncelle(self.merkez,0)
          
     def guncelle(self,merkez,aci):
          self.aci=aci
          self.merkez=merkez
          self.kare=QRectF(self.merkez.x()-100,self.merkez.y()-100,200,200)
     def paint(self, painter, option, widget):
          kalem=KalemOlusturucu.Kalem(1, QColor(255,255,255), "duz")
          painter.setPen(kalem)
          painter.scale(1,-1)
          painter.drawText(self.kare,Qt.AlignCenter,str(self.aci))
     def boundingRect(self):return self.kare