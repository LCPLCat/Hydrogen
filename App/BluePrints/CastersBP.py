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
bp = Blueprint('CastersBP', __name__)

#---------------------------------------------------------------------------------
# All routes for Casters
#---------------------------------------------------------------------------------

@bp.route('/Casters/')
def casters():
    data = Casters.query.all()
    return render_template('Casters/Casters.html', headings = headings.CasterHeadings , data = data)

@bp.route('/CastersAdd/')
def castersadd():
    headings = ("#", "Name", "SubHeading", "Actions")
    data = Casters.query.all()
    Form = CasterRegister()
    return render_template('Casters/CastersAdd.html',form = Form, headings = headings, data = data)

#Caster Del
@bp.route('/Casters/', methods=['POST'])
def casterdel():
    headings = ("#", "Name", "SubHeading", "Actions")
    db.session.delete(Casters.query.get(request.form['id']))
    db.session.commit()
    data = Casters.query.all()
    return render_template('Casters/Casters.html', headings = headings, data = data)

@bp.route('/CasterEdit/', methods=['POST'])
def casteredit():
    temp = Casters.query.get(request.form['id'])
    return render_template('Casters/CasterEdit.html', data = temp)

#Caster Edit
@bp.route('/CasterChanged/', methods=['POST'])
def casterchanged():
    temp = Casters.query.filter_by(id=request.form['id']).first()
    temp.name = request.form['Name']
    temp.subname = request.form['SubName']
    db.session.commit()
    return casters()
