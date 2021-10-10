from flask import Blueprint, render_template, request, flash, jsonify
import flask
from flask.helpers import url_for
from flask.json import jsonify
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import query, session
from sqlalchemy.sql.expression import true
from werkzeug.utils import redirect
from .models import Opponent, User, Tournament, Dual, Opponent, Standing
from .import db
import json
from .TournamentsFunctions import *
from .Classes import *
from datetime import datetime

from website import TournamentsFunctions

from website import Classes

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

@views.route('/new-tournament', methods=['GET', 'POST'])
@login_required
def getScheduleInfo():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        location = request.form.get('location')
        discipline = request.form.get('discipline')
        type = request.form.get('type')

        if len(name) < 3:
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

            newTournament = TournamentController()
            id = newTournament.CreateNew(
                current_user.id, name, date, location, discipline, type)
            current_user.current_tournament_id = id
            newTournament.Save()

            return redirect(url_for('views.getPlayers'))
    return render_template("new_tournament.html", user=current_user)


@views.route('/new-players', methods=['GET', 'POST'])
@login_required
def getPlayers():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    partizipantsNumberLimit = 100
    if request.method == 'POST':
        if len(tournamentDTO.tournament.opponents) > partizipantsNumberLimit:
            flash(
                f'Too many players. Max: {partizipantsNumberLimit}', category='error')
        newPlayerName = request.form.get('player')
        if len(newPlayerName) < 1:
            flash('Name to short', category='error')
        elif Opponent.query.filter_by(name=newPlayerName, tournament_id=current_user.current_tournament_id).first():
            flash('Player already added', category='error')
        else:
            tournamentDTO.UploadPlayer(newPlayerName)
            tournamentDTO.Save()

            flash('Uczestnik dodany!', category='success')
    return render_template("new_players.html", user=current_user, tournament=tournamentDTO.tournament)

@views.route('generate-new-round', methods=['GET', 'POST'])
def generateNewRound():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)

    tournamentDTO.PrepareNewRound()
    tournamentDTO.Save()

    return redirect(url_for("views.schedule"))

@views.route('/set-tournament-id', methods=['POST', 'GET'])      
@login_required
def setTournamentId():
    tournament = json.loads(request.data)
    tournamentId = tournament['tournamentId']
    if tournamentId:
        current_user.current_tournament_id = tournamentId      
        db.session.commit()
        return jsonify({})

@views.route('/schedule')
@login_required
def schedule():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)

    return render_template("schedule.html", user=current_user, tournament=tournamentDTO.tournament)

@views.route('/get-dual-id',methods=['POST', 'GET'])
@login_required
def change_current_dual():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)

    dualId = json.loads(request.data)
    dualId = dualId['dualId']
    
    if dualId:
        tournamentDTO.ChangeEditedDual(dualId)
        tournamentDTO.Save()
    
    return jsonify({})
    
@views.route('update-dual', methods=['POST', 'GET'])
@login_required
def update_dual():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    dual = tournamentDTO.GetChangedDual()

    if request.method == 'POST':
        score_1 = request.form.get('score1')
        score_2 = request.form.get('score2')
        if score_1 == '' or score_2 == '':
            flash('Score cannot be empty',category='error')
 
        else:
            dual.score_1, dual.score_2 = int(score_1),int(score_2)
            tournamentDTO.Save()
            tournamentDTO.DeleteStanding()
            tournamentDTO.PrepareStanding()
            tournamentDTO.Save()
            return redirect(url_for("views.schedule"))
    return render_template("update_dual.html", user=current_user,dual=dual)

@views.route('reset-dual', methods=['POST', 'GET'])
@login_required
def reset_dual():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    dual = tournamentDTO.GetChangedDual()

    dual.score_1 = None
    dual.score_2 = None

    tournamentDTO.Save()
    tournamentDTO.DeleteStanding()
    tournamentDTO.PrepareStanding()
    tournamentDTO.Save()

    return redirect(url_for("views.schedule"))


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
        id=current_user.current_tournament_id).first()
    tournament.is_public = True
    db.session.commit()

    return redirect(url_for("views.public_schedule"))

# Standings Functions
@views.route('/standings')
@login_required
def show_standings():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    return render_template("standing.html", user=current_user, standings=tournamentDTO.ShowStanding(), tournament=tournamentDTO)

@views.route('/public-standings')
@login_required
def show_public_standings():
    tournamentDTO = ChessTournament()
    tournamentDTO.Load(current_user.current_tournament_id)
    tournament = Tournament.query.filter_by(is_public=True).first()
    return render_template("standing.html", user=current_user, standings=tournament.standings, tournament=tournamentDTO)

@views.route('/delete-tournament', methods=['POST', 'GET'])
@login_required
def delete_tournament():
    tournament = json.loads(request.data)
    tournamentId = tournament['tournamentId']
    
    tournamentDTO = TournamentController()
    tournamentDTO.Load(tournamentId)
    
    if tournamentDTO.tournament:
        if tournamentDTO.tournament.user_id == current_user.id:
            current_user.actual_tournament_id = current_user.tournaments[0].id
            tournamentDTO.DeleteTournament()
            tournamentDTO.Save()
            
    return jsonify({})

@views.route('/delete-player', methods=['POST'])
@login_required
def delete_player():
    player = json.loads(request.data)
    playerId = player['playerId']
    player = Opponent.query.get(playerId)
    if player:
        if player.tournament_id == current_user.current_tournament_id:
            db.session.delete(player)
            db.session.commit()
    return jsonify({})


#archived functions - maybe used someday


# @views.route('/new-schedule',methods = ['POST','GET'])
# @login_required
# def newSchedule():
#     newTournament = getScheduleInfo()
#     db.session.add(newTournament)
#     db.session.commit()
#     current_user.current_tournament_id = newTournament.id
#     db.session.commit()
#     return redirect(url_for("views.GetPlayers"))

# @views.route('/edit-schedule',methods = ['POST','GET'])
# @login_required
# def editSchedule():
#     tournament = Tournament.query.filter_by(id=current_user.current_tournament_id).first()
#     newTournament = redirect(url_for('views.getScheduleInfo'))
#     tournament.name = newTournament.name
#     tournament.date = newTournament.date
#     tournament.location = newTournament.location
#     tournament.discipline = newTournament.discipline
#     tournament.type = newTournament.type
#     db.session.commit()
#     return redirect(url_for('views.schedule'))


# @views.route('/top-scorers')
# @login_required
# def show_top_scorers():
#     tournament = Tournament.query.filter_by(
#         id=current_user.current_tournament_id).first()
#     opponents = db.session.query(Opponent).filter(Opponent.tournament_id.like(tournament.id),Opponent.points_scored > 0).order_by(Standing.match_points.desc())
#     return render_template("top_scorers.html", user=current_user, opponents=opponents)

# @views.route('/get-scorers',methods = ['GET','POST'])
# @login_required
# def get_scorers():
#     if request.method == ['POST']:
#         name = request.form.get('name')
#         goals = request.form.get('goals')
#         player = Opponent.query.filter_by(tournament_id=current_user.current_tournament_id,name=name).first()
#         if not player:
#             flash('Player not found',category='error')
#         else:
#             player.goals_scored += goals
#             db.session.commit()
#             flash("Player's goals updated",category='success')
#             return redirect(url_for("views.show_top_scorers"))
#     return render_template("get-scorers.html",user=current_user)

# Delete Functions