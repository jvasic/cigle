# Cigle --- Jovan Vasić 2020
# version no: 1.2

import random
import pygame as pg
import pygamebg
import math
import pygame.mixer
import pprint

pg.mixer.init()
cigla_zvuk = pg.mixer.Sound("cigla.wav")        #muzike
kraj_muzika = pg.mixer.Sound('kraj.wav')
kraj_muzika.set_volume(0.07)
powerup_zvuk = pg.mixer.Sound('power_up.wav')
powerup_zvuk.set_volume(12)
pg.mixer.music.load('logical.mp3')
pg.mixer.music.set_volume(0.3)

(sirina, visina) = (800, 600)               
prozor = pygamebg.open_window(sirina, visina, 'Cigle')
pg.mouse.set_visible(False)

pg.key.set_repeat(10,10)        #nepotrebno za sad

vo = 7
promena_brzine = 0.5              #kad se predje na novi nivo
promena_sirine = -5             #menja se brzina i sirina ploce
debljina_plocice = 5
sirina_plocice_o = 100
x_plocice = sirina // 2
y_plocice = visina - 100

ro = 8
max_nivo = 10
visina_cigle = 28
sirina_cigle = 46
od_plafona = 120
broj_kolona = 15
razmak = 3
od_zida = (sirina - broj_kolona*sirina_cigle - (broj_kolona - 1)*razmak) // 2

manja_loptica, veca_loptica, manja_plocica, veca_plocica, prolazak, usporenje, ubrzanje, smrt, zivot = 0, 0, 0, 0, 0, 0, 0, 0, 0
powerups = [manja_loptica, veca_loptica, manja_plocica, veca_plocica, prolazak, usporenje, ubrzanje, smrt, zivot]
string_powerups = ['manja loptica', 'veća loptica', 'manja pločica', 'veća pločica', 'prolazak', 'usporenje', 'ubrzanje', 'smrt', 'život']
power_verovatnoca = 50    #n%
def no_powerups():
    global powerups
    for i in range(len(powerups)):
        powerups[i] =  0

def reset():
    #pocetne vrednosti
    global kraj_igre, broj_redova, sirina_plocice, v, poeni, preostalo, novi_nivo, lepak, klik, kraj_muzika, nivo, space, r, ro, vo
    kraj_igre = False
    nivo = 0
    broj_redova = nivo + 2
    sirina_plocice = sirina_plocice_o - promena_sirine
    r = ro
    v = vo - promena_brzine
    poeni = 0
    preostalo = 2
    novi_nivo = True
    lepak = True    #loptica zalepljena za plocicu dok je pocetak igre (ovo se uklanja klikom)
    klik = False
    space = False
    kraj_muzika.stop()
    pg.mixer.music.play(-1) #muzika se cuje konstantno

reset() #pocetak igre
(x_loptice, y_loptice) = (x_plocice, y_plocice - r)

def tekst_ispis(x, y, tekst, velicina):
    font = pg.font.SysFont('Bahnschrift', velicina)
    tekst = font.render(tekst, True, pg.Color('white'))
    prozor.blit(tekst, (x, y))

def tekst_centar(x, y, tekst, velicina, boja):
    font = pg.font.SysFont('Bahnschrift', velicina)
    tekst = font.render(tekst, True, pg.Color(boja))
    (sirina_teksta, visina_teksta) = (tekst.get_width(), tekst.get_height())
    (x, y) = (x - sirina_teksta / 2, y - visina_teksta / 2)
    prozor.blit(tekst, (x, y))

def sareni_tekst(x, y, tekst, velicina, boja):
    font = pg.font.SysFont('Bahnschrift', velicina)
    tekst = font.render(tekst, True, pg.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    (sirina_teksta, visina_teksta) = (tekst.get_width(), tekst.get_height())
    (x, y) = (x - sirina_teksta / 2, y - visina_teksta / 2)
    prozor.blit(tekst, (x, y))

def nasumicna_boja():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

def distanca(x1, y1, x2, y2):
    return math.sqrt((y1-y2)**2+(x1-x2)**2)

def nasumicno_odbijanje():
    global v, vx, vy
    vx = random.uniform(-v*0.86, v*0.86)
    vy = -math.sqrt(v*v - vx*vx)

nasumicno_odbijanje()

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

def power_v():
    global power_verovatnoca
    return random.choices((True, False), weights=(power_verovatnoca, 100-power_verovatnoca))

def razbij_ciglu(a, b):
    global cigla_zvuk, poeni, razbijene, power_cigle, power_animacije, powerups
    cigla_zvuk.play()
    poeni += 10
    if (a, b) not in power_cigle:   #cigla vise ne postoji
        razbijene.append((a, b))
    else:
        power_cigle.remove((a, b))
        power_animacije.append((b*(sirina_cigle + razmak) + od_zida - sirina_cigle/2, od_plafona + (a - 1)*(visina_cigle + razmak), (random.randint(0, len(powerups)-1))))
        
def crtaj_powerup():
    global power_animacije, visina, powerups, sirina_plocice, x_plocice, y_plocice, r
    for i in range (len(power_animacije)):
        (x, y, index) = power_animacije[-i]
        if x < 30:
            x = 30
        if x > sirina-30:
            x = sirina - 30
        y += 2.5
        power_animacije[-i] = (x, y, index)
        if x >= x_plocice-sirina_plocice/2 and x <= x_plocice+sirina_plocice/2 and y >= y_plocice - 3 and y <= y_plocice + 1:
            powerups[index] += 1
            powerup_zvuk.play()
            power_animacije.remove((x, y, index))
        if y > visina:
            power_animacije.remove((x, y, index))
        else:
            pg.draw.circle(prozor, pg.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), (round(x), round(y-20)), 5, 1)
            sareni_tekst(x, y, string_powerups[index], 20, (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
cigle = []
razbijene = []


def crtaj():
    global x_plocice, x_loptice, novi_nivo, y_loptice, kraj_igre, space, razbijene, r, sirina_plocice
    prozor.fill(pg.Color('black'))

    if kraj_igre:  
        pg.mixer.music.stop()
        kraj_muzika.play()
        if nivo == 11:
            tekst_centar(sirina/2, visina/2, 'GAME WON!!! '+str(poeni)+' points', 70, 'white')
        else:
            tekst_centar(sirina/2, visina/2, 'GAME OVER: '+str(poeni)+' points', 70, 'white')
        tekst_centar(sirina/2, visina/2 + 80, 'press SPACE to play again', 50, 'white')
        
    else:
        if lepak:
            tekst_centar(sirina/2, visina/2, 'LEVEL '+str(nivo), 70, 'white')
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
                    if (i,j) in power_cigle:
                        debljina_cigle = 0
                        lokalna_sirina_cigle = sirina_cigle + 1
                        lokalna_visina_cigle = visina_cigle + 1
                    else:
                        debljina_cigle = 2
                        lokalna_sirina_cigle = sirina_cigle
                        lokalna_visina_cigle = visina_cigle
                    pg.draw.rect(prozor, boja_reda,
                                 (j*(sirina_cigle + razmak) + od_zida, od_plafona + (i - 1)*(visina_cigle + razmak),
                                  lokalna_sirina_cigle, lokalna_visina_cigle), debljina_cigle)
            
        tekst_ispis(14, 7, str(poeni), 50)
        if preostalo>0:
            for i in range (0,preostalo):
                pg.draw.circle(prozor, pg.Color('white'), (sirina - i*36-27, 23), 2*8)
        crtaj_powerup()
        
def obradi_dogadjaj(dogadjaj):
    global x_plocice, x_loptice, y_loptice, vx, vy, klik, kraj_igre, space
    if not kraj_igre:
        if dogadjaj.type == pg.MOUSEMOTION:
            (x_misa, y_misa) = dogadjaj.pos
            x_plocice = x_misa    #pomeranje plocice misem            
        #if lepak:
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
    global broj_redova, broj_kolona, od_zida, od_plafona, visina_cigle, cigle, razbijene, novi_nivo, poeni, klik, nivo, kraj_igre, space
    global promena_sirine, promena_brzine, power_verovatnoca, power_cigle, power_animacije, max_nivo
    global powerups, manja_loptica, veca_loptica, manja_plocica, veca_plocica, prolazak, usporenje, ubrzanje, smrt, zivot, ro, sirina_plocice_o, vo
    
    if preostalo < 0 or nivo > max_nivo:
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
        power_cigle = []
        power_animacije = []
        pomoc = random.choices((True, False), weights=(power_verovatnoca, 100-power_verovatnoca), k=broj_redova*broj_kolona)
        for i in range(broj_redova):
            for j in range(broj_kolona):
                cigle.append((j*(sirina_cigle + razmak) + od_zida, od_plafona + (i - 1)*(visina_cigle + razmak)))                
                if pomoc[i*broj_redova+j] == True:
                    power_cigle.append((i, j))
        lepak = True
        novi_nivo = False
        
    if lepak:
        no_powerups()
        r = ro
        v = vo + promena_brzine*(nivo-1)
        sirina_plocice = sirina_plocice_o + promena_sirine*(nivo-1)
        
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
        #smrt_zvuk.play()
        preostalo = preostalo - 1
        (x_loptice, y_loptice) = (x_plocice, y_plocice - r)
        lepak = True
    
    for a in range(broj_redova):
            for b in range(broj_kolona):
                (x_cigle, y_cigle) = cigle[a*broj_kolona + b]
                if (a,b) not in razbijene and not novi_nivo:
                #svaka preostala cigla se proverava da li je pogodjena     
                    if (krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle, y_cigle, y_cigle + visina_cigle) or \
                    krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle + sirina_cigle, y_cigle, y_cigle + visina_cigle)) and \
                    (krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle + visina_cigle) or \
                    krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle)):
                        #ako je pogodjen cosak cigle
                        if (krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle+sirina_cigle+razmak, y_cigle, y_cigle + visina_cigle) or \
                    krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle+sirina_cigle+razmak + sirina_cigle, y_cigle, y_cigle + visina_cigle)) and \
                    (krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle+sirina_cigle+razmak, x_cigle+sirina_cigle+razmak + sirina_cigle, y_cigle + visina_cigle) or \
                    krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle+sirina_cigle+razmak, x_cigle+sirina_cigle+razmak + sirina_cigle, y_cigle)):
                            #ako su pogodjena 2 coska istovremeno, odbija se kao od prave linije (valjda)
                            if not prolazak > 0:
                                vy = -vy    #suprotna y komponenta brzine - odbija se na dole/gore
                            razbij_ciglu(a,b)    
                        elif (krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle, y_cigle+visina_cigle+razmak, y_cigle+visina_cigle+razmak + visina_cigle) or \
                    krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle + sirina_cigle, y_cigle+visina_cigle+razmak, y_cigle+visina_cigle+razmak + visina_cigle)) and \
                    (krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle+visina_cigle+razmak + visina_cigle) or \
                    krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle+visina_cigle+razmak)):
                            #isto samo vertikalno
                            if not prolazak > 0:
                                vx = -vx    #suprotna x komponenta brzine - odbija se levo/desno
                            razbij_ciglu(a,b)
                        else:
                            if not prolazak > 0:
                            #samo je jedan cosak pogodjen, vraca se se odakle je dosla
                                vy = -vy    #suprotna brzina
                                vx = -vx
                            razbij_ciglu(a,b)
                    else:              
                        #ako nije cosak
                        if krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle, y_cigle, y_cigle + visina_cigle) or \
                        krugSeceVertikalnuDuz(x_loptice, y_loptice, r, x_cigle + sirina_cigle, y_cigle, y_cigle + visina_cigle):        
                            #ako je pogodjena leva/desna stranica cigle
                            razbij_ciglu(a,b)
                            if not prolazak > 0:
                                vx = -vx                            
                        if krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle + visina_cigle) or \
                        krugSeceHorizontalnuDuz(x_loptice, y_loptice, r, x_cigle, x_cigle + sirina_cigle, y_cigle):
                            #ako je pogodjena gornja/donja stranica
                            razbij_ciglu(a,b)
                            if not prolazak > 0:
                                vy = -vy

    #POWERUPS
    if powerups[0] > 0: #manja_loptica
        if r <= 4:
            powerups[0] = 0
        else:
            r = r - 2
        powerups[0] = powerups[0]-1
    if powerups[1] > 0: #veca_loptica
        r = r + 2
        powerups[1] = powerups[1]-1
    if powerups[2] > 0: #manja_plocica
        if sirina_plocice <= 20:
            powerups[2] = 0
        else:
            sirina_plocice = sirina_plocice - 20
        powerups[2] = powerups[2]-1
    if powerups[3] > 0: #veca_plocica
        sirina_plocice = sirina_plocice + 20
        powerups[3] = powerups[3]-1
    if powerups[4] > 0: #(ubaceno gore)  #prolazak 
        prolazak = 1
        if lepak:
            prolazak = 0
    if powerups[5] > 0: #usporenje
        v = v - v/4
        powerups[5] = powerups[5]-1
    if powerups[6] > 0: #ubrzanje
        v = v + v/4
        powerups[6] = powerups[6]-1
    if powerups[7] > 0: #smrt
        y_loptice = visina + r + 1
        powerups[7] = 0
    if powerups[8] > 0: #zivot
        preostalo = preostalo + 1
        powerups[8] = 0
        
    if not lepak:
        x_loptice += vx     #posalji lopticu gde treba
        y_loptice += vy

    crtaj()

pygamebg.frame_loop(60, novi_frejm, obradi_dogadjaj)
