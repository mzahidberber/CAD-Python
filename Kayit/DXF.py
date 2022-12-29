import ezdxf,sys
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
from Komutlar.Elemanlar import *
from Komutlar.Elemanlar import Cizgi,Cember

class DXFOkuma:
    def __init__(self,gs):
            self.gs=gs

            self.elemanListesi=self.gs.cizilenElemanListesiBilgi()
            self.katmanListesi=self.gs.katman.katmanListesiBilgi()
            self.katmanObjesi=self.gs.katman

            self.kayitDosyasiVar=False

    def okuma(self,komutYazi):
        dialog=QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QtCore.QDir.Files)
          
        if dialog.exec_():
            dosyaAdi=dialog.selectedFiles()
            if dosyaAdi[0].endswith(".dxf"):
                self.konum=dosyaAdi
                self.kayitDosyasiVar=True
                self.dosyaOkuma(self.konum[0])
                komutYazi.addItem(f"Dosya Acildi: {self.konum[0]}")
                komutYazi.scrollToBottom()

    def dosyaOkuma(self,konum):
        try:
            doc = ezdxf.readfile(konum)
            msp = doc.modelspace()
            for e in msp:
                print(e.dxftype())
            for e in msp.query('LINE'):
                p1=QtCore.QPointF(e.dxf.start[0],e.dxf.start[1])
                p2=QtCore.QPointF(e.dxf.end[0],e.dxf.end[1])
                cizgi=Cizgi.Cizgi(self.gs, p1, p2)
                #cizgi.katmanGuncelle(e.dxf.layer)
                self.gs.elemanEkle(cizgi)
            for e in msp.query('CIRCLE'):
                merkez=QtCore.QPointF(e.dxf.center[0],e.dxf.center[1])
                cember=Cember.Cember(self.gs, merkez, e.dxf.radius)
                #cember.katmanGuncelle(e.dxf.layer)
                self.gs.elemanEkle(cember)
            for e in msp.query('LWPOLYLINE'):
                nktListesi=[]
                # for i in e.dxf.vertices:
                #     nokta=QtCore.QPointF(i[0],i[1])
                #     nktListesi.append(nokta)
                a=e.dxf.elevation
                print(a)
                #scizgi=SurekliCizgi.SurekliCizgi(self.gs, nktListesi)
                #cember.katmanGuncelle(e.dxf.layer)
                #self.gs.elemanEkle(scizgi)
        
        except IOError:
            print(f'Not a DXF file or a generic I/O error.')
            sys.exit(1)
        except ezdxf.DXFStructureError:
            print(f'Invalid or corrupted DXF file.')
            sys.exit(2)

doc = ezdxf.new('R2010')  # create a new DXF R2010 drawing, official DXF version name: 'AC1024'

msp = doc.modelspace()  # add new entities to the modelspace
msp.add_line((0, 10), (10, 10),dxfattribs={"layer":"deneme"})  # add a LINE entity
msp.add_line((10, 10,10), (10, 10))  # add a LINE entity
msp.add_circle((0,0), 10)
msp.add_polyline2d([(0,0),(10,10),(30,50)])
doc.saveas('line.dxf')

