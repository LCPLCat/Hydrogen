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

#---------------------------------------------------------------------------------
# All functions for player stats and averages
#---------------------------------------------------------------------------------

def link_player_ID():
    stmt = select(ROLFFile.NAME, ROLFFile.ID)
    res = db.session.execute(stmt)
    for x in res:
        if bool(db.session.query(Players).filter_by(name=x[0]).first()):
            player = Players.query.filter_by(name=x[0]).first()
            player.id = x[1]
            db.session.commit()

def player_stats_average():
    stmt = select(Players.id)
    res = db.session.execute(stmt) 
    for x in res:
        if bool(db.session.query(Players).filter_by(id=x[0]).first()):
            player = Players.query.filter_by(id=x[0]).first()
            rolfs = ROLFFile.query.filter_by(ID=x[0]).all()
            if len(rolfs) == 0:
                continue
            Kills = []
            Deaths = []
            Assists = []
            Gold = []
            Wins = []
            Dmg = []
            CreepScore = []
            for i in rolfs:
                Kills.append(i.CHAMPIONS_KILLED)
                Deaths.append(i.NUM_DEATHS)
                Assists.append(i.ASSISTS)
                Gold.append(i.GOLD_EARNED)
                Wins.append(i.WIN)
                Dmg.append(i.TOTAL_DAMAGE_DEALT)
                CreepScore.append(i.MINIONS_KILLED)
            Assists = [int(i) for i in Assists]
            player.killsavg = (sum(Kills)/len(Kills))
            player.deathsavg = (sum(Deaths)/len(Deaths))
            player.assistsavg = (sum(Assists)/len(Assists))
            player.goldavg = (sum(Gold)/len(Gold))
            #player.winpercentage = (sum(Wins)/len(Wins))
            player.dmgavg = (sum(Dmg)/len(Dmg))
            player.creepscoreavg = (sum(CreepScore)/len(CreepScore))
            db.session.commit()

#---------------------------------------------------------------------------------
# All functions for file upload
#---------------------------------------------------------------------------------

def check_upload_file(form):
    audio_file = form.Audio.data
    filename = audio_file.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/audio', secure_filename(filename))
    audio_file.save(upload_path)

def upload_rofl(form):
    rofl_file = form.Rolf.data
    filename = rofl_file.filename
    BASE_PATH = os.path.dirname(__file__)
    upload_path = os.path.join(BASE_PATH, 'static/rofl', secure_filename(filename))
    rofl_file.save(upload_path)
    uploadrofl(filename)

def check_logo_upload(form):
    BASE_PATH = os.path.dirname(__file__)
    form.LogoBlue.data.save(os.path.join(BASE_PATH, 'static/logos', secure_filename(form.LogoBlue.data.filename)))
    form.LogoRed.data.save(os.path.join(BASE_PATH, 'static/logos', secure_filename(form.LogoRed.data.filename)))

