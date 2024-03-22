from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from .forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey
from .models import Item, Music, Teams, Casters, Players, Match, ROLFFile
from . import db
from .Streams import Stream, Headings
from .replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from .BluePrints import MatchesBP, PlayersBP, TeamsBP, CastersBP, PlayersBP, MusicBP
import os
from datetime import *
import requests
from dotenv import load_dotenv
load_dotenv()
global RIOT_KEY
RIOT_KEY = os.environ['RIOT_KEY']
#---------------------------------------------------------------------------------
# Database functions
#---------------------------------------------------------------------------------

def add_to_database(form):
    item1=Music(title = form.Title.data, author = form.Author.data, audio = form.Audio.data.filename)
    db.session.add(item1)
    db.session.commit()

def add_team_to_database(form):
    item1=Teams(name = form.Name.data, abbreviation = form.Abbreviation.data, logoBlue = form.LogoBlue.data.filename, logoRed = form.LogoRed.data.filename,  description = form.Description.data, colour = form.Colour.data, wins =0, losses = 0 )
    db.session.add(item1)
    db.session.commit()

def add_match_to_database(form):
    db.session.add(Match(team1 = form.Team1.data, team2 = form.Team2.data, time = form.Time.data, format = form.Format.data, team1name = form.Team1name.data, team2name = form.Team2name.data, recorddate=datetime.now()))
    db.session.commit()

def add_casters_to_database(form):
    db.session.add(Casters(name = form.Name.data, subname = form.Subheading.data))
    db.session.commit()

def add_players_to_database(form):
    db.session.add(Players(name = form.Name.data, team = form.Team.data, puid = 'null'))
    db.session.commit()

