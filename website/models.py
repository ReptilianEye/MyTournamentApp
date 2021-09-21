from . import db    #importuje zmienna 'db'
from flask_login import UserMixin
from sqlalchemy.sql import func




class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)       #150 is maxLenght of string
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    is_admin = db.Column(db.Boolean,default=False) 

    tournaments = db.relationship('Tournament')  


class Tournament(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    
    name = db.Column(db.String(150))
    date = db.Column(db.Date)
    location = db.Column(db.String(150))
    status = db.Column(db.String(150))
    discipline = db.Column(db.String(150))
    type = db.Column(db.String(150))

    players = db.relationship('Player')

class Player(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))

    name = db.Column(db.String(100000))
    email = db.Column(db.String(150),unique=True)   

    standing = db.relationship('Standing') 
    


class Dual(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    
    player1_id = db.Column(db.Integer,db.ForeignKey('player.id'))
    player2_id = db.Column(db.Integer,db.ForeignKey('player.id'))
    
    player1 = db.relationship('Player', foreign_keys=[player1_id])
    player2 = db.relationship('Player', foreign_keys=[player2_id])

    score_1 = db.Column(db.Integer,default=0)
    score_2 = db.Column(db.Integer,default=0)

    round_number = db.Column(db.Integer)



class Standing(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    tournament_id = db.Column(db.Integer,db.ForeignKey('tournament.id'))
    player_id = db.Column(db.Integer,db.ForeignKey('player.id'))

    player_point = db.Column(db.Integer)
    matches_won = db.Column(db.Integer)
    matches_lost = db.Column(db.Integer)


    



