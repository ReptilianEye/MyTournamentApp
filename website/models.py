from . import db    #importuje zmienna 'db'
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String(150))
    email = db.Column(db.String(150),unique=True)       #150 is maxLenght of string
    password = db.Column(db.String(150))

    is_admin = db.Column(db.Boolean,default=False) 
    
    actual_tournament_id = db.Column(db.Integer)

    tournaments = db.relationship('Tournament')  


class Tournament(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    name = db.Column(db.String(150))
    date = db.Column(db.Date)
    location = db.Column(db.String(150))
    discipline = db.Column(db.String(150))    
    type = db.Column(db.String(150))

    status = db.Column(db.String(150), default="upcoming")
    is_public = db.Column(db.Boolean(),default=False)

    duals = db.relationship('Dual')
    players = db.relationship('Player')
    teams = db.relationship('Team')
    standings = db.relationship('Standing')


class Team(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    
    name = db.Column(db.String(100000))
    
    players = db.relationship('Player')
    standing = db.relationship('Standing') 



class Player(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    team_id = db.Column(db.Integer,db.ForeignKey('team.id'))
    
    name = db.Column(db.String(100000))
    points_scored = db.Column(db.Integer,default=0)

    


class Dual(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    
    team1_id = db.Column(db.Integer,db.ForeignKey('team.id'))
    team2_id = db.Column(db.Integer,db.ForeignKey('team.id'))
    
    team_1 = db.relationship('Team', foreign_keys=[team1_id])  
    team_2 = db.relationship('Team', foreign_keys=[team2_id])  

    score_1 = db.Column(db.Integer,default=0)
    score_2 = db.Column(db.Integer,default=0)

    date = db.Column(db.Datetime)


    round_number = db.Column(db.Integer)



class Standing(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    team_id = db.Column(db.Integer,db.ForeignKey('team.id'))
    team = db.relationship('Team', foreign_keys=[team_id])  


    match_points = db.Column(db.Integer)
    wins = db.Column(db.Integer)
    loses = db.Column(db.Integer)
    draws = db.Column(db.Integer)


    



