from Komutlar.Yardimcilar.KalemOlusturucu import Kalem,Tarama
from PyQt5 import QtGui

class Katman:
     def __init__(self,katmanAdi:str,renk:QtGui.QColor,kalinlik:float,tip:str):
          self.katmanAdi=katmanAdi
          self.renk=renk
          self.kalinlik=kalinlik
          self.tip=tip

          self.katmanKalemi=Kalem(kalinlik,renk,tip)

          self.elemanListesi=[]

          self.eBilgi={
               "katmanAdi":self.katmanAdi,
               "kilit":True,
               "gorunum":True,
               "cTip":self.tip,
               "cRenk":self.renk,
               "cKalinlik":self.kalinlik,
               "kalem":self.katmanKalemi,
               "elemanlar":self.elemanListesi
          }

     def katmanKopyala(self):
          yeniKatman=Katman(self.eBilgi["katmanAdi"],self.eBilgi["cRenk"],self.eBilgi["cKalinlik"],self.eBilgi["cTip"])
          return yeniKatman

     def katmanKalemiBilgi(self):
          return self.eBilgi["kalem"]

     def elemanListesiBilgi(self):
          return self.eBilgi["elemanlar"]

     def katmanAdiDegistir(self,yeniad):
          self.eBilgi["katmanAdi"]=yeniad

     def renkDegistir(self,renk:QtGui.QColor):
          self.eBilgi["cRenk"]=renk
          self.kalemGuncelle()
     
     def kalinlikDegistir(self,kalinlik:float):
          self.eBilgi["cKalinlik"]=kalinlik
          self.kalemGuncelle()
     
     def tipDegistir(self,tip:str):
          self.eBilgi["cTip"]=tip
          self.kalemGuncelle()

     def kalemGuncelle(self):
          kalem=Kalem(self.eBilgi["cKalinlik"],self.eBilgi["cRenk"],self.eBilgi["cTip"])
          self.eBilgi["kalem"]=kalem

     def kalemDegistir(self,kalem):
          self.eBilgi["kalem"]=kalem

     def elemanlarGuncelle(self):
          self.eBilgi["elemanlar"]=self.elemanListesi

     def elemanEkle(self,eleman):
          self.elemanListesi.append(eleman)
          self.elemanlarGuncelle()

     def elemanlarEkle(self,elemanlar):
          for i in elemanlar:self.elemanListesi.append(i)
          self.elemanlarGuncelle()

     def elemanCikar(self,eleman):
          self.elemanListesi.remove(eleman)
          self.elemanlarGuncelle()

     def elemanlarCikar(self,elemanlar):
          for i in elemanlar:self.elemanListesi.remove(i)
          self.elemanlarGuncelle()

     def elemanlarKitle(self):
          for i in self.elemanListesi:i.elemanSecimKapali()
          self.eBilgi["kilit"]=False

     def elemanlarKilitAc(self):
          for i in self.elemanListesi:i.elemanSecimAcik()
          self.eBilgi["kilit"]=True

     def elemanlariGizle(self):
          for i in self.elemanListesi:i.elemanGizle()
          self.eBilgi["gorunum"]=False

     def elemanlariGoster(self):
          for i in self.elemanListesi:i.elemanGoster()
          self.eBilgi["gorunum"]=True

class KatmanDuzenle:
     def __init__(self,pencere,gs):
          self.pencere=pencere
          self.gs=gs
          
          self.katmanListesi=[]
          varsayilankatman=Katman("0",QtGui.QColor(255,255,255),1,"duz")
          self.katmanListesi.append(varsayilankatman)

          self.seciliKatman=self.katmanListesi[0]

     def katmanListesiBilgi(self):
          return self.katmanListesi

     def seciliKatmanBilgi(self):
          return self.seciliKatman
     
     def seciliKatmanDegistir(self,katmanIsmi):
          for i in self.katmanListesi:
               if i.eBilgi["katmanAdi"]==katmanIsmi:
                    self.seciliKatman=i
                    print(f"Secilen Katman:{self.seciliKatman.eBilgi['katmanAdi']}")
                    break

     def katmanEkle(self,yenikatman:Katman):
          for i in self.katmanListesi:
               if yenikatman.eBilgi["katmanAdi"]==i.eBilgi["katmanAdi"]:
                    if len(yenikatman.eBilgi["katmanAdi"])>=4 and yenikatman.eBilgi["katmanAdi"][-3]=='(' and yenikatman.eBilgi["katmanAdi"][-1]==')':
                         sayi=int(yenikatman.eBilgi["katmanAdi"][-2])+1
                         liste=list(yenikatman.eBilgi["katmanAdi"])
                         liste[-2]=str(sayi)
                         yeniad="".join(liste)
                         yenikatman.eBilgi["katmanAdi"]=yeniad
                    else:
                         yenikatman.eBilgi["katmanAdi"]=yenikatman.eBilgi["katmanAdi"]+"(1)"
                         
          self.katmanListesi.append(yenikatman)

     def katmanSil(self,katman:Katman):
          self.katmanListesi.remove(katman)

     def tumKatmanlariSil(self):
          for i in self.katmanListesi:
               if i.eBilgi["katmanAdi"]=="0":
                    i.elemanlarGuncelle()
                    continue
               else:
                    self.katmanSil(i)

     def katmanDegiştir(self,eskikatman:Katman,yenikatman:Katman):
          pass

     def katmanGizle(self,katman:Katman):
          katman.elemanlariGizle()

     def katmanGoster(self,katman:Katman):
          katman.elemanlariGoster()

     def secilenKatmaninOzellikleri(self,katman:Katman):
          return katman.eBilgi