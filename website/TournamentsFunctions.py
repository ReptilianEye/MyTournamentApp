import random
import copy
import math
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


def GenerateRoundSwiss(opponents, standings, duels):
    PlayersList =  prepareListToSwiss(opponents, standings)
    
    PlayersList = sorted(PlayersList, key=lambda opponent: (
        opponent.wins, opponent.draws), reverse=True)

    # idzie po kolei xd

    Pary = []
    pauza = 'Bye'
    if len(PlayersList) % 2 == 1:
        PlayersList.append(pauza)
    while len(PlayersList) > 0:
        opponent1 = PlayersList[0]
        pairFound = False
        i = 1
        while i <= len(PlayersList):
            opponent2 = PlayersList[i]
            if sprawdzankoGraczy(duels, opponent1, opponent2):
                if opponent1 != pauza and opponent2 != pauza:
                    Pary.append([opponent1, opponent2])
                    pairFound = True
                PlayersList.remove(opponent1)
                PlayersList.remove(opponent2)
                break

            i += 1
        if not pairFound:
            break
    if len(PlayersList) != 0:
        i = 0
        while i < len(duels):
            if PlayersList[i] != pauza and PlayersList[i+1] != pauza: 
                Pary.append([PlayersList[i],PlayersList[i+1]])
            i += 2            
    return Pary
    
def generateFirstRoundTree(players, wildcard):
    potegaWiekszej = math.ceil(math.log2(len(players)))
    potegaDwojki = pow(2, potegaWiekszej)
    liczbaWildcard = potegaDwojki - len(players)

    pary=[]
    e=0
    while e < liczbaWildcard:
        gracz=random.choice(players)
        pary.append([gracz, wildcard])
        players.remove(gracz)
        e+=1
    p=0
    random.shuffle(players)
    while p < len(players):
        pary.append([players[p], players[p+1]])
        p+=2


def GenerateRoundTree(duels, limit=10000):
    winners = []
    i = 0
    while i < len(duels):
        if len(winners) == limit:
            return winners
        firstInDual = whoWins(duels[i].opponent1, duels[i].opponent2)
        secoundInDual = whoWins(duels[i + 1].opponent1, duels[i + 1].opponent2)
        winners.append([firstInDual, secoundInDual])
        i += 2
    return winners  
