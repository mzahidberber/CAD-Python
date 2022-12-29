from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore,QtGui
from Komutlar.Elemanlar.SurekliCizgi import SurekliCizgi
from Komutlar.Yardimcilar import Katman
from Komutlar.Elemanlar import *
from Komutlar.Elemanlar import Yay,Elips,Cember,Cizgi


class Yazma:
     def __init__(self,gs):
          self.gs=gs

          self.elemanListesi=self.gs.cizilenElemanListesiBilgi()
          self.katmanListesi=self.gs.katman.katmanListesiBilgi()
          self.katmanObjesi=self.gs.katman

          self.kayitDosyasiVar=False
     
     def kayitDosyasiOlustur(self):
          ayarlar=QFileDialog.Options()
          self.konum=QFileDialog.getSaveFileName(None,"Kayit Yeri Sec","yenicizim","ÇizimProgramıDosyası (*.cpd)",options=ayarlar)
          print(self.konum[0])
          return self.konum

     def dosyaUzerineKaydet(self,komutYazi):
          if self.kayitDosyasiVar==True:
               with open(self.konum[0],"w",encoding="utf-8") as f:
                    self.katmanYazma(f)
                    self.elemanYazma(f)
                    print("Kaydedildi")
                    komutYazi.addItem(f"Dosya Kaydedildi: {self.konum[0]}")
                    komutYazi.scrollToBottom()

          else:
               self.dosyaBilgiYazma(komutYazi)
     
     def dosyaBilgiYazma(self,komutYazi):
          konum=self.kayitDosyasiOlustur()
          if konum[0]!="":
               with open(konum[0],"w",encoding="utf-8") as f:
                    self.katmanYazma(f)
                    self.elemanYazma(f)
                    print("Kaydedildi")
                    self.kayitDosyasiVar=True
                    komutYazi.addItem(f"Dosya Kaydedildi: {self.konum[0]}")
                    komutYazi.scrollToBottom()
                    

     def katmanYazma(self,f):
          f.write("Katmanlar:\n")
          for i in self.katmanListesi:
               f.write("katman*")
               f.write(f"{i.eBilgi['katmanAdi']}*")
               #f.write(f"{i.eBilgi['kilit']}\n")
               #f.write(f"{i.eBilgi['gorunum']}\n")
               f.write(f"{i.eBilgi['cTip']}*")
               f.write(f"{i.eBilgi['cRenk'].red()},{i.eBilgi['cRenk'].green()},{i.eBilgi['cRenk'].blue()}*")
               f.write(f"{i.eBilgi['cKalinlik']}*")
               #f.write(f"{i.eBilgi['kalem']}\n")
               #f.write(f"{i.eBilgi['elemanlar']}\n")
               f.write("\n")

     def elemanYazma(self,f):
          f.write("Elemanlar:\n")
          for i in self.elemanListesi:
               f.write("eleman*")
               f.write(f"{i.eBilgi['tip']}*")
               f.write(f"{self.noktalarYazma(i.eBilgi['noktalar'])}*")
               f.write(f"{self.merkezNoktaYazma(i)}*")
               f.write(f"{i.eBilgi['yaricap']}*")
               f.write(f"{i.eBilgi['bbAci']}*")
               f.write(f"{self.kareYazma(i)}*")
               f.write(f"{i.eBilgi['katman'].eBilgi['katmanAdi']}*")
               f.write(f"{i.eBilgi['kalem']}*")
               f.write("\n")

     def kareYazma(self,eleman):
          if eleman.eBilgi['kare']!=None:
               noktalar=eleman.eBilgi['kare'].getCoords()
               return noktalar
          else:
               return eleman.eBilgi['kare']

     def merkezNoktaYazma(self,eleman):
          if eleman.eBilgi['merkez']!=None:
               merkeznoktalar=[]
               merkeznoktalar.append(eleman.eBilgi['merkez'])
               merkez=self.noktalarYazma(merkeznoktalar)
               return merkez
          else:
               return eleman.eBilgi['merkez']

     def noktalarYazma(self,noktaListesi):
          noktaListesii=[]
          for i in noktaListesi:
               noktax=i.x()
               noktay=i.y()
               noktaListesii.append(noktax)
               noktaListesii.append(noktay)
          return noktaListesii
     
     def okuma(self,komutYazi):
          dialog=QFileDialog()
          dialog.setFileMode(QFileDialog.AnyFile)
          dialog.setFilter(QtCore.QDir.Files)
          
          
          if dialog.exec_():
               dosyaAdi=dialog.selectedFiles()
               if dosyaAdi[0].endswith(".cpd"):
                    self.konum=dosyaAdi
                    print(self.konum[0])
                    self.kayitDosyasiVar=True
                    self.dosyaOkuma(dosyaAdi)
                    komutYazi.addItem(f"Dosya Acildi: {self.konum[0]}")
                    komutYazi.scrollToBottom()
                    
     def dosyaOkuma(self,dosyaAdi):
          with open(dosyaAdi[0],"r",encoding="utf-8") as f:
               for i in f:
                    bilgi=i.split("*")
                    if bilgi[0]=='Katmanlar:\n' or bilgi[0]=='Elemanlar:\n' or bilgi[1]=="0":
                         continue
                    elif bilgi[0]=="katman":
                         self.katmanEkle(bilgi)
                    elif bilgi[0]=="eleman":
                         self.elemanEkle(bilgi)
                    else:
                         pass

     
     def katmanEkle(self,bilgi):
          rgb=bilgi[3].split(',')
          renk=QtGui.QColor(int(rgb[0]),int(rgb[1]),int(rgb[2]))
          katman=Katman.Katman(bilgi[1],renk, float(bilgi[4]), bilgi[2])
          self.katmanObjesi.katmanEkle(katman)

     def elemanEkle(self,bilgi):
          if bilgi[1]=="Cizgi":
               self.cizgiEkle(bilgi)
          elif bilgi[1]=="Cember":
               self.cemberEkle(bilgi)
          elif bilgi[1]=="Elips":
               self.elipsEkle(bilgi)
          elif bilgi[1]=="SCizgi":
               self.sCizgiEkle(bilgi)
          elif bilgi[1]=="Dikdortgen":
               self.dikdortgenEkle(bilgi)
          elif bilgi[1]=="Yay":
               self.yayEkle(bilgi)

     def dikdortgenEkle(self,bilgi):
          noktalar=bilgi[2][1:-1].split(",")
          noktalarListesi=[]
          i=0
          while i<len(noktalar):
               nokta=QtCore.QPointF(float(noktalar[i]),float(noktalar[i+1]))
               noktalarListesi.append(nokta)
               i+=2
          dikdorgen=SurekliCizgi.Dikdortgen(self.gs, noktalarListesi)
          for i in self.katmanListesi:
               if i.eBilgi["katmanAdi"]==bilgi[7]:
                    dikdorgen.katmanGuncelle(i)
          self.gs.elemanEkle(dikdorgen)

     def sCizgiEkle(self,bilgi):
          noktalar=bilgi[2][1:-1].split(",")
          noktalarListesi=[]
          i=0
          while i<len(noktalar):
               nokta=QtCore.QPointF(float(noktalar[i]),float(noktalar[i+1]))
               noktalarListesi.append(nokta)
               i+=2
          scizgi=SurekliCizgi.SurekliCizgi(self.gs, noktalarListesi)
          for i in self.katmanListesi:
               if i.eBilgi["katmanAdi"]==bilgi[7]:
                    scizgi.katmanGuncelle(i)
          self.gs.elemanEkle(scizgi)
     
     def yayEkle(self,bilgi):
          noktalar=bilgi[2][1:-1].split(",")
          p3=QtCore.QPointF(float(noktalar[4]),float(noktalar[5]))
          p2=QtCore.QPointF(float(noktalar[2]),float(noktalar[3]))
          p1=QtCore.QPointF(float(noktalar[0]),float(noktalar[1]))
          yay=Yay.UcNoktaYay(self.gs, p1, p2, p3)
          for i in self.katmanListesi:
               if i.eBilgi["katmanAdi"]==bilgi[7]:
                    yay.katmanGuncelle(i)
          self.gs.elemanEkle(yay)
     
     def elipsEkle(self,bilgi):
          noktalar=bilgi[3][1:-1].split(",")
          merkez=QtCore.QPointF(float(noktalar[0]),float(noktalar[1]))
          yaricapNoktalar=bilgi[4][1:-1].split(",")
          yaricap1=float(yaricapNoktalar[0])
          yaricap2=float(yaricapNoktalar[1])
          elips=Elips.Elips(self.gs, merkez, yaricap1, yaricap2)
          for i in self.katmanListesi:
               if i.eBilgi["katmanAdi"]==bilgi[7]:
                    elips.katmanGuncelle(i)
          self.gs.elemanEkle(elips)
     
     def cemberEkle(self,bilgi):
          noktalar=bilgi[3][1:-1].split(",")
          merkez=QtCore.QPointF(float(noktalar[0]),float(noktalar[1]))
          yaricap=float(bilgi[4])
          cember=Cember.Cember(self.gs, merkez, yaricap)
          for i in self.katmanListesi:
               if i.eBilgi["katmanAdi"]==bilgi[7]:
                    cember.katmanGuncelle(i)
          self.gs.elemanEkle(cember)

     def cizgiEkle(self,bilgi):
          noktalar=bilgi[2][1:-1].split(",")
          p2=QtCore.QPointF(float(noktalar[2]),float(noktalar[3]))
          p1=QtCore.QPointF(float(noktalar[0]),float(noktalar[1]))
          cizgi=Cizgi.Cizgi(self.gs,p1,p2)
          for i in self.katmanListesi:
               if i.eBilgi["katmanAdi"]==bilgi[7]:
                    cizgi.katmanGuncelle(i)
          self.gs.elemanEkle(cizgi)