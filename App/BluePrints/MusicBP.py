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
bp = Blueprint('MusicBP', __name__)

@bp.route('/Music/')
def music():
    data = Music.query.all()
    return render_template('Music/Music.html', headings = headings.MusicHeadings, data = data)

@bp.route('/MusicAdd/')
def musicadd():
    data = Music.query.all()
    Form = MusicUpload()
    return render_template('Music/MusicAdd.html', form = Form, headings = headings.MusicHeadings, data = data)

#Music Del
@bp.route('/Music/', methods=['POST'])
def musicdel():
    db.session.delete(Music.query.get(request.form['id']))
    db.session.commit()
    data = Music.query.all()
    return render_template('Music/Music.html', headings = headings.MusicHeadings, data = data)

@bp.route('/MusicEdit/', methods=['POST'])
def musicedit():
    Musictemp = Music.query.get(request.form['id'])
    return render_template('Music/MusicEdit.html', data = Musictemp)

#Music Edit
@bp.route('/MusicChanged/', methods=['POST'])
def musicchanged():
    temp = Music.query.filter_by(id=request.form['id']).first()
    temp.title = request.form['Title']
    temp.author = request.form['Author']
    if request.form['Audio'] != "":
        temp.audio = request.form['Audio']
    db.session.commit()
    return music()
