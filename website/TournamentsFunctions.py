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


def printStandings(L):
    for el in L:
        print(el.id)


def generateStandings(tournament):
    Standings = []
    print(tournament.duals)
    for dual in tournament.duals:
        if findTeamInList(dual.team1_id, Standings) == None:
            Standings.append(TeamInStanding(dual.team1_id))
        if findTeamInList(dual.team2_id, Standings) == None:
            Standings.append(TeamInStanding(dual.team2_id))
        if dual.score_1 > dual.score_2:
            Standings[findTeamInList(dual.team1_id, Standings)].wins += 1
            Standings[findTeamInList(dual.team2_id, Standings)].loses += 1
        elif dual.score_1 < dual.score_2:
            Standings[findTeamInList(dual.team1_id, Standings)].loses += 1
            Standings[findTeamInList(dual.team2_id, Standings)].wins += 1
        else:
            Standings[findTeamInList(dual.team1_id, Standings)].draws += 1
            Standings[findTeamInList(dual.team2_id, Standings)].draws += 1
    #sorted(Standings,key=lambda team: team.wins, reverse=True)
    return Standings
