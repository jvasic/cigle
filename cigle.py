
# Cigle --- Jovan Vasić 2020

import random
import pygame as pg
import pygamebg
import math
import pygame.mixer

pg.mixer.init()
cigla_zvuk = pg.mixer.Sound("cigla.wav")        #muzike
kraj_muzika = pg.mixer.Sound('kraj.wav')
kraj_muzika.set_volume(0.07)
pg.mixer.music.load('logical.mp3')
pg.mixer.music.set_volume(0.3)

(sirina, visina) = (800, 600)               
prozor = pygamebg.open_window(sirina, visina, 'Cigle')
pg.mouse.set_visible(False)

pg.key.set_repeat(10,10)        #nepotrebno za sad


promena_brzine = 1              #kad se predje na novi nivo
promena_sirine = -6             #menja se brzina i sirina ploce
debljina_plocice = 5                                   
x_plocice = sirina // 2
y_plocice = visina - 100

r = 8
(x_loptice, y_loptice) = (x_plocice, y_plocice - r)

debljina_cigle = 28
sirina_cigle = 46
od_plafona = 120
broj_kolona = 15

razmak = 3
od_zida = (sirina - broj_kolona*sirina_cigle - (broj_kolona - 1)*razmak) // 2

def reset():
    #pocetne vrednosti
    global kraj_igre, broj_redova, sirina_plocice, v, poeni, preostalo, novi_nivo, lepak, klik, kraj_muzika, nivo, space

    kraj_igre = False
    nivo = 0
    broj_redova = nivo + 2
    sirina_plocice = 100 - promena_sirine
    v = 7 - promena_brzine
    poeni = 0
    preostalo = 2
    novi_nivo = True
    lepak = True    #loptica zalepljena za plocicu dok je pocetak igre (ovo se uklanja klikom)
    klik = False
    space = False
    kraj_muzika.stop()
    pg.mixer.music.play(-1)

reset() #pocetak igre

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

def distanca(x1, y1, x2, y2):
    return math.sqrt((y1-y2)**2+(x1-x2)**2)

def nasumicno_odbijanje():
    global v, vx, vy
    vx = random.uniform(-v*0.86, v*0.86)
    vy = -math.sqrt(v*v - vx*vx)

nasumicno_odbijanje()

def nasumicna_boja():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def generisi_boje():
    global boje
    boje = []
    for i in range(broj_redova):
        boje.append(nasumicna_boja())

def krugSeceVertikalnuDuz(cx, cy, r, x, y1, y2):
    if abs(x - cx)<=r and cy>=y1 and cy<=y2:
        return True
    else:
        return False

def krugSeceHorizontalnuDuz(cx, cy, r, x1, x2, y):
    return krugSeceVertikalnuDuz(cy, cx, r, y, x1, x2)

def krugSeceTacku(cx, cy, r, x, y):
    return distanca(cx, cy, x, y) < r

cigle = []
razbijene = []


def crtaj():
    global x_plocice, x_loptice, novi_nivo, y_loptice, kraj_igre, space, razbijene
    prozor.fill(pg.Color('black'))

    if kraj_igre:  
        pg.mixer.music.stop()
        kraj_muzika.play()
        if nivo == 11:
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
        pg.draw.line(prozor, pg.Color('white'),   #plocica
                     (x_plocice - sirina_plocice // 2, y_plocice),            
                     (x_plocice + sirina_plocice // 2, y_plocice), debljina_plocice)
        if lepak:  
            x_loptice = x_plocice
            y_loptice = y_plocice - r
        pg.draw.circle(prozor, pg.Color('white'), (round(x_loptice), round(y_loptice)), r)
        
        for i in range(broj_redova): #crtanje nerazbijenih cigli
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
        if nivo == 11:
            kraj_igre = True
            
def obradi_dogadjaj(dogadjaj):
    global x_plocice, x_loptice, y_loptice, vx, vy, klik, kraj_igre, space
    if not kraj_igre:
        if dogadjaj.type == pg.MOUSEMOTION:
            (x_misa, y_misa) = dogadjaj.pos
            x_plocice = x_misa    #pomeranje plocice misem
            
        if lepak:
            if dogadjaj.type == pg.MOUSEBUTTONDOWN:
                klik = True
                
    if dogadjaj.type == pg.KEYDOWN:
        if dogadjaj.key == pg.K_SPACE:
            space = True

    if dogadjaj.type == pg.KEYUP:
        if dogadjaj.key == pg.K_SPACE:
            space = False

            
def novi_frejm():
    global x_loptice, y_loptice, lepak, vx, vy, v, sirina, visina, preostalo, r, razmak, sirina_cigle, x_plocice, sirina_plocice
    global broj_redova, broj_kolona, od_zida, od_plafona, debljina_cigle, cigle, razbijene, novi_nivo, poeni, klik, nivo, kraj_igre, space
    global promena_sirine, promena_brzine
    if preostalo < 0 or nivo == 9:
        kraj_igre = True    #izgubljeni svi zivoti/poslednji nivo

    if len(razbijene) == len(cigle):   #kraj nivoa kad su razbijene sve cigle
        novi_nivo = True
        
    if novi_nivo:           #NOVI NIVO
        lepak = True
        nivo += 1
        broj_redova += 1
        generisi_boje()
        razbijene = []
        cigle = []
        sirina_plocice += promena_sirine
        v += 1
        for i in range(broj_redova):
            for j in range(broj_kolona):
                cigle.append((j*(sirina_cigle + razmak) + od_zida, od_plafona + (i - 1)*(debljina_cigle + razmak)))
        lepak = True
        novi_nivo = False

    if kraj_igre and space:     #press space to play again
        reset()
    

    if x_loptice - r <= 0:           #odbijanje od zidova
        vx = -vx
    if x_loptice + r >= sirina:
        vx = -vx
    if y_loptice - r <= 0:
        vy = -vy

    if distanca(x_loptice, y_loptice, x_loptice, y_plocice) <= r and x_loptice >= x_plocice-sirina_plocice/2 and x_loptice <= x_plocice+sirina_plocice/2:    #odbijanje od plocice
        if lepak and klik:
            nasumicno_odbijanje()
            lepak = False
            klik = False
        else:
            vx = (x_loptice - x_plocice)/sirina_plocice*2*0.95*v        #loptica se odbija u zavisnosti od mesta na plocici kojw je pogodjeno, max 95% brzine po x (jednoj) osi
            vy = -math.sqrt(v**2 - vx*vx)
    if distanca(x_loptice, y_loptice, x_plocice - sirina_plocice/2, y_plocice)<=r:  #ako je pogodjena ivica plocice 97% od ukupne brzine (odbija se pod malim uglom)
        vx = -0.97*v
        vy = -math.sqrt(v**2 - vx*vx)
    if distanca(x_loptice, y_loptice, x_plocice + sirina_plocice/2, y_plocice)<=r:  #druga ivica
        vx = 0.97*v
        vy = -math.sqrt(v**2 - vx*vx)
        
    if y_loptice > visina:          #ako loptica padne u rupu
        preostalo = preostalo - 1
        (x_loptice, y_loptice) = (x_plocice, y_plocice - r)
        lepak = True
    
    for a in range(broj_redova):
            for b in range(broj_kolona):
                (x_cigle, y_cigle) = cigle[a*broj_kolona + b]
                if (a,b) not in razbijene and not novi_nivo:
                #svaka preostala cigla se proverava da li je pogodjena     
                    if (krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle, y_cigle, y_cigle + debljina_cigle) or \
                    krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle + sirina_cigle, y_cigle, y_cigle + debljina_cigle)) and \
                    (krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle + debljina_cigle) or \
                    krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle)):
                        #ako je pogodjen cosak cigle
                        if (krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle+sirina_cigle+razmak, y_cigle, y_cigle + debljina_cigle) or \
                    krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle+sirina_cigle+razmak + sirina_cigle, y_cigle, y_cigle + debljina_cigle)) and \
                    (krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle+sirina_cigle+razmak, x_cigle+sirina_cigle+razmak + sirina_cigle, y_cigle + debljina_cigle) or \
                    krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle+sirina_cigle+razmak, x_cigle+sirina_cigle+razmak + sirina_cigle, y_cigle)):
                            #ako su pogodjena 2 coska istovremeno, odbija se kao od prave linije (valjda)
                            vy = -vy    #suprotna y komponenta brzine - odbija se na dole/gore
                            cigla_zvuk.play()   #zvuk lomljenja cigle
                            razbijene.append((a, b))    #cigla vise ne postoji
                            poeni += 10     #dodato 10 poena
                        elif (krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle, y_cigle+debljina_cigle+razmak, y_cigle+debljina_cigle+razmak + debljina_cigle) or \
                    krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle + sirina_cigle, y_cigle+debljina_cigle+razmak, y_cigle+debljina_cigle+razmak + debljina_cigle)) and \
                    (krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle+debljina_cigle+razmak + debljina_cigle) or \
                    krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle+debljina_cigle+razmak)):
                            #isto samo vertikalno
                            vx = -vx    #suprotna x komponenta brzine - odbija se levo/desno
                            cigla_zvuk.play()
                            razbijene.append((a, b))
                            poeni += 10
                        else:
                            #samo je jedan cosak pogodjen, vraca se se odakle je dosla
                            vy = -vy    #suprotna brzina
                            vx = -vx
                            cigla_zvuk.play()
                            razbijene.append((a, b))
                            poeni += 10

                    else:              
                        #ako nije cosak
                        if krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle, y_cigle, y_cigle + debljina_cigle) or \
                        krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle + sirina_cigle, y_cigle, y_cigle + debljina_cigle):        
                            #ako je pogodjena leva/desna stranica cigle
                            cigla_zvuk.play()
                            razbijene.append((a, b))
                            poeni += 10
                            vx = -vx
                            
                        if krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle + debljina_cigle) or \
                        krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle):
                            #ako je pogodjena gornja/donja stranica
                            cigla_zvuk.play()
                            razbijene.append((a, b))
                            poeni += 10
                            vy = -vy
                    
    if not lepak:
        x_loptice += vx     #posalji lopticu gde treba
        y_loptice += vy

    crtaj()
    
pygamebg.frame_loop(60, novi_frejm, obradi_dogadjaj)
