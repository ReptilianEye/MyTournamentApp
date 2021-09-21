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


@views.route('/generator', methods=['GET', 'POST'])
@login_required
def Schedules():
    return render_template("tournaments.html", user=current_user)

# TODO zrobic limit dodawania zawodnikow (aby ktos nie zrobil turnieju na niskonczona ilosc osob)


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
    return render_template("new_schedule.html", user=current_user)


@views.route('/new-players', methods=['GET', 'POST'])
@login_required
def GetPlayers(Tournament):
    if request.method == 'POST':
        name = request.form.get('player')
        if len(name) < 1:
            flash('Imie uczestnika za krotkie', category='error')
        else:
            newPlayer = Player(tournament_id=Tournament.id, name=name)
            db.session.add(newPlayer)
            db.session.commit()
            flash('Uczestnik dodany!', category='success')
    return render_template("new_players.html", user=current_user)


def GenerateSchedule():

    tournament = Tournament.query.filter_by(user_id=current_user.id).last()
    players = Player.query.filter_by(tournament_id=tournament.id).all()
    Schedule = WygenerujTermiarz(players)
    round_number = 0
    for line in Schedule:
        if type(line) == int:
            round_number = line
        else:
            player1_name = line[0]
            player2_name = line[1]

            player1_id = Player.query.filter_by(name=player1_name).first()
            player2_id = Player.query.filter_by(name=player2_name).first()

            newDual = Dual(tournament_id=Tournament.id, player1_id=player1_id,
                           player2_id=player2_id, round_number=round_number)

            db.session.add(newDual)
            db.session.commit()

    return redirect(url_for("views.Schedule"))


@views.route('/schedule', methods=['GET', 'POST'])
@login_required
def Schedule():

    if request.method == 'POST':
        scores = request.form.getlist('score')
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

    return render_template("schedule.html", user=current_user)


@views.route('public-schedule')
@login_required
def public_schedule():
    Schedule = Round.query.filter_by(public=True).all()
    return render_template("public_schedule.html", Schedule=Schedule, user=current_user)


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
