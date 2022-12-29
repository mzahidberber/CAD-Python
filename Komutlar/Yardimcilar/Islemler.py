import numpy as np
import math
from PyQt5.QtCore import QPointF 

def cizgiUzunlukBul(n1,n2):
     "İki nokta arasi cizgi uzunlugunu bulmak icin fonksiyon"
     x1,y1,x2,y2=n1.x(),n1.y(),n2.x(),n2.y()
     toplam=((x2-x1)**2)+((y2-y1)**2)
     uzunluk=math.sqrt(toplam)
     return uzunluk

def merkezveYaricapBul(p1,p2,p3):
     "üc noktası biline cemberin merkez ve yaricapını bulma fonksiyonu noktalar x,y,z olmalı z=1 olmalı"
     x1,y1,z1=p1.x(),p1.y(),1
     x2,y2,z2=p2.x(),p2.y(),1
     x3,y3,z3=p3.x(),p3.y(),1
     a1=-(x1**2)-(y1**2)
     a2=-(x2**2)-(y2**2)
     a3=-(x3**2)-(y3**2)
     matris=np.array([
          [x1,y1,z1],
          [x2,y2,z2],
          [x3,y3,z3]
     ])
     matris1=np.array([
          [a1,y1,z1],
          [a2,y2,z2],
          [a3,y3,z3]
     ])
     matris2=np.array([
          [x1,a1,z1],
          [x2,a2,z2],
          [x3,a3,z3]
     ])
     matris3=np.array([
          [x1,y1,a1],
          [x2,y2,a2],
          [x3,y3,a3]
     ])
     det=np.linalg.det(matris)
     det1=np.linalg.det(matris1)
     det2=np.linalg.det(matris2)
     det3=np.linalg.det(matris3)
     
     D=det1/det
     E=det2/det
     F=det3/det
     Merkez=(-D/2,-E/2)
     Yaricap=(math.sqrt((D**2)+(E**2)-(4*F)))*0.5
     return Merkez,Yaricap

def dogruEgimBulma(p1,p2):
     "Dogrunun egimini bulmak icin fonksyion"
     x1,y1,x2,y2=p1.x(),p1.y(),p2.x(),p2.y()
     try:
          egim=(y2-y1)/(x2-x1)
     except Exception as ex:
          print("egim 0/a veya a/0 oldugundan sonsuz deger donduruldu")
          return math.inf
     else:
          return egim

def dogruAciBulma(egim):
     "egimi bilinen dogrunun acısını bulmak icin fonksiyon"
     aci=math.atan(egim)
     derece = radyaniDereceyeCevirme(aci)
     return derece

def dogruAciBul(p1,p2):
     "iki noktası bilinen dogrunun acısını bulmak icin fonksiyon"
     egim=dogruEgimBulma(p1,p2)
     aci=dogruAciBulma(egim)
     return aci

def acidanEgimBulma(aci):
     "Acidan Egim bulma"
     egim=math.tan(aci)
     return egim

def radyaniDereceyeCevirme(radyan):
     derece = radyan * (180 / math.pi)
     return derece

def dereceyiRadyanaCevirme(derece):
     radyan = derece * (math.pi / 180)
     return radyan

def cizgiOrtaNokta(n1,n2):
     "iki nokta arası orta noktayi bulmak icin fonksiyon"
     x=(n1.x()+n2.x())/2
     y=(n1.y()+n2.y())/2
     ortaNokta=QPointF(x,y)
     return ortaNokta

def pointMatrisDonustur(point):
     "QPointF veya QPoint matris listeye cevirme [x,y,z] z=1"
     matris=[point.x(),point.y(),1]
     return matris

def ikiDogruArasiAciBulma(egim1,egim2):
     "Kesişen İki Dogru Arasi Aci Bulma Formülü"
     tanjant=(egim1-egim2)/(1+(egim1*egim2))
     aci=dogruAciBulma(tanjant)
     return aci

def IkiNoktaninIcCarpimi(p1,p2):
     "İki Noktanın İc Carpim Bulmak icin Fonksiyon"
     return p1.x()*p2.y()-p1.y()*p2.x()

def IkıNoktaninFarki(p1,p2):
     "İki Noktanın Farkını Bulmak icin Fonksiyon"
     nokta=QPointF(p1.x()-p2.x(),p1.y()-p2.y())
     return nokta
     
def NoktaDogrununNeresindeBul(p1,p2,p3):
     "P3,P1 ve P2 noktalarından olusan dogrunun neresinde sag-sol-üzerindemi"
     k=IkıNoktaninFarki(p3,p1)
     l=IkıNoktaninFarki(p2,p1)
     kontrol=IkiNoktaninIcCarpimi(k,l)
     if kontrol>0:
          return "sag"
     elif kontrol<0:
          return "sol"
     else:
          return "üzerinde"

def ikiDogrununKesisimNoktasiBulma(p1,p2,p3,p4):
     a=((p4.y()-p3.y())*(p3.x()-p1.x()))-((p3.y()-p1.y())*(p4.x()-p3.x()))
     b=((p4.y()-p3.y())*(p2.x()-p1.x()))-((p2.y()-p1.y())*(p4.x()-p3.x()))
     T=a/b
     p5x=p1.x()+(p2.x()-p1.x())*T
     p5y=p1.y()+(p2.y()-p1.y())*T
     nokta=QPointF(p5x,p5y)
     return nokta

def ikinciDerecedenDenklemCozumu(a,b,c):
     d=(b**2)-(4*a*c)
     if d<0:
          print("kök yok")
     if d==0:
          print("kökler cakısık")
          x=-b/(2*a)
          return x,x
     if d>0:
          x=(-b-math.sqrt(d))/(2*a)
          y=(-b+math.sqrt(d))/(2*a)
          return x,y

def ikiParalelDogru(p1,p2,mesafe):
     egim=dogruEgimBulma(p1,p2)
     a=egim
     b=-1
     x1,y1,x3,y3=p1.x(),p1.y(),float,float
     c1=-y1-(egim*x1)
     deger=mesafe*(math.sqrt(a**2+b**2))
     c2=deger+c1

     #c2=-y3-(egim*x3)
     p3=QPointF(x3,y3)
     return p3

def uzunlukNoktalariniBul(nokta,uzunluk,egim):
     "Baslagic Noktasina Aynı Dogru Uzerindeki Eşit Uzunluktaki iki Noktayi Bulur"

     noktaA=QPointF()
     noktaB=QPointF()

     if egim==0:
          noktaA.setX(nokta.x()+uzunluk)
          noktaA.setY(nokta.y())

          noktaB.setX(nokta.x()-uzunluk)
          noktaB.setY(nokta.y())

     elif math.isinf(egim):
          noktaA.setX(nokta.x())
          noktaA.setY(nokta.y()+uzunluk)

          noktaB.setX(nokta.x())
          noktaB.setY(nokta.y()-uzunluk)

     else:
          dx=uzunluk/math.sqrt(1+(egim*egim))
          dy=egim*dx

          noktaA.setX(nokta.x()+dx)
          noktaA.setY(nokta.y()+dy)

          noktaB.setX(nokta.x()-dx)
          noktaB.setY(nokta.y()-dy)
     return noktaA,noktaB

def uzunluktakiNoktayiBul(bnokta,uzunluk,fareKonumu):
     "Mousenin Konumuna Gore Belli Uzunluktali Mesafedeki Noktayi Bulur"

     egim=dogruEgimBulma(bnokta, fareKonumu)

     a=uzunlukNoktalariniBul(bnokta, uzunluk,egim)
     b=uzunlukNoktalariniBul(bnokta, uzunluk,-egim)

     noktalar=NoktaDogrununNeresindeBul(bnokta, b[1], a[0])
     fareKonumuNoktasi=NoktaDogrununNeresindeBul(bnokta, b[1], fareKonumu)
     
     if noktalar=="üzerinde":
          xfark=fareKonumu.x()-bnokta.x()
          yfark=fareKonumu.y()-bnokta.y()
          if xfark<0 or yfark<0:
               return a[1]
          else:
               return a[0]
     elif noktalar==fareKonumuNoktasi:
          return a[0]
     else:
          return a[1]

def ikiNoktaXYFark(p1,p2):
     "P2 ve P1 x ve y leri arasindaki farki hesaplar x,y dondurur"
     x=p2.x()-p1.x()
     y=p2.y()-p1.y()
     return x,y

def noktaHangiBolgedeBul(origin,p1):
     "Origin noktasi koordinat sistemin 0,0 kabul edilerek p1 noktasının hangi bölgede oldugnu bulur"
     originx,originy=origin.x(),origin.y()
     p1x,p1y=p1.x(),p1.y()
     if p1x>originx and p1y>originy:
          return 1
     elif p1x<originx and p1y>originy:
          return 2
     elif p1x<originx and p1y<originy:
          return 3
     elif p1x>originx and p1y<originy:
          return 4
     else:
          #üzerinde
          return 5