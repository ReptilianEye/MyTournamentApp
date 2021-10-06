import random
from .AdditionalFunctions import *

def GenerateRoundRobin(ListaZawodnikow):
    return WygenerujTermiarzRoundRobin(ListaZawodnikow)


def Generate2Teams(ListaZawodnikow):
    lista1 = []
    lista2 = []

    random.shuffle(ListaZawodnikow)
    n = 1
    for imie in ListaZawodnikow:
        if n == 1:
            lista1.append(imie)
        else:
            lista2.append(imie)
        n *= -1
    Terminarz = []
    Terminarz.append(lista1)
    Terminarz.append(lista2)
    return Terminarz

def generateStandings(duals):
    Standings = []
    for dual in duals:
        if not (dual.score_1 is None and dual.score_2 is None):
            if findOpponentInList(dual.opponent1_id, Standings) == None:
                Standings.append(OpponentInStanding(dual.opponent1_id))
            if findOpponentInList(dual.opponent2_id, Standings) == None:
                Standings.append(OpponentInStanding(dual.opponent2_id))
            if dual.score_1 > dual.score_2:
                Standings[findOpponentInList(dual.opponent1_id, Standings)].wins += 1
                Standings[findOpponentInList(dual.opponent2_id, Standings)].loses += 1
            elif dual.score_1 < dual.score_2:
                Standings[findOpponentInList(dual.opponent1_id, Standings)].loses += 1
                Standings[findOpponentInList(dual.opponent2_id, Standings)].wins += 1
            else:
                Standings[findOpponentInList(dual.opponent1_id, Standings)].draws += 1
                Standings[findOpponentInList(dual.opponent2_id, Standings)].draws += 1
    #sorted(Standings,key=lambda team: team.wins, reverse=True)
    return Standings

