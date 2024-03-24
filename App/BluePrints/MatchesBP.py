from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, jsonify
from ..forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey, MatchID
from ..models import Item, Music, Teams, Casters, Players, Match, ROLFFile, MatchStas, Tournment
from .. import db
from ..Streams import Stream, Headings
from ..DataBaseUtils import *
from ..replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from flask_login import login_required
from ..Streams import Stream, Headings
import os
from datetime import *
from . import RiotAPIBP
import sys
headings = Headings
bp = Blueprint('MatchesBP', __name__)
global PROVIDER
PROVIDER = os.environ['PROVIDER']
@bp.route('/Matches/')
@login_required
def match():
    time = datetime.now()
    matchs = Match.query.all()
    Form = MatchRegister()
    Form.Team1.choices = [(T.id, T.name+' | '+T.description) for T in Teams.query.order_by('id')]
    Form.Team2.choices = [(T.id, T.name+' | '+T.description) for T in Teams.query.order_by('id')]
    Form.Tournament.choices = [(T.id, T.tournementname) for T in Tournment.query.all()]
    args = ''
    if request.args.get('time') == 'hour':
        args = '?time=hour'
        time = time - timedelta(hours=10)
        data = Match.query.filter(Match.recorddate >= time)
    elif request.args.get('time') == 'week':
        args = '?time=week'
        time = time - timedelta(weeks=1)
        data = Match.query.filter(Match.recorddate >= time)
    elif request.args.get('time') == 'month':
        args = '?time=month'
        time = time - timedelta(weeks=4)
        data = Match.query.filter(Match.recorddate >= time)
    elif request.args.get('time') == 'all':
        args = '?time=all'
        data = Match.query.all()
    else:
        data = Match.query.all()
    tournaments = Tournment.query.all()
    Forms = []
    for i, match in enumerate(matchs):
        tempForm = MatchRegister(
                                Tournament=match.tournament,
                                Team1=match.team1,
                                Team2=match.team2,
                                Team1name=match.team1name,
                                Team2name=match.team2name,
                                Time=match.time,
                                Format=match.format)
        Forms.append(tempForm)
    teams = Teams.query.all()
    return render_template('Matches/Matches.html', headings = headings.MatchHeadings, data = data,teams=teams, form=Form, tournaments=tournaments, forms=Forms)

@bp.route('/Matches/Add')
@login_required
def matchadd():
    data = Match.query.all()
    Form = MatchRegister()
    Form.Team1.choices = [(T.id, T.name+' | '+T.description) for T in Teams.query.order_by('id')]
    Form.Team2.choices = [(T.id, T.name+' | '+T.description) for T in Teams.query.order_by('id')]
    Form.Tournament.choices = [(T.id, T.tournementname) for T in Tournment.query.all()]

    return render_template('Matches/MatchAdd.html', data = data, form=Form)

@bp.route('/Matches/Edit', methods=['POST'])
@login_required
def matchsave():
    data = Match.query.filter_by(id=request.form['id']).first()
    teams = Teams.query.all()
    return render_template('Matches/MatchEdit.html', matches = data, teams=teams)

@bp.route('/Matches/Decide', methods=['POST'])
@login_required
def matchdecide():
    data = Match.query.filter_by(id=request.form['id']).first()
    teams = Teams.query.all()
    return render_template('Matches/MatchDecide.html', match = data, teams=teams)

@bp.route('/Matches/Decided', methods=['POST'])
def matchdecide_submit():
    data = Match.query.filter_by(id=request.form['matchid']).first()
    winner = Teams.query.filter_by(id=request.form['winnerid']).first()
    loser = Teams.query.filter_by(id=request.form['loserid']).first()
    loser.losses = int(loser.losses) + 1
    winner.wins = int(winner.wins) + 1
    data.winner = winner.id
    data.loser = loser.id
    data.decided = 1
    db.session.commit()
    return redirect('/Matches/')

@bp.route('/Matches/Swap', methods=['POST'])
@login_required
def matchswap():
    data = Match.query.filter_by(id=request.form['matchid']).first()
    winner = Teams.query.filter_by(id=request.form['winnerid']).first()
    loser = Teams.query.filter_by(id=request.form['loserid']).first()
    loser.losses = int(loser.losses) - 1
    winner.wins = int(winner.wins) - 1
    loser.wins = int(loser.wins) + 1
    winner.losses = int(winner.losses) + 1
    data.loser = winner.id
    data.winner = loser.id
    db.session.commit()
    return redirect('/Matches/')

#Matches Del
@bp.route('/Matches/', methods=['POST'])
def matchdel():
    db.session.delete(Match.query.get(request.form['id']))
    db.session.commit()
    data = Match.query.get(request.form['id'])
    teams = Teams.query.all()
    return redirect('/Matches/')

@bp.route('/MatchChanged/', methods=['POST'])
def matchchanged():
    temp = Match.query.filter_by(id=request.form['id']).first()
    print(request.form['id'])
    temp.team1 = request.form['Team1']
    temp.team2 = request.form['Team2']
    temp.time = request.form['Time']
    temp.format = request.form['Format']
    db.session.commit()
    return redirect('/Matches/')

@bp.route('/MatchGetStats/', methods=['POST'])
@login_required
def matchgetstats():
    Form = MatchID()
    temp = Match.query.filter_by(id=request.form['id']).first()
    Form.Players.choices = [(T.id, T.name) for T in Players.query.filter_by(team=temp.team1)]
    #print(Form.Players.choices)
    return render_template('Matches/MatchGetStats.html', form=Form)


@bp.route('/StatsSubmit/', methods=['POST'])
def StatsSubmit():
    RiotAPIBP.GetMatchIDFromPlayer(Players.query.filter_by(id=request.form['Players']).first().name)
    return redirect('/Matches/')

@bp.route('/matchsubmit', methods=['GET','POST'])
@login_required
def matchsubmit():
    Codedata = {
        "enoughPlayers": request.form['enoughPlayers'],
        "mapType": request.form['mapType'],
        "pickType": request.form['pickType'],
        "spectatorType": request.form['spectatorType'],
        "teamSize": request.form['teamSize']
    }
    Tournmentid = Tournment.query.filter_by(id=request.form['Tournament']).first()
    response = requests.post('https://americas.api.riotgames.com/lol/tournament/v5/codes?count=1&tournamentId='+Tournmentid.tournementid+'&api_key='+RIOT_KEY, json=Codedata).json()
    add_match_to_database(MatchRegister(), response)
    return redirect('/Matches/')

@bp.route('/Match/Stats/Player',methods=['GET'])
def IndividualStats():
    res = MatchStas.query.filter_by(id2=request.args.get('player')).first()
    return render_template('Stats/PlayerStats.html', stats=res)