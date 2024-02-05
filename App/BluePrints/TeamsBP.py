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
    if request.files['LogoTXT'].filename != "":
        LogoTXT = request.files['LogoTXT']
        print(LogoTXT.filename)
        LogoTXT.save(os.path.join(BASE_PATH, 'static/logos', secure_filename(LogoTXT.filename)))
        temp.logoTXT = request.files['LogoTXT'].filename
    if request.files['LogoTOP'].filename != "":
        LogoTOP = request.files['LogoTOP']
        LogoTOP.save(os.path.join(BASE_PATH, 'static\logos', secure_filename(LogoTOP.filename)))
        temp.logoTOP = request.files['LogoTOP'].filename
    if request.files['LogoBR'].filename != "":
        LogoBR = request.files['LogoBR']
        LogoBR.save(os.path.join(BASE_PATH, 'static\logos', secure_filename(LogoBR.filename)))
        temp.logoBR = request.files['LogoBR'].filename
    if request.files['LogoBL'].filename != "":
        LogoBL = request.files['LogoBL']
        LogoBL.save(os.path.join(BASE_PATH, 'static\logos', secure_filename(LogoBL.filename)))
        temp.logoBL = request.files['LogoBL'].filename
    db.session.commit()
    return teams()
