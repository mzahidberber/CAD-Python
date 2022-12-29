from PyQt5.QtWidgets import QGraphicsObject,QGraphicsRectItem
from PyQt5.QtCore import *
from Komutlar.Elemanlar import *
from Komutlar.Yardimcilar import Ayarlar,Tutamaclar,KalemOlusturucu
from Komutlar.Yardimcilar.OnIzleme import OnIzlemeDikdortgenSecim

class Secme:
     def __init__(self,gs):
          self.gs=gs
          self.secilenElemanlar=[]
          self.secimAcik=True

          self.isaretlemeKalemi=Ayarlar.cizgiIsaretlemeKalem
          
          #self.secimDikdorgenAlanEkle()
          self.secimDikdorgeni=None
          

     def secimDikdorgenGuncelle(self,dikdorgen):
          if self.secimDikdorgeni!=None:
               koordinat=dikdorgen.getCoords()
               genislik=dikdorgen.width()
               yukseklik=dikdorgen.height()
               self.secimDikdorgeni.setRect(koordinat[0], koordinat[1], genislik, yukseklik)
     
     def secimDikdorgenAlanEkle(self):
          self.secimDikdorgeni=QGraphicsRectItem(0,0, 0, 0)
          self.secimDikdorgeni.setPen(self.isaretlemeKalemi)
          self.gs.addItem(self.secimDikdorgeni)

     def secimKapat(self):
          self.secimAcik=False

     def secimAc(self):
          self.secimAcik=True

     def secilenElemanListesiBilgi(self):
          return self.secilenElemanlar

     def secilenElemanlaraTutamacEkle(self,sElemanlar):
          if len(sElemanlar)!=0:
               for i in sElemanlar:
                    i.tutamaclariEkle()
     
     
     def secilenElemanlardanTutamacSil(self,cElemanlar):
          if len(cElemanlar)!=0:
               for i in cElemanlar:
                    i.tutamaclariSil()

     def secilenElemanlarTutamacSil(self):
          if self.secilenElemanlar!=0:
               for i in self.secilenElemanlar:
                    i.tutamaclariSil()
     
     
     def secimTemizle(self):
          if self.secimAcik==True:
               self.secilenElemanVarsayilanCevirme()
               self.secilenElemanlardanTutamacSil(self.secilenElemanlar)
               self.secilenElemanlar.clear()
               self.secimDikdorgenGuncelle(QRectF(0,0,0,0))
               self.gs.sahneGuncelleme()


     def secilenElemanVarsayilanCevirme(self):
          for i in self.secilenElemanlar:
               i.eBilgi["kalem"]=None

     def secilenElemanlarinBelirtilmesi(self):
          for i in self.secilenElemanlar:
               elemanKatmanKalinlik=i.eBilgi["katman"].eBilgi["cKalinlik"]
               elemanKatmanTip=i.eBilgi["katman"].eBilgi["cTip"]
               self.isaretlemeKalemi=KalemOlusturucu.Kalem(elemanKatmanKalinlik, Ayarlar.cizgiIsaretlemeRenk,elemanKatmanTip)
               i.eBilgi["kalem"]=self.isaretlemeKalemi

     def secilenElemanDikdorgenAlani(self):
          dikdorgen=QRectF()
          if len(self.secilenElemanlar)!=0:
               for i in self.secilenElemanlar:
                    dikdorgen |= i.sceneBoundingRect()
          
          self.secimDikdorgenGuncelle(dikdorgen)
          return dikdorgen

          
     def listeyeElemanEkle(self,secilenElemanListesi):
          if self.secimAcik==True:
               for i in secilenElemanListesi:
                    if self.secilenElemanlar.count(i)==0:
                         self.secilenElemanlar.append(i)
               if len(self.secilenElemanlar)<=5:
                    self.secilenElemanlaraTutamacEkle(self.secilenElemanlar)
               else:
                    self.secilenElemanlarTutamacSil()
               self.secilenElemanDikdorgenAlani()
               self.secilenElemanlarinBelirtilmesi()
               self.gs.sahneGuncelleme()
     
     def listedenElemanCikar(self,cikarilanElemanListesi):
          if self.secimAcik==True:
               for i in cikarilanElemanListesi:
                    if i in self.secilenElemanlar:
                         self.secilenElemanlar.remove(i)
                    i.eBilgi["kalem"]=None
               if len(self.secilenElemanlar)<=5:
                    self.secilenElemanlaraTutamacEkle(self.secilenElemanlar)
               self.secilenElemanDikdorgenAlani()
               self.secilenElemanlardanTutamacSil(cikarilanElemanListesi)
               self.secilenElemanlarinBelirtilmesi()
               self.gs.sahneGuncelleme()

class SecimKutusuCizim(QGraphicsObject):
     def __init__(self,tahta,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.tahta=tahta
          
          self.fareTakipBasla()
          self.onIzlemeBasla()

          self.noktaListesi=[]
     
     def fareTakipBasla(self):
          self.tahta.addItem(self)
          self.tahta.fareHareketKoordinat.connect(self.yakalamaNoktasiAl)
          self.tahta.fareTiklamaKoordinat.connect(self.tiklamaNoktaAl)

     def fareTakipBitir(self):
          self.tahta.fareHareketKoordinat.disconnect(self.yakalamaNoktasiAl)
          self.tahta.fareTiklamaKoordinat.disconnect(self.tiklamaNoktaAl)
          self.tahta.removeItem(self)
     
     def onIzlemeBasla(self):
          self.onIzlemeDik=OnIzlemeDikdortgenSecim([])
          self.tahta.addItem(self.onIzlemeDik)
     
     def onIzlemeGuncelle(self,p1,p2):
          nListesi=self.nListesi(p1,p2)
          self.onIzlemeDik.noktalariYenile(nListesi)
     
     def onIzlemeBitir(self):
          self.onIzlemeDik.noktalariYenile([])
          self.tahta.removeItem(self.onIzlemeDik)

     def noktaEkle(self,nokta):
          """
          if len(self.yakalamaNoktasi)!=0:
               self.noktaListesi.append(self.yakalamaNoktasi[1])
          else:
          """
          self.noktaListesi.append(nokta)

     def yakalamaNoktasiAl(self,ev,nokta):
          self.fareN=ev.scenePos()
          self.yakalamaNoktasi=nokta
          
          if len(self.noktaListesi)>=1:
               self.onIzlemeGuncelle(self.noktaListesi[0],self.fareN)
          
          self.tahta.sahneGuncelleme()
          
     def tiklamaNoktaAl(self,nokta):
          if len(self.noktaListesi)<=1:
               self.noktaEkle(nokta)
          
          if len(self.noktaListesi)==2:
               self.tahta.setSelectionArea(self.onIzlemeDik.shape())
               self.tahta.secimObjesi.listeyeElemanEkle(self.tahta.selectedItems())
               self.fareTakipBitir()
               self.onIzlemeBitir()
               self.tahta.sahneGuncelleme()

     def paint(self, painter,option, widget):
          pass
          
     def boundingRect(self):
          return QRectF(0,0,0,0)  

     def nListesi(self,p1,p2):
          dListe=[]
          dListe.append(QPointF(p1.x(),p1.y()))
          dListe.append(QPointF(p2.x(),p1.y()))
          dListe.append(QPointF(p2.x(),p2.y()))
          dListe.append(QPointF(p1.x(),p2.y()))
          dListe.append(QPointF(p1.x(),p1.y()))
          return dListe   