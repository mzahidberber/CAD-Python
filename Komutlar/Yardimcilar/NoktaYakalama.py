from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Komutlar.Yardimcilar import Ayarlar,Islemler
from Komutlar.Elemanlar import Cizgi,Cember,Elips,SurekliCizgi,Yay


class NoktaYakalama:
     def __init__(self,gs):
          self.gs=gs
          
          self.eBilgi={
               "ucn":bool,
               "ortan":bool,
               "merkezn":bool,
               "herhangin":bool,
               "kesisimn":bool,
               "grid":bool
          }

          self.yaricap=Ayarlar.nYakalamaYaricap
          self.yaricapn=QPointF(self.yaricap,self.yaricap)

          #yay ekle
          self.objetipleri=(Cizgi.Cizgi,SurekliCizgi.SurekliCizgi,Cember.Cember,Elips.Elips,Yay.UcNoktaYay)
          self.mrkzobjetipleri=(Cember.Cember,Elips.Elips,Yay.UcNoktaYay)
          self.ortobjetipleri=(Cizgi.Cizgi,SurekliCizgi.SurekliCizgi)
          self.kesisimobjetipleri=(Cizgi.Cizgi)
     
          self.bosListe=[]
          self.ucNoktaSekilEkle()
          self.ortaNoktaSekilEkle()
          self.merkezNoktaSekilEkle()
          self.kesisimNoktaSekilEkle()
               
     def tarama(self,ev):
          self.taramaN=ev.scenePos()
          taramaAlan=QRectF((self.taramaN-self.yaricapn).x(),(self.taramaN-self.yaricapn).y(),self.yaricap*2,self.yaricap*2)
          tarananObjeler=self.gs.items(taramaAlan)
          return tarananObjeler

     def tarananObjelerFiltreli(self,objetipi,ev):
          tarananObjeler=self.tarama(ev)
          tarananObjeler=list(filter(lambda x:isinstance(x,objetipi),tarananObjeler))
          return tarananObjeler

     def surekliCizgiNoktalar(self,tarananObje):
          if tarananObje==SurekliCizgi.SurekliCizgi:
               pass
          #SurekliCizgiyi Parcalara Ayırmak İcin kod

     def yakalamaNoktasi(self,ev):
          ucListe=self.ucNoktaYakalama(ev)
          mrkzListe=self.mrkzNoktaYakalama(ev)
          ortListe=self.ortNoktaYakalama(ev)
          kesisimListe=self.kesisimNoktaYakalama(ev)
          
          enyakinNokta=self.enYakinNoktaBul(ucListe+mrkzListe+ortListe+kesisimListe)
          #print(enyakinNokta)
          if len(enyakinNokta)!=0:
               if enyakinNokta[0]=="uc":
                    self.ucNoktaSekilTasima(enyakinNokta[1])
               elif enyakinNokta[0]=="ortan":
                    self.ortaNoktaTasima(enyakinNokta[1])
               elif enyakinNokta[0]=="mrkz":
                    self.merkezNoktaSekilHareket(enyakinNokta[1])
               elif enyakinNokta[0]=="kesisimn":
                    self.kesisimNoktaSekilHareket(enyakinNokta[1])
               return enyakinNokta
          else:
               self.ortaNoktaSekilKapat()
               self.merkezNoktaSekilKapat()
               self.ucNoktaSekilKapat()
               self.kesisimNoktaSekilKapat()
               return enyakinNokta
          return enyakinNokta
               
     
     def enYakinNoktaBul(self,noktaListesi):
          if len(noktaListesi)!=0:
               uzunlukL=[]
               for i in noktaListesi:
                    uzunluk=Islemler.cizgiUzunlukBul(self.taramaN,i[1])
                    uzunlukL.append(uzunluk)
               indeks=uzunlukL.index(min(uzunlukL))
               enyakinnokta=noktaListesi[indeks]
               return enyakinnokta
          return self.bosListe
     
     def ucNoktaYakalama(self,ev):
          if self.eBilgi["ucn"]==True:
               tarananObjeler=self.tarananObjelerFiltreli(self.objetipleri,ev)
               if len(tarananObjeler)!=0:
                    ucnnoktaListesi=[]
                    for i in tarananObjeler:
                         for i in i.eBilgi["noktalar"]:ucnnoktaListesi.append(["uc",i])
                    return ucnnoktaListesi
               return self.bosListe
          else:
               return self.bosListe

     def mrkzNoktaYakalama(self,ev):
          if self.eBilgi["merkezn"]==True:
               tarananObjeler=self.tarananObjelerFiltreli(self.mrkzobjetipleri,ev)
               if len(tarananObjeler)!=0:
                    mrkznoktaListesi=[]
                    for i in tarananObjeler:
                         mrkznoktaListesi.append(["mrkz",i.eBilgi["merkez"]])
                    return mrkznoktaListesi
               return self.bosListe
          else:
               return self.bosListe

     def ortNoktaYakalama(self,ev):
          if self.eBilgi["ortan"]==True:
               tarananObjeler=self.tarananObjelerFiltreli(self.ortobjetipleri,ev)
               if len(tarananObjeler)!=0:
                    ortnoktaListesi=[]
                    for i in tarananObjeler:
                         liste=[]
                         for i in i.eBilgi["noktalar"]:liste.append(i)
                         i=0
                         while i<len(liste)-1:
                              czgort=Islemler.cizgiOrtaNokta(liste[i],liste[i+1])
                              ortnoktaListesi.append(["ortan",czgort])
                              i+=1
                    return ortnoktaListesi
               return self.bosListe
          else:
               return self.bosListe

     def kesisimNoktaYakalama(self,ev):
          if self.eBilgi["kesisimn"]==True:
               tarananObjeler=self.tarananObjelerFiltreli(self.kesisimobjetipleri,ev)
               if len(tarananObjeler)>1:
                    kesisimnoktaListesi=[]
                    liste=[]
                    i=0
                    while i<len(tarananObjeler)-1:
                         for a in tarananObjeler:
                              if tarananObjeler[i]==a:
                                   continue
                              p1=tarananObjeler[i].eBilgi["noktalar"][0]
                              p2=tarananObjeler[i].eBilgi["noktalar"][1]
                              p3=a.eBilgi["noktalar"][0]
                              p4=a.eBilgi["noktalar"][1]
                              kesisimnok=Islemler.ikiDogrununKesisimNoktasiBulma(p1,p2,p3,p4)
                              kesisimnoktaListesi.append(["kesisimn",kesisimnok])
                         i+=1
                    return kesisimnoktaListesi
               return self.bosListe
          else:
               return self.bosListe

          

     def ucNoktaSekilEkle(self):
          self.ucNS=ucNoktaSekil(QPointF(0,0))
          self.ucNS.setVisible(False)
          self.gs.addItem(self.ucNS)
     
     def ucNoktaSekilTasima(self,enyakinNokta):
          self.ucNS.nokta=enyakinNokta
          self.ucNS.setVisible(True)
          self.ortaNS.setVisible(False)
          self.kesisimNS.setVisible(False)
          self.mrkzNS.setVisible(False)
     
     def ucNoktaSekilKapat(self):
          self.ucNS.nokta=QPointF(0,0)
          self.ucNS.setVisible(False)
               

     def ortaNoktaSekilEkle(self):
          self.ortaNS=ortNoktaSekil(QPointF(0,0))
          self.ortaNS.setVisible(False)
          self.gs.addItem(self.ortaNS)

     def ortaNoktaTasima(self,enyakinnokta):
          self.ortaNS.setVisible(True)
          self.mrkzNS.setVisible(False)
          self.ucNS.setVisible(False)
          self.kesisimNS.setVisible(False)
          self.ortaNS.nokta=enyakinnokta
     
     def ortaNoktaSekilKapat(self):
          self.ortaNS.nokta=QPointF(0,0)
          self.ortaNS.setVisible(False)
                     

     def merkezNoktaSekilEkle(self):
          self.mrkzNS=mrkzNoktaSekil(QPointF(0,0))
          self.mrkzNS.setVisible(False)
          self.gs.addItem(self.mrkzNS)

     def merkezNoktaSekilHareket(self,enyakinnokta):
          self.mrkzNS.setVisible(True)
          self.ucNS.setVisible(False)
          self.ortaNS.setVisible(False)
          self.kesisimNS.setVisible(False)
          self.mrkzNS.nokta=enyakinnokta
     
     def merkezNoktaSekilKapat(self):
          self.mrkzNS.nokta=QPointF(0,0)
          self.mrkzNS.setVisible(False)

     def kesisimNoktaSekilEkle(self):
          self.kesisimNS=kesisimNoktaSekil(QPointF(0,0))
          self.kesisimNS.setVisible(False)
          self.gs.addItem(self.kesisimNS)

     def kesisimNoktaSekilHareket(self,enyakinnokta):
          self.kesisimNS.setVisible(True)
          self.mrkzNS.setVisible(False)
          self.ucNS.setVisible(False)
          self.ortaNS.setVisible(False)
          self.kesisimNS.nokta=enyakinnokta
     
     def kesisimNoktaSekilKapat(self):
          self.kesisimNS.nokta=QPointF(0,0)
          self.kesisimNS.setVisible(False)
               

class ucNoktaSekil(QGraphicsObject):
     def __init__(self,nokta,parent=None):
          QGraphicsObject.__init__(self,parent)
          self.nokta=nokta

     def paint(self, painter,option, widget):
          painter.setPen(Ayarlar.noktaYKalem)
          painter.drawPath(self.shape())

     def boundingRect(self):
          return self.shape().boundingRect()

     def shape(self):
          p=QPainterPath()
          if Ayarlar.nYakalamaYaricap<1:
               Ayarlar.nYakalamaYaricap=1
          p.moveTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          return p

class ortNoktaSekil(ucNoktaSekil):
     def __init__(self,nokta,parent=None):
          ucNoktaSekil.__init__(self,nokta,parent)
          self.nokta=nokta
     
     def shape(self):
          p=QPainterPath()
          if Ayarlar.nYakalamaYaricap<1:
               Ayarlar.nYakalamaYaricap=1
          p.moveTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          return p

class mrkzNoktaSekil(ucNoktaSekil):
     def __init__(self,nokta,parent=None):
          ucNoktaSekil.__init__(self,nokta,parent)
          self.nokta=nokta
     
     def shape(self):
          p=QPainterPath()
          if Ayarlar.nYakalamaYaricap<1:
               Ayarlar.nYakalamaYaricap=1
          p.moveTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(-Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          return p

class kesisimNoktaSekil(ucNoktaSekil):
     def __init__(self,nokta,parent=None):
          ucNoktaSekil.__init__(self,nokta,parent)
          self.nokta=nokta
     
     def shape(self):
          p=QPainterPath()
          if Ayarlar.nYakalamaYaricap<1:
               Ayarlar.nYakalamaYaricap=1
          p.moveTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta+QPointF(0,Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta+QPointF(Ayarlar.nYakalamaYaricap,-Ayarlar.nYakalamaYaricap))
          p.lineTo(self.nokta-QPointF(Ayarlar.nYakalamaYaricap,Ayarlar.nYakalamaYaricap))
          return p