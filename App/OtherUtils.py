from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from .forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey
from .models import Item, Music, Teams, Casters, Players, Match, ROLFFile, MatchStas
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
    stmt = select(Players.puid)
    res = db.session.execute(stmt) 
    for x in res:
        if bool(db.session.query(Players).filter_by(puid=x[0]).first()):
            player = Players.query.filter_by(puid=x[0]).first()
            rolfs = MatchStas.query.filter_by(puuid=x[0]).all()
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
                Kills.append(int(i.kills))
                Deaths.append(int(i.deaths))
                Assists.append(int(i.assists))
                Gold.append(int(i.goldEarned))
                #Wins.append(i.WIN)
                Dmg.append(int(i.totalDamageDealt))
                CreepScore.append(int(i.totalMinionsKilled))
            Assists = [int(i) for i in Assists]
            player.killsavg = round(sum(Kills)/len(Kills))
            player.deathsavg = round(sum(Deaths)/len(Deaths))
            player.assistsavg = round(sum(Assists)/len(Assists))
            player.goldavg = round(sum(Gold)/len(Gold))
            player.dmgavg = round(sum(Dmg)/len(Dmg))
            player.creepscoreavg = round(sum(CreepScore)/len(CreepScore))
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

