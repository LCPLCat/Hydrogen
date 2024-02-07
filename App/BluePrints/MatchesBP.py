from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from ..forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey
from ..models import Item, Music, Teams, Casters, Players, Match, ROLFFile
from .. import db
from ..Streams import Stream, Headings
from ..replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from ..Streams import Stream, Headings
import os
headings = Headings
bp = Blueprint('MatchesBP', __name__)

@bp.route('/Matches/')
def match():
    data = Match.query.all()
    teams = Teams.query.all()
    return render_template('Matches/Matches.html', headings = headings.MatchHeadings, data = data,teams=teams)

@bp.route('/Matches/Add')
def matchadd():
    data = Match.query.all()
    teams = Teams.query.all()
    return render_template('Matches/MatchAdd.html', data = data, teams=teams)

@bp.route('/Matches/Edit', methods=['POST'])
def matchsave():
    data = Match.query.filter_by(id=request.form['id']).first()
    teams = Teams.query.all()
    return render_template('Matches/MatchEdit.html', matches = data, teams=teams)

@bp.route('/Matches/Decide', methods=['POST'])
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
    return match()

@bp.route('/Matches/Swap', methods=['POST'])
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
    return match()

#Matches Del
@bp.route('/Matches/', methods=['POST'])
def matchdel():
    db.session.delete(Match.query.get(request.form['id']))
    db.session.commit()
    data = Match.query.get(request.form['id'])
    teams = Teams.query.all()
    return match()

@bp.route('/MatchChanged/', methods=['POST'])
def matchchanged():
    temp = Match.query.filter_by(id=request.form['id']).first()
    print(request.form['id'])
    temp.team1 = request.form['Team1']
    temp.team2 = request.form['Team2']
    temp.time = request.form['Time']
    temp.format = request.form['Format']
    db.session.commit()
    return match()