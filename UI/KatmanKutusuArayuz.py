from UI.KatmanKutusuUI import Ui_KatmanDuzenleme
from UI.ElemanSilKutusuArayuz import ElemanSilKutusu
from PyQt5.QtWidgets import *
from PyQt5 import QtGui,QtCore,Qt
from Komutlar.Yardimcilar.KalemOlusturucu import KALEMTIPLERI

class KatmanKutusuArayuz(QDialog):
     def __init__(self,katmanObjesi):
          super(KatmanKutusuArayuz,self).__init__()
          self.ui=Ui_KatmanDuzenleme()
          self.ui.setupUi(self)
          self.katmanObjesi=katmanObjesi

          self.ui.katmanListesi.setColumnWidth(0,100)
          self.ui.katmanListesi.setColumnWidth(1,15)
          self.ui.katmanListesi.setColumnWidth(2,60)
          self.ui.katmanListesi.setColumnWidth(3,60)
          self.ui.katmanListesi.setColumnWidth(4,15)
          self.ui.katmanListesi.setColumnWidth(5,100)
          self.ui.katmanListesi.setColumnWidth(6,80)
          
          self.ui.katmanListesi.itemPressed.connect(self.secilenKatmanlar)
          self.ui.katmanListesi.doubleClicked.connect(self.ciftTik)
          self.ui.KatmanEkle.clicked.connect(self.katmanEkle)
          self.ui.katmanSil.clicked.connect(self.katmanSil)

          self.secilenler=[]
     
     def ciftTik(self,ev):
          row=ev.row()
          lineEdit=self.ui.katmanListesi.cellWidget(row,0)
          isim=lineEdit.text()
          self.katmanObjesi.seciliKatmanDegistir(isim)
          secilikatman=self.katmanObjesi.seciliKatmanBilgi()
     
     def katmanSil(self,ev):
          if len(self.secilenler)>0 and self.secilenler!=None:
               secilenKatmanlar=[]
               rowListesi=[]
               for i in self.secilenler:
                    row=i.row()
                    katman=self.hangiKatmanBul(row)
                    if katman.eBilgi["katmanAdi"]=="0":
                         continue
                    rowListesi.append(row)
                    secilenKatmanlar.append(katman)
               
               secilenKatmnElemanlar=[]
               for i in secilenKatmanlar:secilenKatmnElemanlar.extend(i.eBilgi["elemanlar"])
               if len(secilenKatmnElemanlar)>0:
                    self.katmanSilKutusuBaslat(secilenKatmanlar)
                    if secilenKatmanlar[0] in self.katmanListesi:
                         pass
                    else:
                         for i in rowListesi:self.satirSil(i)
               else:
                    for i in secilenKatmanlar:self.katmanObjesi.katmanSil(i)
                    for i in rowListesi:self.satirSil(i)

          self.secilenler.clear()
     
     def katmanSilKutusuBaslat(self,silinenKatmanlar):
          self.katmanSilKutusu=ElemanSilKutusu(self.katmanObjesi,silinenKatmanlar)
          self.katmanSilKutusu.show()
          self.katmanSilKutusu.exec_()
     
     def hangiKatmanBul(self,row):
          lineEdit=self.ui.katmanListesi.cellWidget(row,0)
          isim=lineEdit.text()
          for i in self.katmanListesi:
               if isim==i.eBilgi["katmanAdi"]:
                    return i

     def katmanEkle(self,ev):
          self.seciliKatman=self.katmanObjesi.seciliKatmanBilgi()
          yenikatman=self.seciliKatman.katmanKopyala()
          self.katmanObjesi.katmanEkle(yenikatman)
          satir=self.ui.katmanListesi.rowCount()
          self.ui.katmanListesi.insertRow(satir)
          self.satirWidgetleriEkle(satir,yenikatman)

     def secilenKatmanlar(self,ev):
          self.secilenler=self.ui.katmanListesi.selectedItems()

     def satirEkle(self):
          satirBilgi=self.ui.katmanListesi.rowCount()
          self.ui.katmanListesi.insertRow(satirBilgi)

     def satirSil(self,satir):
          self.ui.katmanListesi.removeRow(satir)

     def satirWidgetleriEkle(self,satir,katman):
          self.ui.katmanListesi.setCellWidget(satir,0,AdEditText(katman,self.katmanObjesi))
          self.ui.katmanListesi.setCellWidget(satir,1,Kilit(katman))
          self.ui.katmanListesi.setCellWidget(satir,2,GorunumButon(katman))
          self.ui.katmanListesi.setCellWidget(satir,3,KalinlikEditText(katman))
          self.ui.katmanListesi.setCellWidget(satir,4,RenkButonu(katman))
          self.ui.katmanListesi.setCellWidget(satir,5,TipSecim(katman))
          self.ui.katmanListesi.setItem(satir,6,QTableWidgetItem(str(len(katman.eBilgi["elemanlar"]))))

     
     def katmanlariGuncelle(self):
          self.katmanListesi=self.katmanObjesi.katmanListesiBilgi()
          satir=0
          for i in self.katmanListesi:
               self.satirEkle()
               self.satirWidgetleriEkle(satir,i)
               satir+=1

class AdEditText(QLineEdit):
     def __init__(self,katman,katmanObjesi):
          QLineEdit.__init__(self)
          self.katman=katman
          self.katmanObjesi=katmanObjesi

          self.setText(str(self.katman.eBilgi["katmanAdi"]))

          self.textChanged.connect(self.AdDegisim)
          self.editingFinished.connect(self.degisimBitti)
     def degisimBitti(self):
          deger=self.styleSheet()
          if deger=="background-color: rgb(211,0,0);":
               self.setText(str(self.katman.eBilgi["katmanAdi"]))
               self.setStyleSheet(f"background-color: rgb(255,255,255);")
     
     def AdDegisim(self,ev):
          self.katmanListesi=self.katmanObjesi.katmanListesiBilgi()
          adListesi=[]
          for i in self.katmanListesi:adListesi.append(i.eBilgi["katmanAdi"])
          oncekiisim=self.katman.eBilgi["katmanAdi"]
          if ev in adListesi:
               self.setStyleSheet(f"background-color: rgb(211,0,0);")
          else:
               self.setStyleSheet(f"background-color: rgb(255,255,255);")
               self.katman.katmanAdiDegistir(ev)

class KalinlikEditText(QLineEdit):
     def __init__(self,katman):
          QLineEdit.__init__(self)
          self.katman=katman

          self.setText(str(self.katman.eBilgi["cKalinlik"]))
          self.textChanged.connect(self.kalinlikDegisim)
          self.editingFinished.connect(self.degisimBitti)
     
     def degisimBitti(self):
          deger=self.styleSheet()
          if deger=="background-color: rgb(211,0,0);":
               self.setText(str(self.katman.eBilgi["cKalinlik"]))
               self.setStyleSheet(f"background-color: rgb(255,255,255);")

     def kalinlikDegisim(self,ev):
          try:
               if float(ev)<=20 and float(ev)>0:
                    self.katman.kalinlikDegistir(float(ev))
               else:
                    self.setText(str(self.katman.eBilgi["cKalinlik"]))
          except Exception as ex:
               print("Yanlış Bilgi Girdiniz!!",ex)
               self.setStyleSheet(f"background-color: rgb(211,0,0);")
          else:
               self.setStyleSheet(f"background-color: rgb(255,255,255);")
          finally:
               print(self.katman.eBilgi["cKalinlik"])

class RenkButonu(QPushButton):
     def __init__(self,katman):
          QPushButton.__init__(self)
          self.katman=katman

          # self.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Fixed)
          # self.setMaximumSize(20,20)
          self.secilenRenk=katman.eBilgi["cRenk"]
          self.setStyleSheet(f"background-color: {self.secilenRenk.name()};")
          self.clicked.connect(self.tiklama)

     def tiklama(self,ev):
          secilenRenk=QColorDialog.getColor()
          if secilenRenk.isValid():
               self.setStyleSheet(f"background-color: {secilenRenk.name()};")
               self.katman.renkDegistir(secilenRenk)

class TipSecim(QComboBox):
     def __init__(self,katman):
          QComboBox.__init__(self)
          self.katman=katman

          for i in KALEMTIPLERI:
               self.addItem(i)
               if i==self.katman.eBilgi["cTip"]:
                    self.setCurrentText(i)

          self.currentTextChanged.connect(self.tipDegisim)
     
     def tipDegisim(self,ev):
          self.katman.tipDegistir(ev)

class GorunumButon(QPushButton):
     def __init__(self,katman):
          QPushButton.__init__(self)
          self.katman=katman

          self.setText("")
          icon = QtGui.QIcon()
          icon.addPixmap(QtGui.QPixmap(":/Sembol/Semboller/gorunumacik.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
          icon.addPixmap(QtGui.QPixmap(":/Sembol/Semboller/gorunumkapali.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
          self.setIcon(icon)
          self.setIconSize(QtCore.QSize(16,16))
          self.setObjectName("gorunumButon")

          self.setCheckable(True)

          if self.katman.eBilgi["gorunum"]==False:
               self.setChecked(True)

          self.clicked.connect(self.tiklama)

     def tiklama(self,ev):
          if ev==True:
               self.katman.elemanlariGizle()
          else:
               self.katman.elemanlariGoster()

class Kilit(QPushButton):
     def __init__(self,katman):
          QPushButton.__init__(self)
          self.katman=katman

          self.setText("")
          icon = QtGui.QIcon()
          icon.addPixmap(QtGui.QPixmap(":/Sembol/Semboller/kilitacik.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
          icon.addPixmap(QtGui.QPixmap(":/Sembol/Semboller/kilitkapali.png"), QtGui.QIcon.Normal, QtGui.QIcon.On)
          self.setIcon(icon)
          self.setIconSize(QtCore.QSize(16,16))
          self.setObjectName("kilitButon")

          self.setCheckable(True)
          if self.katman.eBilgi["kilit"]==False:
               self.setChecked(True)

          self.clicked.connect(self.tiklama)

     def tiklama(self,ev):
          if ev==True:
               self.katman.elemanlarKitle()
          else:
               self.katman.elemanlarKilitAc()
     
     