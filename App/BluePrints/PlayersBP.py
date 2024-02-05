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
bp = Blueprint('PlayersBP', __name__)

@bp.route('/Players/')
def players():
    data = Players.query.all()
    return render_template('Players/Players.html', headings = headings.PlayerHeadings, data = data)

@bp.route('/PlayersAdd/')
def playeradd():
    Form = PlayerRegister()
    data = Players.query.all()
    return render_template('Players/PlayersAdd.html', form = Form, data =data )

@bp.route('/PlayersEdit/', methods=['POST'])
def playeredit():
    temp = Players.query.get(request.form['id'])
    return render_template('Players/PlayersEdit.html', data = temp)

@bp.route('/PlayersChanged/', methods=['POST'])
def playerchanged():
    temp = Players.query.filter_by(id=request.form['id']).first()
    temp.name = request.form['Name']
    temp.team = request.form['Team']
    db.session.commit()
    return players()

#Players Del
@bp.route('/Players/', methods=['POST'])
def playerdel():
    db.session.delete(Players.query.get(request.form['id']))
    db.session.commit()
    data = Players.query.all()
    return render_template('Players/Players.html', headings = headings.PlayerHeadings, data = data)
