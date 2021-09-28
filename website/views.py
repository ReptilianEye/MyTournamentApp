from os import urandom
from flask import Blueprint, render_template, request, flash, jsonify
from flask.helpers import url_for
from flask.json import jsonify
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import query, session
from sqlalchemy.sql.expression import true
from werkzeug.utils import redirect
from .models import Player, User, Tournament, Dual, Player, Standing
from .import db
import json
from .TournamentsFunctions import *
from .AdditionalFunctions import PlayerInStanding
from datetime import datetime

# blueprint - miejsce gdzie jest wiele stron

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)


@views.route('/tournaments', methods=['GET', 'POST'])
@login_required
def tournaments():
    return render_template("tournaments.html", user=current_user)


# @views.route('/new-schedule',methods = ['POST','GET'])
# @login_required
# def newSchedule():
#     newTournament = getScheduleInfo()
#     db.session.add(newTournament)
#     db.session.commit()
#     current_user.actual_tournament_id = newTournament.id
#     db.session.commit()
#     return redirect(url_for("views.GetPlayers"))

# @views.route('/edit-schedule',methods = ['POST','GET'])
# @login_required
# def editSchedule():
#     tournament = Tournament.query.filter_by(id=current_user.actual_tournament_id).first()
#     newTournament = redirect(url_for('views.getScheduleInfo'))
#     tournament.name = newTournament.name
#     tournament.date = newTournament.date
#     tournament.location = newTournament.location
#     tournament.discipline = newTournament.discipline
#     tournament.type = newTournament.type
#     db.session.commit()
#     return redirect(url_for('views.schedule'))

@views.route('/new-schedule', methods=['GET', 'POST'])
@login_required
def getScheduleInfo():
    if request.method == 'POST':
        tournamentName = request.form.get('name')
        date = request.form.get('date')
        location = request.form.get('location')
        discipline = request.form.get('discipline')
        type = request.form.get('type')

        if len(tournamentName) < 3:
            flash(f'Tournaments name too short (at least 3 characters).',
                  category='error')
        elif not date:
            flash(f'Select date.', category='error')
        elif not location:
            flash(f'Type location.', category='error')
        elif not discipline:
            flash(f'Type discypline.', category='error')
        elif not type:
            flash(f'Select type.', category='error')
        else:
            y, m, d = date.split('-')
            date = datetime(int(y), int(m), int(d))
            newTournament = Tournament(user_id=current_user.id, name=tournamentName,
                                       date=date, location=location, discipline=discipline, type=type)
            db.session.add(newTournament)
            db.session.commit()
            current_user.actual_tournament_id = newTournament.id
            db.session.commit()
            return redirect(url_for('views.getPlayers'))
    return render_template("new_schedule.html", user=current_user)


@views.route('/new-players', methods=['GET', 'POST'])
@login_required
def getPlayers():
    partizipantsNumberLimit = 100
    tournament = Tournament.query.filter_by(
        id=current_user.actual_tournament_id).first()
    if request.method == 'POST':
        if len(tournament.players) > partizipantsNumberLimit:
            flash(
                f'Too many players. Max: {partizipantsNumberLimit}', category='error')
        newPlayerName = request.form.get('player')
        if len(newPlayerName) < 1:
            flash('Name to short', category='error')
        elif Player.query.filter_by(name=newPlayerName, tournament_id=current_user.actual_tournament_id).first():
            flash('Player already added', category='error')
        else:
            newPlayer = Player(tournament_id=tournament.id, name=newPlayerName)
            db.session.add(newPlayer)
            db.session.commit()
            flash('Uczestnik dodany!', category='success')
    return render_template("new_players.html", user=current_user, tournament=tournament)


@views.route('generate-new-schedule', methods=['GET', 'POST'])
def generateSchedule():
    tournament = Tournament.query.filter_by(
        id=current_user.actual_tournament_id).first()
    players = Player.query.filter_by(tournament_id=tournament.id).all()
    Schedule = WygenerujTermiarzRoundRobin(players)
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

    return redirect(url_for("views.schedule"))


@views.route('/show-tournament', methods=['POST', 'GET'])
@login_required
def showTournament():
    tournament = json.loads(request.data)
    tournamentId = tournament['tournamentId']
    if tournamentId:
        current_user.actual_tournament_id = tournamentId
        db.session.commit()
        return redirect(url_for("views.Schedule"))


@views.route('/schedule')
@login_required
def schedule():
    tournament = Tournament.query.filter_by(
        id=current_user.actual_tournament_id).first()
    return render_template("schedule.html", user=current_user, tournament=tournament)


@views.route('update-schedule', methods=['POST', 'GET'])
@login_required
def update_schedule():
    tournament = Tournament.query.filter_by(
        id=current_user.actual_tournament_id).first()
    if request.method == 'POST':
        scores = request.form.getlist('score')
        for i in range(len(scores)):
            if scores[i] != '':
                scores[i] = int(scores[i])

        i = 0
        for dual in tournament.duals:
            if type(scores[i]) is int:
                dual.score_1 = scores[i]
            i += 1
            if type(scores[i]) is int:
                dual.score_2 = scores[i]
                db.session.commit()
            i += 1
        delete_standing()
        prepareStandings(tournament)
        return redirect(url_for("views.schedule"))
    return render_template("update_schedule.html", user=current_user, tournament=tournament)


# Functions to pubish schedule
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

    tournament = Tournament.query.filter_by(
        id=current_user.actual_tournament_id).first()
    tournament.is_public = True
    db.session.commit()

    return redirect(url_for("views.public_schedule"))


# Standings Functions


@views.route('/standings')
@login_required
def show_standings():
    tournament = Tournament.query.filter_by(
        id=current_user.actual_tournament_id).first()
    if not tournament.standings:
        prepareStandings(tournament)
    standings = db.session.query(Standing).filter(Standing.tournament_id.like(tournament.id)).order_by(Standing.points.desc())
    return render_template("standing.html", user=current_user, standings=standings)

@views.route('/public-standings')
@login_required
def show_public_standings():
    tournament = Tournament.query.filter_by(
        is_public=True).first()
    if not tournament.standings:
        prepareStandings(tournament)
    standings = db.session.query(Standing).filter(Standing.tournament_id.like(tournament.id)).order_by(Standing.points.desc())
    return render_template("standing.html", user=current_user, standings=standings)



def prepareStandings(tournament):
    standings = generateStandings(tournament)
    for player in standings:
        newStanding = Standing(tournament_id=current_user.actual_tournament_id, player_id=player.id,
                               wins=player.wins, loses=player.loses, points=player.wins+player.draws*0.5)
        db.session.add(newStanding)
    db.session.commit()


def delete_standing():
    tournament = Tournament.query.filter_by(
        id=current_user.actual_tournament_id).first()
    for standing in tournament.standings:
        db.session.delete(standing)
    db.session.commit()


# Delete Functions

@views.route('/delete-tournament', methods=['POST', 'GET'])
@login_required
def delete_schedule():
    tournament = json.loads(request.data)
    tournamentId = tournament['tournamentId']
    tournament = Tournament.query.get(tournamentId)
    if tournament:
        if tournament.user_id == current_user.id:
            current_user.actual_tournament_id = current_user.tournaments[0].id
            for dual in tournament.duals:
                db.session.delete(dual)

            for player in tournament.players:
                db.session.delete(player)

            for standing in tournament.standings:
                db.session.delete(standing)

            db.session.delete(tournament)
            db.session.commit()
    return jsonify({})


@views.route('/delete-player', methods=['POST'])
@login_required
def delete_player():
    player = json.loads(request.data)
    playerId = player['playerId']
    player = Player.query.get(playerId)
    if player:
        if player.tournament_id == current_user.actual_tournament_id:
            db.session.delete(player)
            db.session.commit()
    return jsonify({})
