import random
from .models import Tournament

pauza = "pauza"


def PrzygotowujeTerminarzDoWyswietlenia(terminarz):
    global pauza

    Terminarz = []
    numerRundy = 1

    for Runda in terminarz:
        Terminarz.append(numerRundy)
        for para in Runda:
            if pauza in para:
                continue
            Para = []
            Para.append(para[0])
            Para.append(para[1])
            Terminarz.append(Para)
        numerRundy += 1

    return Terminarz


def ZapisujeWTerminarzFormieCSV(terminarz):
    global pauza
    with open("Terminarz.csv", "w") as file:
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


def DodajParyDoTermiarza(TablicaMeczy, Terminarz, n):
    runda = []
    for numerKolumny in range(n//2):
        para = []
        para.append(TablicaMeczy[0][numerKolumny])
        para.append(TablicaMeczy[1][numerKolumny])
        runda.append(para)
    Terminarz.append(runda)


def PrzesuwaListeZawodnikow(ListaZawodnikow, n):
    # przesuwa liczbe na srodku na koniec listy
    sr = ListaZawodnikow.pop(n//2-1)
    ListaZawodnikow.append(sr)

    # przesuwa zawodnika na srodku na pozycje pierwszego +1 (pozycji pierwszego nie zmieniamy)
    sr = ListaZawodnikow.pop(n//2-1)
    ListaZawodnikow.insert(1, sr)


def ZnajdujeIndexPary(t1, t2, zaDuzoBialych, zaDuzoCzarnych):
    for z1 in zaDuzoBialych:
        for z2 in zaDuzoCzarnych:
            for i in range(len(t1)):
                if t1[i] == z1 and t2[i] == z2:
                    return i


def WyrownujeMeczeNaStronach(terminarz, n):
    t1 = []
    t2 = []
    for runda in terminarz:
        for para in runda:  # Rozdziela terminarz na dwie tablice aby porownac pary
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
        if len(zaDuzoBialych) == 0:  # zakoncz jesli jest rowno
            break
        # `kiedy liczba zawodnikow jest nieparzysta nie mozna podzielic po rowno,
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


def WygenerujTermiarzRoundRobin(Uczestnicy):

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
        # PokazPary(TablicaMeczy,n)
        DodajParyDoTermiarza(TablicaMeczy, Terminarz, n)
        PrzesuwaListeZawodnikow(ListaZawodnikow, n)
        i += 1

    Terminarz = WyrownujeMeczeNaStronach(Terminarz, n)

    Terminarz = PrzygotowujeTerminarzDoWyswietlenia(Terminarz)
    return Terminarz


def Generate2Teams(ListaZawodników):
    lista1 = []
    lista2 = []

    random.shuffle(ListaZawodników)
    n = 1
    for imie in ListaZawodników:
        if n == 1:
            lista1.append(imie)
        else:
            lista2.append(imie)
        n *= -1
    Terminarz = []
    Terminarz.append(lista1)
    Terminarz.append(lista2)
    return Terminarz


class OpponentInStanding:
    def __init__(self, id, wins=0, loses=0, draws=0):
        self.id = id
        self.wins = wins
        self.loses = loses
        self.draws = draws

# return index of player in a list


def findOpponentInList(player_id, L):
    for i in range(len(L)):
        if L[i].id == player_id:
            return i

def getOpponentPoints(player_id, S):
    for i in range(len(S)):
        if S[i].opponent_id == player_id:
            return S[i].match_points
    return 0


def sprawdzankoGraczy(Wyniki,Gracz1,Gracz2):
    for el in Wyniki:
        para=[el.opponent1_id, el.opponent2_id]
        if Gracz1 in para and Gracz2 in para:
           return False
    return True

def prepareListToSwiss(players,standings):
    pointsTable = []
    visited = {}
    for el in standings:
        pointsTable.append(OpponentInStanding(el.opponent_id,el.wins,el.loses,el.draws))
        visited.update({el.opponent_id:True})
    if len(players) != len(standings):
        for player in players:
            result = visited.get(player.id)
            if result is None:
                pointsTable.append(OpponentInStanding(player.id,draws=1))
    return pointsTable



def whoWins(duel,reverse = False):
    if duel.score_1 > duel.score_2 and not reverse:
        return duel.opponent_1
    else:
        return duel.opponent_2

def checkIfScoresAreWritten(duels):
    for duel in duels:
        if duel.score_1 is None or duel.score_2 is None:
            return False
    return True

def checkIfScoresAreDecided(duels):
    for duel in duels:
        if duel.score_1 == duel.score_2:
            return False
    return True

def checkIfEveryonePlayed(opponents,duels):
    for duel in duels:
        if duel.opponent_1 in opponents:
            opponents.remove(duel.opponent_1)
        if duel.opponent_2 in opponents:
            opponents.remove(duel.opponent_2)
    if len(opponents) == 0:
        return []
    else:
        return opponents
        