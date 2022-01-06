from flask import Blueprint, render_template, request, flash, jsonify
import flask
from flask.helpers import url_for
from flask.json import jsonify
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy.orm import query, session
from werkzeug.utils import redirect
from .models import Opponent, User, Tournament, Duel, Opponent, Standing
from .import db
import json
from .TournamentsFunctions import *
from .Classes import *
from datetime import datetime

# blueprint - miejsce gdzie jest wiele stron
views = Blueprint('views', __name__)

### main pages ###


@views.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html", user=current_user)


@views.route('/video', methods=['GET', 'POST'])
def video():
    tournaments = Tournament.query.filter_by(is_public=True).all()
    return render_template("video.html", user=current_user, tournaments=tournaments)


@views.route('/tournaments', methods=['GET', 'POST'])
@login_required
def tournaments():
    return render_template("tournaments.html", user=current_user)


@views.route('/public-tournaments', methods=['GET', 'POST'])
def public_tournaments():
    tournaments = Tournament.query.filter_by(is_public=True).all()
    return render_template("public_tournaments.html", user=current_user, tournaments=tournaments)


### tournament pages ###

@views.route('/new-tournament', methods=['GET', 'POST'])
@login_required
def get_tournament_info():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        location = request.form.get('location')
        discipline = request.form.get('discipline')
        type = request.form.get('type')

        if len(name) < 3:
            flash(f"Tournament's name is too short (at least 3 characters).",
                  category='error')
        elif not date:
            flash(f'Select date.', category='error')
        elif not location:
            flash(f"Type in tournament's location.", category='error')
        elif not discipline:
            flash(f"Type in tournament's discipline.", category='error')
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

            return redirect(url_for('views.schedule'))
    return render_template("new_tournament.html", user=current_user)


@views.route('/edit-tournament', methods=['GET', 'POST'])
@login_required
def edit_tournament():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        location = request.form.get('location')
        discipline = request.form.get('discipline')
        status = request.form.get('status')
        movielink = request.form.get('movielink')

        tournamentDTO.EditTournament(
            name, date, location, discipline, status, movielink)

        return redirect(url_for('views.tournaments'))
    return render_template("edit_tournament.html", user=current_user, tournament=tournamentDTO.tournament)


@views.route('/new-players', methods=['GET', 'POST'])
@login_required
def get_players_manually():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    partizipantsNumberLimit = 100
    if request.method == 'POST':
        if len(tournamentDTO.tournament.opponents) > partizipantsNumberLimit:
            flash(
                f'Too many participants. Max: {partizipantsNumberLimit}', category='error')
        newPlayerName = request.form.get('player')
        if len(newPlayerName) < 1:
            flash('The name is too short! D:', category='error')
        elif Opponent.query.filter_by(name=newPlayerName, tournament_id=current_user.current_tournament_id).first():
            flash('Participant has been already added', category='error')
        else:
            tournamentDTO.UploadPlayer(newPlayerName)
            tournamentDTO.Save()

            flash('Participant has been added! :)', category='success')
    return render_template("new_players.html", user=current_user, tournament=tournamentDTO.tournament)


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


@views.route('/joined-tournaments', methods=['GET', 'POST'])
@login_required
def show_joined_tournaments():
    tournaments = Tournament.query.filter_by(is_public=True).all()
    i = 0
    n = len(tournaments)
    while i < n:
        if not checkIfUserInTournaments(current_user, tournaments[i]):
            tournaments.remove(tournaments[i])
            n -= 1
        else:
            i += 1
    return render_template("my_public_tournaments.html", user=current_user, tournaments=tournaments)


@views.route('/joined-schedule', methods=['GET', 'POST'])
@login_required
def show_joined_schedule():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    return render_template("my_public_schedule.html", user=current_user, tournament=tournamentDTO.tournament)


@views.route('/schedule')
@login_required
def schedule():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    return render_template("schedule.html", user=current_user, tournament=tournamentDTO.tournament)

@views.route('/start-tournament')
@login_required
def start_tournament():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    if len(tournamentDTO.tournament.opponents) < 2:
        flash('You cannot start tournament that have less than 2 players',category='error')
    else:
        tournamentDTO.Start()
    return redirect(url_for('views.schedule'))

@views.route('/end-tournament')
@login_required
def end_tournament():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    if tournamentDTO.CheckIfScoresAreWritten():
        tournamentDTO.End()
        flash('You successfully ended your tournament',category='success')
        return redirect(url_for('views.show_standings'))
    else:
        flash('You have to fill all the scores, first',category='error')
        return redirect(url_for('views.schedule'))

def reset_tournament():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    tournamentDTO.Reset()
    

@views.route('public-schedule')
def public_schedule():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(temporatyId)

    return render_template("public_schedule.html", user=current_user, tournament=tournamentDTO.tournament)

@views.route('/publish-tournament')
@login_required
def publish_tournament():
    if current_user.is_admin:
        tournamentDTO = TournamentController()
        tournamentDTO.Load(current_user.current_tournament_id)
        tournamentDTO.Publish()
        flash('You successfully published tournament! You can find it now in Public Tournaments',category='success')    
    else:
        flash('You do not have permission to publish tournament. You have to be an admin. Ask another admin how you can get a permission.')
    return redirect(url_for("views.schedule"))


@views.route('/join-tournament', methods=['GET', 'POST'])
@login_required
def join_tournament():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(temporatyId)

    result = tournamentDTO.JoinToTheTournament(current_user)
    if result:
        flash("You have sucessfully joined to the tournament")
        return redirect(url_for("views.show_joined_tournaments"))
    else:
        flash("You have already joined that tournament")
        return redirect(url_for("views.public_schedule"))


@views.route('/set-tournament-id', methods=['POST', 'GET'])
@login_required
def set_tournament_ID():
    tournament = json.loads(request.data)
    tournamentId = tournament['tournamentId']
    if tournamentId:
        current_user.current_tournament_id = tournamentId
        db.session.commit()
        return jsonify({})


temporatyId = -1


@views.route('/set-temp-tournament-id', methods=['POST', 'GET'])
# @login_required
def set_temp_tournament_ID():
    global temporatyId
    tournament = json.loads(request.data)
    tournamentId = tournament['tournamentId']
    if tournamentId:
        temporatyId = tournamentId
        return jsonify({})


@views.route('/quit-tournament', methods=['POST', 'GET'])
@login_required
def quit_tournament():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    tournamentDTO.Quit(current_user)
    return redirect(url_for("views.show_joined_tournaments"))


@views.route('/delete-tournament', methods=['POST', 'GET'])
@login_required
def delete_tournament():
    tournament = json.loads(request.data)
    tournamentId = tournament['tournamentId']

    tournamentDTO = TournamentController()
    tournamentDTO.Load(tournamentId)

    if tournamentDTO.tournament:
        if tournamentDTO.tournament.user_id == current_user.id:
            current_user.current_tournament_id = current_user.tournaments[0].id
            tournamentDTO.DeleteTournament()
            tournamentDTO.Save()

    flash('Tournament has been deleted', category='success')
    return jsonify({})


### ROUNDS ###

@views.route('/generate-new-round', methods=['GET', 'POST'])
@login_required
def generate_new_round():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)

    result = tournamentDTO.PrepareNewRound()
    if result:
        flash(result, category="error")
    else:
        tournamentDTO.Save()

    return redirect(url_for("views.schedule"))


@views.route('/generate-all-rounds', methods=['GET', 'POST'])
@login_required
def generate_all_rounds():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    if tournamentDTO.tournament.type == 'RoundRobin':
        tournamentDTO.PrepareAllRound()
    return redirect(url_for("views.schedule"))
### DUELS ###

@views.route('/get-duel-id', methods=['POST', 'GET'])
@login_required
def change_current_duel():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)

    duelId = json.loads(request.data)
    duelId = duelId['duelId']

    if duelId:
        tournamentDTO.ChangeEditedDuel(duelId)
        tournamentDTO.Save()

    return jsonify({})


@views.route('update-duel', methods=['POST', 'GET'])
@login_required
def update_duel():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    duel = tournamentDTO.GetChangedDuel()

    if request.method == 'POST':
        score_1 = request.form.get('score1')
        score_2 = request.form.get('score2')
        if score_1 == '' or score_2 == '':
            flash('Score cannot be empty', category='error')

        else:
            duel.score_1, duel.score_2 = int(score_1), int(score_2)
            tournamentDTO.Save()
            tournamentDTO.DeleteStanding()
            tournamentDTO.PrepareStanding()
            tournamentDTO.Save()
            return redirect(url_for("views.schedule"))
    return render_template("update_duel.html", user=current_user, duel=duel)


@views.route('reset-duel', methods=['POST', 'GET'])
@login_required
def reset_duel():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    duel = tournamentDTO.GetChangedDuel()

    duel.score_1 = None
    duel.score_2 = None

    tournamentDTO.Save()
    tournamentDTO.DeleteStanding()
    tournamentDTO.PrepareStanding()
    tournamentDTO.Save()

    return redirect(url_for("views.schedule"))


### STANDING ###

@views.route('/standings')
@login_required
def show_standings():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(current_user.current_tournament_id)
    return render_template("standing.html", user=current_user, standings=tournamentDTO.ShowStanding(), tournament=tournamentDTO)


@views.route('/public-standings')
# @login_required
def show_public_standings():
    tournamentDTO = TournamentController()
    tournamentDTO.Load(temporatyId)
    return render_template("standing.html", user=current_user, standings=tournamentDTO.ShowStanding(), tournament=tournamentDTO)
