from . import db    #importuje zmienna 'db'
from flask_login import UserMixin
from sqlalchemy.sql import func

class Player(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100000))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(150),unique=True)       #150 is maxLenght of string
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))

    admin = db.Column(db.Boolean,default=False) #TODO zmienic na isAdmin - poniewaz boolean

    players = db.relationship('Player')  

    rounds = db.relationship('Round')    

class Participant(db.Model):
    id = db.Column(db.Integer,primary_key=True)

    name = db.Column(db.String(150))
    score = db.Column(db.Integer)

    duo_id = db.Column(db.Integer,db.ForeignKey('duo.id'))


class Duo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    
    participants = db.relationship('Participant')
    
    round_id = db.Column(db.Integer,db.ForeignKey('round.id'))


class Round(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    
    duos = db.relationship('Duo')
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    public = db.Column(db.Boolean,default=False)



