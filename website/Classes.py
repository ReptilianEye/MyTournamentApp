import re
from .TournamentsFunctions import *
from .import db
from .models import Opponent, User, Tournament, Dual, Opponent, Standing, Round


class TournamentController():

    def CreateNew(self, user_Id, name, date, location, discipline, type):
        self.tournament = Tournament(user_id=user_Id, name=name,
                                     date=date, location=location, discipline=discipline, type=type)
        db.session.add(self.tournament)
        db.session.commit()
        return self.tournament.id

    def Load(self, id):
        self.tournament = Tournament.query.filter_by(id=id).first()

    def Save(self):  # self is always required as a argument
        db.session.commit()

    def UploadPlayer(self, opponent):
        db.session.add(
            Opponent(tournament_id=self.tournament.id, name=opponent))
    
    def ChangeEditedDual(self,dual_id):
        self.tournament.edited_dual_id = dual_id
    
    def GetChangedDual(self):
        return Dual.query.filter_by(id = self.tournament.edited_dual_id).first()

    def UpdateScores(self,score1,score2):
        dual = Dual.query.filter_by(id=self.tournament.edited_dual_id).first()
        dual.score1 = score1
        dual.score2 = score2

    def DeleteTournament(self):
        pass


    tournamentTypes = ['RoundRobin', '2Teams']
    def PrepareNewRound(self):
        if self.tournament.type == self.tournamentTypes[0]:
            return RoundRobinRS(self.tournament).getNewRound()

    def PrepareStanding(self):
        standing = generateStandings(self.tournament.duals)
        for opponent in standing:
            db.session.add(Standing(tournament_id=self.tournament.id, opponent_id=opponent.id,
                                    wins=opponent.wins, loses=opponent.loses, match_points=opponent.wins*self.multipleForWin+opponent.loses*self.multipleForLose+opponent.draws*self.multipleForDraw))

    def ShowStanding(self):
        if len(self.tournament.standings) == 0:
            self.PrepareStanding()
        return self.tournament.standings

    def DeleteStanding(self):
        for standing in self.tournament.standings:
            db.session.delete(standing)
        self.Save()

    def DeleteTournament(self):
        pass


class ChessTournament(TournamentController):
    multipleForWin = 1
    multipleForLose = 0
    multipleForDraw = 0.5
    def PrepareStanding(self):
        pass


class BasketballStanding(TournamentController):
    multipleForWin = 2
    multipleForLose = 1
    multipleForDraw = 1
    def PrepareStanding(self):
            return super().PrepareStanding()


class FootballStanding(TournamentController):
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
        db.session.commit()  # TODO czy da sie to zrobic lepiej - z funkcja Save()

        

    def getNewRound(self):
        if len(self.tournament.duals) == 0:
            self.__generateSchedule()
        
        self.tournament.current_round_number+=1
        db.session.commit()
    
