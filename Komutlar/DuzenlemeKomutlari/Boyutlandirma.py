from Komutlar.DuzenlemeKomutlari.AnaKomut import AnaKomutDuzenleme
from PyQt5.QtCore import *
from Komutlar.Elemanlar import *
from Komutlar.Yardimcilar import Islemler

class Boyutlandirma(AnaKomutDuzenleme):
    def __init__(self,gv,gs,komutPanel):
        AnaKomutDuzenleme.__init__(self, gv, gs, komutPanel)
        self.gs=gs
        self.gv=gv
        self.komutPanel=komutPanel

    def komutBasla(self,x,y):
        if len(self.noktaListesi)==0:
            self.komutSatiriYazi("Tasima Noktasi Seciniz veya Koordinat Giriniz")
        elif len(self.noktaListesi)==1:
            oran=self.oranBul(x, y)
            self.elemanlariBoyutlandirma(oran)
            self.komutSatiriYazi("Nokta Seciniz veya Koordinat Giriniz veya Oran Giriniz")
            self.noktaListesi.clear()
        elif len(self.noktaListesi)==2:
            oran=self.oranBul(x, y)
            self.elemanlariBoyutlandirma(oran)
            self.noktaListesi.clear()
    
    def komutBaslaorn(self,oran):
        if len(self.noktaListesi)==0:
            self.komutSatiriYazi("Tasima Noktasi Seciniz veya Koordinat Giriniz")
        elif len(self.noktaListesi)==1:
            self.elemanlariBoyutlandirma(oran)
            self.noktaListesi.clear()

    def elemanlariBoyutlandirma(self,oran):
        for i in self.gs.secimObjesi.secilenElemanlar:i.boyutlandirma(self.noktaListesi[0],oran)
        self.gs.sahneGuncelleme()
        self.komutSatiriYazi("Elemanlar Boyutlandirildi.")
        self.komutBitti()

    def enUzakNoktaBul(self,nokta,noktaListesi):
        uzunlukL=[]
        for i in noktaListesi:
            uzunluk=Islemler.cizgiUzunlukBul(nokta,i)
            uzunlukL.append(uzunluk)
        indeks=uzunlukL.index(max(uzunlukL))
        enuzaknokta=noktaListesi[indeks]
        return enuzaknokta

    def oranBul(self,x,y):
        secimDikdorgeni=self.gs.secimObjesi.secilenElemanDikdorgenAlani()
        koordinat=secimDikdorgeni.getCoords()
        p1=QPointF(koordinat[0],koordinat[1])
        p2=QPointF(koordinat[2],koordinat[3])
        uzaknokta=self.enUzakNoktaBul(self.noktaListesi[0],[p1,p2])
        n1=uzaknokta
        n2=self.noktaListesi[0]+QPointF(x,y)
        u2=Islemler.cizgiUzunlukBul(self.noktaListesi[0], n1)
        u1=Islemler.cizgiUzunlukBul(self.noktaListesi[0], n2)
        oran=u1/u2
        return oran

    def yakalamaNoktasiAl(self,ev,ynokta):
        self.fareN=ev.scenePos()
        self.yakalamaNoktasi=ynokta
        if len(self.noktaListesi)==1:
            if len(self.aciYakalamaNoktasi)!=0:
                xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.aciYakalamaNoktasi[0])
            else:
                xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.fareN)
            oran=self.oranBul(xy[0],xy[1])
            self.elemanlarOnIzlemeBoyutlandirmaGuncelle(self.noktaListesi[0],oran)
        
        if len(self.noktaListesi)==1:
            self.aciYakalamaNoktasi=self.gs.ay.aciYakalama(self.noktaListesi[0],ev)
        
        self.tahta.sahneGuncelleme()

    
    def veriKoordinat(self,koordinat):
        if len(self.secimObjesi.secilenElemanlar)!=0 and self.secimOnay==False:
            self.komutSatiriYazi("Secimi Onaylayiniz")
        if self.secimOnay==True:
            if len(self.noktaListesi)==0:
                self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
                self.komutSatiriYazi("Yerlesme Noktasi Seciniz veya Oran Giriniz")
                self.elemanlarOnIzlemeBasla()

            # elif len(self.noktaListesi)!=0:
            #     self.noktaListesi.append(QPointF(koordinat[0],koordinat[1]))
            #     xy=Islemler.ikiNoktaXYFark(self.noktaListesi[0], self.noktaListesi[1])
            #     self.komutBasla(xy[0], xy[1])

    def veriUzunluk(self,oran):
        if len(self.noktaListesi)!=0:
            self.komutBaslaorn(oran)

    def noktaEkle(self,nokta):
        if len(self.noktaListesi)==0:
            if len(self.yakalamaNoktasi)!=0:
                self.noktaListesi.append(self.yakalamaNoktasi[1])
            else:
                self.noktaListesi.append(nokta)
            self.komutSatiriYazi("Yerlesme Noktasi Seciniz veya Oran Giriniz")
            self.elemanlarOnIzlemeBasla()
        else:
            if len(self.yakalamaNoktasi)!=0:
                self.noktaListesi.append(self.yakalamaNoktasi[1])
            elif len(self.aciYakalamaNoktasi)!=0:
                self.noktaListesi.append(self.aciYakalamaNoktasi[0])
            else:
                self.noktaListesi.append(nokta)