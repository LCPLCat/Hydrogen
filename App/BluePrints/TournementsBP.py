from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from ..forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey, TournementRegister
from ..models import Item, Music, Teams, Casters, Players, Match, ROLFFile, Tournment
from .. import db
from ..Streams import Stream, Headings
from ..replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from ..Streams import Stream, Headings
from ..OtherUtils import *
import os
headings = Headings
bp = Blueprint('TournementsBP', __name__)

@bp.route('/Tournements/')
def Tournements():
    Tournements = Tournment.query.all()
    return render_template('Tournements/Tournements.html', Tournements=Tournements)

@bp.route('/Tournements/Add')
def Tournementsadd():
    form = TournementRegister()
    return render_template('Tournements/TournementsAdd.html', form=form)

@bp.route('/Tournements/Submit', methods=['POST'])
def submit():
    return Tournements()
