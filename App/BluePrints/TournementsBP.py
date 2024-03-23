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
from ..DataBaseUtils import *
import requests
import os
from dotenv import load_dotenv
load_dotenv()
global PROVIDER
PROVIDER = os.environ['PROVIDER']
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

    form = TournementRegister()
    response = requests.post('https://americas.api.riotgames.com/lol/tournament/v5/tournaments?api_key='+RIOT_KEY, json={"name": form.Name.data,"providerId": PROVIDER}).json()
    add_touranment_to_database(form, response)
    return redirect('/Tournements/')

@bp.route('/Tournements/Codes', methods=['POST','GET'])
def TournementsCodes():
    return str(200)