from os import urandom
from flask import Blueprint, render_template, request, flash, jsonify
from flask.helpers import url_for
from flask.json import jsonify
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import query, session
from sqlalchemy.sql.expression import true
from werkzeug.utils import redirect
from .models import User, Tournament, Dual, Player, Standing
from . import db
import json
from .GenerujeRoundRobinTournamentFlask import *

# blueprint - miejsce gdzie jest wiele stron

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/tournaments', methods=['GET', 'POST'])
@login_required
def Schedules():
    return render_template("tournaments.html", user=current_user)



@views.route('/new-schedule', methods=['GET', 'POST'])
@login_required
def CreateNewSchedule():
    if request.method == 'POST':
        tournamentName = request.form.get('name')
        date = request.form.get('date')
        location = request.form.get('location')
        discipline = request.form.get('discipline')
        type = request.form.get('type')

        newTournament = Tournament(user_id=current_user.id, name=tournamentName,
                                   date=date, location=location, discipline=discipline, type=type)
        db.session.add(newTournament)
        db.session.commit()
        current_user.actual_tournament_id = newTournament.id
        db.session.commit()
        return redirect(url_for("views.GetPlayers"))
    return render_template("new_schedule.html", user=current_user)

# TODO zrobic limit dodawania zawodnikow (aby ktos nie zrobil turnieju na niskonczona ilosc osob)
@views.route('/new-players', methods=['GET', 'POST'])
@login_required
def GetPlayers():
    partizipantsNumberLimit = 100
    tournament = Tournament.query.filter_by(id=current_user.actual_tournament_id).first()
    if request.method == 'POST':
        if len(tournament.players) > partizipantsNumberLimit:
            flash(f'Limit uczestnikow wykorzystany. Limit: {partizipantsNumberLimit}', category='error')
        newPlayerName = request.form.get('player')
        if len(newPlayerName) < 1:
            flash('Imie uczestnika za krotkie', category='error')
        else:
            newPlayer = Player(tournament_id=tournament.id, name=newPlayerName)
            db.session.add(newPlayer)
            db.session.commit()
            flash('Uczestnik dodany!', category='success')
    return render_template("new_players.html",user=current_user, tournament=tournament)

@views.route('generate-new-schedule')
def GenerateSchedule():
    tournament = Tournament.query.filter_by(id=current_user.actual_tournament_id).first()
    players = Player.query.filter_by(tournament_id=tournament.id).all()
    Schedule = WygenerujTermiarz(players)
    round_number = 0
    for line in Schedule:
        if type(line) == int:
            round_number = line
        else:
            player1_name = line[0]
            player2_name = line[1]

            player1 = Player.query.filter_by(name=player1_name).first()
            player2 = Player.query.filter_by(name=player2_name).first()

            newDual = Dual(tournament_id=tournament.id, player1_id=player1.id,
                           player2_id=player2.id, round_number=round_number)

            db.session.add(newDual)
            db.session.commit()

    return redirect(url_for("views.Schedule"))
    
@views.route('/show-schedule',methods=['POST','GET'])
@login_required
def showSchedule():
    tournament = json.loads(request.data)
    tournamentId = tournament['tournamentId']
    if tournamentId:
        current_user.actual_tournament_id = tournamentId
        db.session.commit() 
    return redirect(url_for("views.Schedule"))



@views.route('/schedule')
@login_required
def Schedule():
    tournament = Tournament.query.filter_by(id=current_user.actual_tournament_id).first()
    return render_template("schedule.html", user=current_user,tournament=tournament)

@views.route('update-schedule')
@login_required
def update_schedule():
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
    return render_template("update_schedule.html")


@views.route('public-schedule')
@login_required
def public_schedule():
    tournament = Tournament.query.filter_by(is_public=True).first()
    if tournament:
        return render_template("public_schedule.html", tournament=tournament, user=current_user)
    else:
        flash('Unfortunately, there is no public shedule. Probably new is incoming...!', category='error')
        return redirect(url_for("views.home"))


@views.route('publish-schedule')
@login_required
def publish_schedule():

    prevPublicTournament = Tournament.query.filter_by(is_public=True).first()

    if prevPublicTournament:
        prevPublicTournament.is_public = False
        db.session.commit()

    tournament = Tournament.query.filter_by(id=current_user.actual_tournament_id).first()
    tournament.is_public = True
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
    return render_template("generator.html", user=current_user)


@views.route('/delete-player', methods=['POST'])
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
