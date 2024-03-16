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
bp = Blueprint('TeamsBP', __name__)

#---------------------------------------------------------------------------------
# All routes for Teams
#---------------------------------------------------------------------------------

@bp.route('/Teams/')
def teams():
    data = Teams.query.all()
    return render_template('Teams/Teams.html', headings = headings.TeamHeadings, data = data)

@bp.route('/TeamsAdd/')
def teamadd():
    data = Teams.query.all()
    Form = TeamRegister()
    return render_template('Teams/TeamAdd.html',form = Form, headings = headings.TeamHeadings, data = data)

#Team Del
@bp.route('/Teams/', methods=['POST'])
def teamdel():
    db.session.delete(Teams.query.get(request.form['id']))
    db.session.commit()
    data = Teams.query.all()
    return render_template('Teams/Teams.html', headings = headings.TeamHeadings, data = data)

@bp.route('/TeamsEdit/', methods=['POST'])
def teamedit():
    temp = Teams.query.get(request.form['id'])
    return render_template('Teams/TeamEdit.html', data = temp)

#Team Edit
@bp.route('/TeamsChanged/', methods=['POST'])
def teamchanged():
    temp = Teams.query.filter_by(id=request.form['id']).first()
    BASE_PATH = os.path.dirname(__file__)
    temp.name = request.form['Name']
    temp.abbreviation = request.form['Abbreviation']
    temp.description = request.form['Description']
    temp.colour = request.form['Colour']
    temp.logoBlue = request.files['LogoBlue'].filename
    temp.logoRed = request.files['LogoRed'].filename
    if request.files['LogoBlue'].filename != "":
        LogoBlue = request.files['LogoBlue']
        LogoBlue.save(os.path.join(BASE_PATH, '..\static\logos', secure_filename(LogoBlue.filename)))
    if request.files['LogoRed'].filename != "":
        LogoRed = request.files['LogoRed']
        LogoRed.save(os.path.join(BASE_PATH, '..\static\logos', secure_filename(LogoRed.filename)))
    db.session.commit()
    return teams()
