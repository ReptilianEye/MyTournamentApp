from .TournamentsFunctions import *
from .import db
from .models import Opponent, User, Tournament, Dual, Opponent, Standing, Round
import math

class TournamentController():

    def CreateNew(self, user_Id, name, date, location, discipline, type):
        self.tournament = Tournament(user_id=user_Id, name=name,
                                     date=date, location=location, discipline=discipline, type=type)
        db.session.add(self.tournament)
        db.session.commit()
        return self.tournament.id

    def Load(self, id):
        self.tournament = Tournament.query.get(id)

    def Save(self):  # self is always required as a argument
        db.session.commit()

    def UploadPlayer(self, opponent):
        db.session.add(
            Opponent(tournament_id=self.tournament.id, name=opponent))

    def ChangeEditedDual(self, dual_id):
        self.tournament.edited_dual_id = dual_id

    def GetChangedDual(self):
        return Dual.query.filter_by(id=self.tournament.edited_dual_id).first()

    def UpdateScores(self, score1, score2):
        dual = Dual.query.filter_by(id=self.tournament.edited_dual_id).first()
        dual.score1 = score1
        dual.score2 = score2

    def DeleteTournament(self):

        for round in self.tournament.rounds:
            db.session.delete(round)

        for dual in self.tournament.duals:
            db.session.delete(dual)

        for opponent in self.tournament.opponents:
            db.session.delete(opponent)

        for standing in self.tournament.standings:
            db.session.delete(standing)

        db.session.delete(self.tournament)

    tournamentTypes = ['RoundRobin', 'Swiss']

    def PrepareNewRound(self):
        if self.tournament.type == self.tournamentTypes[0]:
            return RoundRobinRS(self.tournament).getNewRound()
        if self.tournament.type == self.tournamentTypes[1]:
            return SwissRS(self.tournament).getNewRound()

    def PrepareStanding(self):
        standing = generateStandings(self.tournament.duals)
        if self.tournament.discipline == self.disciplines[0]:
            Tournament = ChessTournament()
        elif self.tournament.discipline == self.disciplines[1]:
            Tournament = BasketballTournament()
        else:
            Tournament = FootballTournament()
        Tournament.Load(self.tournament.id)

        for opponent in standing:
            db.session.add(Standing(tournament_id=Tournament.tournament.id, opponent_id=opponent.id,
                                    wins=opponent.wins, loses=opponent.loses, draws=opponent.draws, match_points=opponent.wins*Tournament.multipleForWin+opponent.loses*Tournament.multipleForLose+opponent.draws*Tournament.multipleForDraw))

    disciplines = ['Chess', 'Basketball', 'Football']

    def ShowStanding(self):
        if len(self.tournament.standings) == 0:
            self.PrepareStanding()
        return sorted(self.tournament.standings, key=lambda standing: (standing.match_points, standing.wins, standing.draws), reverse=True)

    def DeleteStanding(self):
        for standing in self.tournament.standings:
            db.session.delete(standing)
        self.Save()


class ChessTournament(TournamentController):
    multipleForWin = 1
    multipleForLose = 0
    multipleForDraw = 0.5

    def PrepareStanding(self):
        pass


class BasketballTournament(TournamentController):
    multipleForWin = 2
    multipleForLose = 1
    multipleForDraw = 1

    def PrepareStanding(self):
        return super().PrepareStanding()


class FootballTournament(TournamentController):
    multipleForWin = 3
    multipleForLose = 0
    multipleForDraw = 1

    def PrepareStanding(self):
        return super().PrepareStanding()


class RoundStrategy():

    def __init__(self, tournament):
        self.tournament = tournament

    def getNewRound(self):
        pass

    def createNewRound(self, round_number):
        newRund = Round(tournament_id=self.tournament.id, number=round_number)
        db.session.add(newRund)
        db.session.commit()
        return newRund.id


class RoundRobinRS(RoundStrategy):

    def __generateSchedule(self):       # "__" means private method
        schedule = GenerateRoundRobin(self.tournament.opponents)
        round_number = 0
        for line in schedule:
            if type(line) is int:
                round_number = line
                newRundId = self.createNewRound(round_number)
            else:
                opponent1 = Opponent.query.filter_by(
                    name=line[0], tournament_id=self.tournament.id).first()
                opponent2 = Opponent.query.filter_by(
                    name=line[1], tournament_id=self.tournament.id).first()

                db.session.add(Dual(tournament_id=self.tournament.id, round_id=newRundId, opponent1_id=opponent1.id,
                                    opponent2_id=opponent2.id, round_number=round_number))
        db.session.commit()
    
    def getNewRound(self):
        if len(self.tournament.duals) == 0:
            self.__generateSchedule()
            self.tournament.max_rounds = len(self.tournament.rounds)

        self.tournament.current_round_number += 1
        db.session.commit()


class SwissRS(RoundStrategy):
    

    def saveRound(self, round, round_number):
        newRundId = self.createNewRound(round_number)
        for duel in round:
            db.session.add(Dual(tournament_id=self.tournament.id, round_id=newRundId, opponent1_id=duel[0].id,
                            opponent2_id=duel[1].id, round_number=1))
        db.session.commit()

   


    def GenerateFirstRound(self):
        firstRound = GenerateFirstRoundSwiss(self.tournament.opponents)
        self.saveRound(firstRound,1)


    def getNewRound(self):
        self.tournament.current_round_number += 1
        db.session.commit()
        if len(self.tournament.duals) == 0:
            self.GenerateFirstRound()
            self.tournament.max_rounds = 5
        else:
            if checkIfScoresAreWritten(self.tournament.duals):
                newRound = GenerateRoundSwiss(
                    self.tournament.duals, self.tournament.standings)
                self.saveRound(newRound, self.tournament.current_round_number)
            else:
                return "Your have to fill all scores"


class TreeRS(RoundStrategy):
    

    def firstRound(self, duels):
        potegaWiekszej = math.floor(math.log2(len(duels)))
        potegaDwojki = pow(2, potegaWiekszej)
        liczbaDuelsWPierwszej = len(duels) - potegaDwojki
        return self.getNewRound(duels, liczbaDuelsWPierwszej)

    def getNewRound(self):
        self.tournament.current_round_number += 1
        db.session.commit()
        if len(self.tournament.duals) == 0:
            self.GenerateFirstRound()
            
            if checkIfScoresAreWritten(self.tournament.duals):
                if checkIfScoresAreDecided(self.tournament.duals):
                    newRound = GenerateRoundTree(self.tournament.duals)
                    self.saveRound(newRound, self.tournament.current_round_number)
                else:
                    return "None of the scores can be tied"
            else:
                return "Your have to fill all scores"
        
       