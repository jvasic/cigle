# Cigle --- Jovan Vasić 2020

import random
import pygame as pg
import pygamebg
import math
import pprint

(sirina, visina) = (800, 600)
prozor = pygamebg.open_window(sirina, visina, 'Cigle')
pg.mouse.set_visible(False)

pg.key.set_repeat(10,10)

def tekst_ispis(x, y, tekst, velicina):
    font = pg.font.SysFont('Bahnschrift', velicina)
    tekst = font.render(tekst, True, pg.Color('white'))
    prozor.blit(tekst, (x, y))

def tekst_centar(x, y, tekst, velicina):
    font = pg.font.SysFont('Bahnschrift', velicina)
    tekst = font.render(tekst, True, pg.Color('white'))
    (sirina_teksta, visina_teksta) = (tekst.get_width(), tekst.get_height())
    (x, y) = (x - sirina_teksta / 2, y - visina_teksta / 2)
    prozor.blit(tekst, (x, y))

promena_brzine = 1
v = 7 - promena_brzine
minus_lista = [-1,1]

def nasumicno_odbijanje():
    global v, vx, vy
    vx = random.uniform(-v*0.8, v*0.8)
    vy = -math.sqrt(v*v - vx*vx)

nasumicno_odbijanje()

promena_sirine = -6
debljina_plocice = 5                                   
sirina_plocice = 100 - promena_sirine
x_plocice = sirina // 2
y_plocice = visina - 100

r = 8
(x_loptice, y_loptice) = (x_plocice, y_plocice - r)

novi_nivo = False
lepak = True
klik = False
kraj_igre = False

nivo = 0

debljina_cigle = 28
sirina_cigle = 46
od_plafona = 120
broj_kolona = 15
broj_redova = nivo + 2
razmak = 3
od_zida = (sirina - broj_kolona*sirina_cigle - (broj_kolona - 1)*razmak) // 2

poeni = 0
preostalo = 2

def nasumicna_boja():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generisi_boje():
    global boje
    boje = []
    for i in range(broj_redova):
        boje.append(nasumicna_boja())

def krugSeceVertikalnuDuz(cx, cy, r, x, y1, y2):
    if abs(x - cx)<=r and cy>y1 and cy<y2:
        return True
    else:
        return False

def krugSeceHorizontalnuDuz(cx, cy, r, x1, x2, y):
    return krugSeceVertikalnuDuz(cy, cx, r, y, x1, x2)

cigle = []
razbijene = []

def crtaj():
    global x_plocice, x_loptice, novi_nivo, y_loptice, kraj_igre
    prozor.fill(pg.Color('black'))

    if kraj_igre:
        if nivo == 9:
            tekst_centar(sirina/2, visina/2, 'GAME WON!!! '+str(poeni)+' points', 70)
        else:
            tekst_centar(sirina/2, visina/2, 'GAME OVER: '+str(poeni)+' points', 70)
        tekst_centar(sirina/2, visina/2 + 80, 'press SPACE to play again', 50)
        
    else:
        if lepak:
            tekst_centar(sirina/2, visina/2, 'LEVEL '+str(nivo), 70)
        if x_plocice + sirina_plocice/2 < sirina_plocice:    #izlazak plocice iz ekrana
            x_plocice = sirina_plocice/2
        if x_plocice - sirina_plocice/2 > sirina - sirina_plocice:
            x_plocice = sirina - sirina_plocice/2
        pg.draw.line(prozor, pg.Color('white'),
                     (x_plocice - sirina_plocice // 2, y_plocice),            #
                     (x_plocice + sirina_plocice // 2, y_plocice), debljina_plocice)
        if lepak:
            x_loptice = x_plocice
            y_loptice = y_plocice - r
        pg.draw.circle(prozor, pg.Color('white'), (round(x_loptice), round(y_loptice)), r)
        
        for i in range(broj_redova):
            boja_reda = boje[i]
            for j in range(broj_kolona):
                if not (i,j) in razbijene:
                    pg.draw.rect(prozor, boja_reda,
                                 (j*(sirina_cigle + razmak) + od_zida, od_plafona + (i - 1)*(debljina_cigle + razmak),
                                  sirina_cigle, debljina_cigle), 2)
            
        tekst_ispis(14, 7, str(poeni), 50)
        if preostalo>0:
            for i in (1,preostalo):
                pg.draw.circle(prozor, pg.Color('white'), (sirina - i*(r+28)-7, r+15), 2*r)
                
        if preostalo<0:
            kraj_igre = True
        if nivo == 9:
            kraj_igre = True
            
def obradi_dogadjaj(dogadjaj):
    global x_plocice, x_loptice, y_loptice, vx, vy, klik, kraj_igre
    if not kraj_igre:
        if dogadjaj.type == pg.MOUSEMOTION:
            (x_misa, y_misa) = dogadjaj.pos
            x_plocice = x_misa
            
        if lepak:
            if dogadjaj.type == pg.MOUSEBUTTONDOWN:
                klik = True

            
def novi_frejm():
    global x_loptice, y_loptice, lepak, vx, vy, v, sirina, visina, preostalo, r, razmak, sirina_cigle, x_plocice, sirina_plocice
    global broj_redova, broj_kolona, od_zida, od_plafona, debljina_cigle, cigle, razbijene, novi_nivo, poeni, klik, nivo
    global promena_sirine, promena_brzine
    if preostalo < 0 or nivo == 9:
        kraj_igre = True

    if len(razbijene) == len(cigle):
        novi_nivo = True
    
    if novi_nivo:                   #NOVI NIVO
        nivo += 1
        broj_redova += 1
        generisi_boje()
        razbijene = []
        cigle = []
        sirina_plocice += promena_sirine
        v += promena_brzine
        
        for i in range(broj_redova):
            for j in range(broj_kolona):
                cigle.append((j*(sirina_cigle + razmak) + od_zida, od_plafona + (i - 1)*(debljina_cigle + razmak)))
        lepak = True
        novi_nivo = False

    if x_loptice - r < 0:           #odbijanje od zidova
        vx = -vx
    if x_loptice + r > sirina:
        vx = -vx
    if y_loptice - r < 0:
        vy = -vy

    if y_loptice + r == y_plocice and x_loptice > x_plocice-sirina_plocice//2 and x_loptice < x_plocice+sirina_plocice//2:
        if lepak and klik:
            nasumicno_odbijanje()
            lepak = False
            klik = False
        else:
            vx = (x_loptice - x_plocice)/sirina_plocice*2*0.95*v
            vy = -math.sqrt(v**2 - vx*vx)

    #odbijanje od coska plocice        
    #if (x_plocice - sirina_plocice/2 - x_loptice)**2 + (y_plocice - y_loptice)**2 == r**2 or\
     #  (x_plocice + sirina_plocice/2 - x_loptice)**2 + (y_plocice - y_loptice)**2 == r**2:
     #   vx = -vx
     #   vy = -vy
        
    if y_loptice > visina:          #ako loptica padne u rupu
        preostalo = preostalo - 1
        (x_loptice, y_loptice) = (x_plocice, y_plocice - r)
        lepak = True
    
    for a in range(broj_redova):
            for b in range(broj_kolona):
                if (a,b) not in razbijene:
                    (x_cigle, y_cigle) = cigle[a*broj_kolona + b]

                    if (krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle, y_cigle, y_cigle + debljina_cigle) or \
                    krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle + sirina_cigle, y_cigle, y_cigle + debljina_cigle)) and \
                    (krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle + debljina_cigle) or \
                    krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle)):
                        vy = -vy
                        vx = -vx
                        razbijene.append((a, b))
                        poeni += 10

                    else:
                        if krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle, y_cigle, y_cigle + debljina_cigle) or \
                        krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle + sirina_cigle, y_cigle, y_cigle + debljina_cigle):              
                            
                            razbijene.append((a, b))
                            poeni += 10
                            vx = -vx
                            
                        if krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle + debljina_cigle) or \
                        krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle):
                            razbijene.append((a, b))
                            poeni += 10
                            vy = -vy
                        
    if not lepak:
        x_loptice += vx
        y_loptice += vy
        
    crtaj()


pygamebg.frame_loop(60, novi_frejm, obradi_dogadjaj)
