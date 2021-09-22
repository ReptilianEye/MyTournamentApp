from flask import Blueprint,render_template, request, flash, jsonify
from flask.helpers import url_for
from flask.json import jsonify
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import query, session
from sqlalchemy.sql.expression import true
from werkzeug.utils import redirect
from .models import Participant,Duo, Player, Round, User
from . import db
import json
from .GenerujeRoundRobinTournamentFlask import *

#blueprint - miejsce gdzie jest wiele stron

views = Blueprint('views', __name__)

@views.route('/',methods = ['GET','POST'])
@login_required
def home():

    return render_template("home.html",user=current_user)



# TODO zrobic limit dodawania zawodnikow (aby ktos nie zrobil turnieju na niskonczona ilosc osob)
@views.route('/generator',methods = ['GET','POST'])
@login_required
def GetPlayers():
    if request.method == 'POST':
        name = request.form.get('name')
        if len(name) < 1:
            flash('Imie uczestnika za krotkie', category='error')
        else:
            newPlayer = Player(name=name,user_id = current_user.id)
            db.session.add(newPlayer)
            db.session.commit()
            flash('Uczestnik dodany!',category='success')

    return render_template("generator.html",user=current_user)

@views.route('/generate')
@login_required
def Generuje():
    delete_schedule()
    uczestnicy = Player.query.filter_by(user_id=current_user.id).all()
    Terminarz = WygenerujTermiarz(uczestnicy)
    for duo in Terminarz:
        
        newRound = Round(user_id=current_user.id)
        db.session.add(newRound)
        db.session.commit()
        
        round_id = newRound.id

        newDuo = Duo(round_id=round_id)
        db.session.add(newDuo)
        db.session.commit()

        
        duo_id = newDuo.id
        for participant in duo:
            newPartcip = Participant(name=participant,score=0,duo_id=duo_id)
            db.session.add(newPartcip)
            db.session.commit()

    
    return redirect(url_for("views.Schedule"))

@views.route('/schedule', methods = ['GET','POST'])
@login_required
def Schedule():
    
    if request.method == 'POST':
        scores = request.form.getlist('wynik')
        for i in range(len(scores)):
            if scores[i] != '':
                scores[i] = int(scores[i])

        i = 0
        for round in current_user.rounds:
            for duo in round.duos:
                for particip in duo.participants:
                    if type(scores[i]) is int:
                        particip.score = scores[i]
                        db.session.commit()
                    i += 1


    return render_template("schedule.html",user=current_user)


@views.route('public-schedule')
@login_required
def public_schedule():
    Schedule = Round.query.filter_by(public=True).all()
    return render_template("public_schedule.html",Schedule=Schedule,user=current_user)

@views.route('publish-schedule')
@login_required
def publish_schedule():
    
    prevSchedule = Round.query.filter_by(public=True).all()
   
    for prev in prevSchedule:
        prev.public = False
        db.session.commit()

    for round in current_user.rounds:
        round.public = True
        db.session.commit()
    
    return redirect(url_for("views.public_schedule"))

@views.route('/delete-schedule')
@login_required
def delete_schedule():
    for round in current_user.rounds:
        for duo in round.duos:
            db.session.delete(duo)
        db.session.delete(round)
    db.session.commit()
    return render_template("generator.html",user=current_user)

@views.route('/delete-player',methods = ['POST'])
@login_required
def delete_player():
    player = json.loads(request.data)
    playerId = player['playerId']
    player = Player.query.get(playerId)
    if player:
        if player.user_id == current_user.id:
            db.session.delete(player)
            db.session.commit()
    return jsonify({})


