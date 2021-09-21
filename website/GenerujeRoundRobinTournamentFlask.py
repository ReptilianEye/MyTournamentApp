import time
import random
import os
import progressbar

pauza = "pauza"

def PasekLadowania():
    widgets = [
        "LOSOWANIE PAR: " ,
        progressbar.Bar(),
        progressbar.Percentage()
    ]
    for i in progressbar.progressbar(range(100), widgets=widgets):
        if i == 99:
            time.sleep(3)
        time.sleep(0.05)
    print("PARY WYLOSOWANE!")
    time.sleep(2)
    os.system('cls')

def PrzygotowujeTerminarzDoWyswietlenia(terminarz):
    global pauza

    Terminarz = []
    numerRundy = 1
    numerPary = 0

    for Runda in terminarz:
        Terminarz.append(numerRundy)
        for para in Runda:
            if pauza in para:
                continue
            Terminarz.append([])
            Terminarz[numerPary].append(para[0])
            Terminarz[numerPary].append(para[1])
            numerPary += 1

        numerRundy += 1
    
    return Terminarz

def ZapisujeWTerminarzFormieCSV(terminarz):
    global pauza
    with open("Terminarz.csv","w") as file:
        numerRundy = 1
        for Runda in terminarz:
            file.write(f"Runda {numerRundy}\n")
            for para in Runda:
                if pauza in para:
                    continue
                file.write(f";{para[0]};;;{para[1]}\n")
            numerRundy += 1

def WczytujeDane(Uczestnicy):
    ListaZawodnikow = []
    for uczestnik in Uczestnicy:
        imie = uczestnik.name
        imie = imie.strip()
        if imie == "":
            break
        ListaZawodnikow.append(imie)
    return ListaZawodnikow

def PrzygotujTabliceMeczy(ListaZawodnikow):
    TablicaMeczy = []
    i = 0
    numerZawodnika = 0
    while i < 2:
        TablicaMeczy.append([])
        j = 0
        while j < len(ListaZawodnikow)//2:
            TablicaMeczy[i].append(ListaZawodnikow[numerZawodnika])
            j += 1
            numerZawodnika += 1
        i += 1
    
    return TablicaMeczy


def DodajParyDoTermiarza(TablicaMeczy,Terminarz,n):
    runda = []
    for numerKolumny in range(n//2):
        para = []
        para.append(TablicaMeczy[0][numerKolumny])
        para.append(TablicaMeczy[1][numerKolumny])
        runda.append(para)
    Terminarz.append(runda)


def PrzesuwaListeZawodnikow(ListaZawodnikow,n):
    sr = ListaZawodnikow.pop(n//2-1)        #przesuwa liczbe na srodku na koniec listy
    ListaZawodnikow.append(sr)

    sr = ListaZawodnikow.pop(n//2-1)        #przesuwa zawodnika na srodku na pozycje pierwszego +1 (pozycji pierwszego nie zmieniamy)
    ListaZawodnikow.insert(1,sr)


def ZnajdujeIndexPary(t1, t2, zaDuzoBialych, zaDuzoCzarnych):
    for z1 in zaDuzoBialych:
        for z2 in zaDuzoCzarnych:
            for i in range(len(t1)):
                if t1[i] == z1 and t2[i] == z2:
                    return i


def WyrownujeMeczeNaStronach(terminarz,n):
    t1 = []
    t2 = []
    for runda in terminarz:
        for para in runda:          #Rozdziela terminarz na dwie tablice aby porownac pary
            t1.append(para[0])
            t2.append(para[1])
    
    while True:
        zaDuzoBialych = []
        zaDuzoCzarnych = []
        for zawodnik in t1:
            zaDuzoBialych.append(zawodnik)
        for zawodnik in t2:
            if zawodnik in zaDuzoBialych:
                zaDuzoBialych.remove(zawodnik)
            else:
                zaDuzoCzarnych.append(zawodnik)
        if len(zaDuzoBialych) == 0:     #zakoncz jesli jest rowno
            break
        #`kiedy liczba zawodnikow jest nieparzysta nie mozna podzielic po rowno,
        #  wiec sprawdzamy az do momentu jest tak rowno jak sie da,
        #  (w praktyce kazda osoba bedzie grala po jednej stronie 1 raz wiecej)
        if len(zaDuzoBialych) == len(set(zaDuzoBialych)) and len(zaDuzoCzarnych) == len(set(zaDuzoCzarnych)):
            break
        indexPary = ZnajdujeIndexPary(t1, t2, zaDuzoBialych, zaDuzoCzarnych)
        t1[indexPary], t2[indexPary] = t2[indexPary], t1[indexPary]
    
    NowyTerminarz = []
    NowyTerminarz.append([])

    i = 0
    ileWRundzie = 0
    numerRundy = 0
    coIleDzieli = n//2

    while i < len(t1):
        
        if ileWRundzie == coIleDzieli:
            ileWRundzie = 0
            numerRundy += 1
            NowyTerminarz.append([])
        
        para = []
        para.append(t1[i])
        para.append(t2[i])
        NowyTerminarz[numerRundy].append(para)
        ileWRundzie += 1
        i += 1

    return NowyTerminarz


def WygenerujTermiarz(Uczestnicy):
    
    Terminarz = []
    global pauza
    ListaZawodnikow = WczytujeDane(Uczestnicy)
    if len(ListaZawodnikow) % 2 == 1:
        ListaZawodnikow.append(pauza)
    
    random.shuffle(ListaZawodnikow)     # miesza kolejnosc zawodnikow
    
    n = len(ListaZawodnikow)

    i = 0
    while i < n - 1:
        TablicaMeczy = PrzygotujTabliceMeczy(ListaZawodnikow)
        #PokazPary(TablicaMeczy,n)
        DodajParyDoTermiarza(TablicaMeczy,Terminarz,n)
        PrzesuwaListeZawodnikow(ListaZawodnikow,n)
        i += 1
    
    Terminarz = WyrownujeMeczeNaStronach(Terminarz,n)


    Terminarz = PrzygotowujeTerminarzDoWyswietlenia(Terminarz)
    return Terminarz


