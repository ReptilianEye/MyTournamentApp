import random
import copy
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
                Standings[findOpponentInList(
                    dual.opponent1_id, Standings)].wins += 1
                Standings[findOpponentInList(
                    dual.opponent2_id, Standings)].loses += 1
            elif dual.score_1 < dual.score_2:
                Standings[findOpponentInList(
                    dual.opponent1_id, Standings)].loses += 1
                Standings[findOpponentInList(
                    dual.opponent2_id, Standings)].wins += 1
            else:
                Standings[findOpponentInList(
                    dual.opponent1_id, Standings)].draws += 1
                Standings[findOpponentInList(
                    dual.opponent2_id, Standings)].draws += 1
    #sorted(Standings,key=lambda team: team.wins, reverse=True)
    return Standings


def GenerateFirstRoundSwiss(T):

    losowanie = copy.deepcopy(T)

    random.shuffle(losowanie)

    pary = []

    i = 0
    n = len(losowanie)
    if n % 2 == 1:
        n -= 1
    while i < n:
        para = []
        para.append(losowanie[i])
        para.append(losowanie[i+1])
        pary.append(para)
        i += 2

    return pary


def GenerateRoundSwiss(Wyniki, Standing):
    Standing = sorted(Standing, key=lambda standing: (
        standing.wins, standing.draws), reverse=True)
    # idzie po kolei xd
    Pary = []
    for i in range(len(Standing)):
        opponent1 = Standing[i]
        if len(Standing) == 0:
            return Pary
        if len(Standing) == 1:
            Pary.append([opponent1.opponent_id, 'Bye'])
            return Pary
        for j in range(i+1, len(Standing)):
            opponent2 = Standing[j]
            if sprawdzankoGraczy(Wyniki, opponent1.opponent_id, opponent2.opponent_id):
                Pary.append([opponent1.opponent_id, opponent2.opponent_id])
                Standing.remove(opponent1)
                Standing.remove(opponent2)
                break
    i == 0
    while len(Standing) > 0:
        opponent1 = Standing[0]
        pairFound = False
        while i <= len(Standing):
            if sprawdzankoGraczy(Wyniki, opponent1.opponent_id, opponent2.opponent_id):
                Pary.append([opponent1.opponent_id, opponent2.opponent_id])
                Standing.remove(opponent1)
                Standing.remove(opponent2)
                pairFound = True
                break
            i += 1
        if not pairFound:
            break
    if len(Standing) == 0:
        return Pary
    else:
        i = 0
        while i < len(Standing):
            Pary.append([Standing[i],Standing[i+1]])
            i += 2-            
    
