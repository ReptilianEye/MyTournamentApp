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


def generateStandings(duels):
    Standings = []
    for duel in duels:
        if not (duel.score_1 is None and duel.score_2 is None):
            if findOpponentInList(duel.opponent1_id, Standings) == None:
                Standings.append(OpponentInStanding(duel.opponent1_id))
            if findOpponentInList(duel.opponent2_id, Standings) == None:
                Standings.append(OpponentInStanding(duel.opponent2_id))
            if duel.score_1 > duel.score_2:
                Standings[findOpponentInList(
                    duel.opponent1_id, Standings)].wins += 1
                Standings[findOpponentInList(
                    duel.opponent2_id, Standings)].loses += 1
            elif duel.score_1 < duel.score_2:
                Standings[findOpponentInList(
                    duel.opponent1_id, Standings)].loses += 1
                Standings[findOpponentInList(
                    duel.opponent2_id, Standings)].wins += 1
            else:
                Standings[findOpponentInList(
                    duel.opponent1_id, Standings)].draws += 1
                Standings[findOpponentInList(
                    duel.opponent2_id, Standings)].draws += 1
    #sorted(Standings,key=lambda team: team.wins, reverse=True)
    return Standings


def GenerateFirstRoundSwiss(opponents,bye):

    losowanie = copy.deepcopy(opponents)

    random.shuffle(losowanie)

    pary = []

    i = 0
    n = len(losowanie)
    if n % 2 == 1:
        losowanie.append(bye)
    while i < n:
        para = []
        para.append(losowanie[i])
        para.append(losowanie[i+1])
        pary.append(para)
        i += 2

    return pary


def GenerateRoundSwiss(opponents, standings, duels):
    OpponentsList = prepareListToSwiss(opponents, standings)

    OpponentsList = sorted(OpponentsList, key=lambda opponent: (
        opponent.wins, opponent.draws), reverse=True)

    # idzie po kolei xd

    Pary = []
    pauza = 'Bye'
    if len(OpponentsList) % 2 == 1:
        OpponentsList.append(pauza)
    while len(OpponentsList) > 0:
        opponent1 = OpponentsList[0]
        pairFound = False
        i = 1
        while i <= len(OpponentsList):
            opponent2 = OpponentsList[i]
            if sprawdzankoGraczy(duels, opponent1, opponent2):
                if opponent1 != pauza and opponent2 != pauza:
                    Pary.append([opponent1, opponent2])
                    pairFound = True
                OpponentsList.remove(opponent1)
                OpponentsList.remove(opponent2)
                break
            i += 1
        if not pairFound:
            break
    if len(OpponentsList) != 0:
        i = 0
        while i < len(duels):
            if OpponentsList[i] != pauza and OpponentsList[i+1] != pauza:
                Pary.append([OpponentsList[i], OpponentsList[i+1]])
            i += 2
    return Pary


def GenerateFirstRoundTree(opponents, ileGraczy):
    firstRound = []
    i = 0
    random.shuffle(opponents)
    while i < ileGraczy:
        firstRound.append([opponents[i], opponents[i+1]])
        i += 2
    return firstRound

def GenerateRoundTreeWithRest(prevRound, rest):
    winners = []
    for duel in prevRound:
        rest.append(whoWins(duel))
    i = 0
    while i < len(rest):
        winners.append([rest[i], rest[i+1]])
        i += 2
    return winners


def GenerateRoundTreeWithoutRest(prevRound):
    winners = []
    i = 0
    while i < len(prevRound):
        firstInDuel = whoWins(prevRound[i])
        secoundInDuel = whoWins(prevRound[i+1])
        winners.append([firstInDuel, secoundInDuel])
        i += 2
    return winners
