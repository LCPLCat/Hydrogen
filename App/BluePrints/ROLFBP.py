from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from ..forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey
from ..models import Item, Music, Teams, Casters, Players, Match, ROLFFile
from .. import db
from ..Streams import Stream, Headings
from ..replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from ..Streams import Stream, Headings
from ..OtherUtils import *
import os
headings = Headings
bp = Blueprint('ROLFBP', __name__)

#---------------------------------------------------------------------------------
# All routes for rofl upload
#---------------------------------------------------------------------------------
@bp.route('/ROLF/')
def rolf():
    Form = ROLF()
    return render_template('ROLF/ROFL.html', form = Form)

@bp.route('/ROLF/', methods=['POST'])
def rolfadd():
    Form = ROLF()
    upload_rofl(Form)
    link_player_ID()
    player_stats_average()
    return rolf()