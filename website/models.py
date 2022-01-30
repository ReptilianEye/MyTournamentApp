from . import db  # importuje zmienna 'db'
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    # 150 is maxLenght of string
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    # picture = db.Column(db.Text, nullable=False)

    is_admin = db.Column(db.Boolean, default=False)

    current_tournament_id = db.Column(db.Integer)

    tournaments = db.relationship('Tournament')


class Tournament(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    name = db.Column(db.String(150))
    date = db.Column(db.Date)
    location = db.Column(db.String(150))
    discipline = db.Column(db.String(150))    
    type = db.Column(db.String(150))
    description = db.Column(db.String(250))
    movielink = db.Column(db.String(150),default="")

    status = db.Column(db.String(150), default="upcoming")
    is_public = db.Column(db.Boolean(),default=False)
    current_round_number = db.Column(db.Integer(),default=0)
    max_rounds = db.Column(db.Integer(),default = 100000000)
    max_opponents = db.Column(db.Integer(),default = 100)

    edited_duel_id = db.Column(db.Integer())

    rounds = db.relationship('Round')
    duels = db.relationship('Duel')
    opponents = db.relationship('Opponent')
    standings = db.relationship('Standing')

class Opponent(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    # team_id = db.Column(db.Integer,db.ForeignKey('team.id'))
    email = db.Column(db.String(150))       

    standing = db.relationship('Standing') 
    name = db.Column(db.String(100000))
    # points_scored = db.Column(db.Integer,default=0)

    
class Round(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    number = db.Column(db.Integer)
    
    duels = db.relationship('Duel')
    
class Duel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    round_id = db.Column(db.Integer,db.ForeignKey('round.id'))

    opponent1_id = db.Column(db.Integer,db.ForeignKey('opponent.id'))
    opponent2_id = db.Column(db.Integer,db.ForeignKey('opponent.id'))
    
    opponent_1 = db.relationship('Opponent', foreign_keys=[opponent1_id])  
    opponent_2 = db.relationship('Opponent', foreign_keys=[opponent2_id])  

    score_1 = db.Column(db.Integer)
    score_2 = db.Column(db.Integer)

    date = db.Column(db.DateTime)


    round_number = db.Column(db.Integer)



class Standing(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    opponent_id = db.Column(db.Integer,db.ForeignKey('opponent.id'))
    opponent = db.relationship('Opponent', foreign_keys=[opponent_id])  


    match_points = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    loses = db.Column(db.Integer)
    draws = db.Column(db.Integer)


    



