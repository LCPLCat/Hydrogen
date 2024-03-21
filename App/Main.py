from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, Response
from .forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey
from .models import Item, Music, Teams, Casters, Players, Match, ROLFFile, MatchStas
from . import db
from .Streams import Stream, Headings
from .replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from .BluePrints import MatchesBP, PlayersBP, TeamsBP, CastersBP, PlayersBP, MusicBP, ROLFBP
from . import OtherUtils, DataBaseUtils
import os
import time
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()
import requests
bp = Blueprint('main', __name__)
os.environ
global CLIENT_ID
CLIENT_ID = os.environ['CLIENT_ID']
global CLIENT_SECRET
CLIENT_SECRET = os.environ['CLIENT_SECRET']
global RIOT_KEY
RIOT_KEY = os.environ['RIOT_KEY']
#format for which stream is selected
Astream = Stream("A")
Bstream = Stream("B")
headings = Headings
global TwitchAuthData
TwitchAuthData = null
timing=10

#---------------------------------------------------------------------------------
# Base Route for the home page
#---------------------------------------------------------------------------------
@bp.route('/')
def index():
    OtherUtils.link_player_ID()
    OtherUtils.player_stats_average()
    data = Casters.query.all()
    data1 = Teams.query.all()
    data2 = Players.query.all()
    return render_template('Home.html', headings = headings.CasterHeadings, data = data, data1 =data1, AStream = Astream, BStream=Bstream, Group1 = Astream.CasterGroup1,
                            Group2 = Astream.CasterGroup2, Group3 = Bstream.CasterGroup1, Group4 = Bstream.CasterGroup2,
                            strm = "A", AWidgets = Astream.Widgets, BWidgets = Bstream.Widgets, code = TwitchAuthData, data2 = data2)
    

@bp.route('/Countdown', methods=['GET'])
def Countdown():
    global timing
    def timer(t):
        for i in range(t):
            time.sleep(60)
            yield str(i)
    return Response(timer(timing), mimetype='text/html')
    
@bp.route('/CountdownTimer', methods=['GET', 'POST'])
def CountdownTimer():
    value = "Bonjour"
    title_html = value
    if request.method=="POST":
        global timing
        timing = int(request.form['timing'])
    return render_template('Countdown/Countdown.html', message=title_html)

@bp.route('/RiotData')
def riotdata():
    Name = 'pip4pig'
    return requests.get("https://oc1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{Name}?api_key={Key}".format(Name=Name, Key=RIOT_KEY)).json()
    
@bp.route('/TwitchAuth/')
def twitchauth():
    return redirect('https://id.twitch.tv/oauth2/authorize?response_type=code&client_id='+CLIENT_ID+'&force_verify=true&redirect_uri=http://localhost:5000/TwitchRedirect/&scope=channel%3Amanage%3Abroadcast')

@bp.route('/TwitchRedirect/', methods = ["POST","GET"])
def twitchredirect():
    TwitchAuthData = request.args.get("code")
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': TwitchAuthData,
            'grant_type': 'authorization_code',
            'redirect_uri': 'http://localhost:5000/Oauth2/'

    }
    text = requests.request('POST', 'https://id.twitch.tv/oauth2/token', headers=headers, data=data).json()
    
    return render_template('TwtichAPI/TwtichAPI.html',access_token=text["access_token"],refresh_token=text["refresh_token"], CLIENT_ID = CLIENT_ID)

@bp.route('/Oauth2/', methods = ["POST","GET"])
def oauth2():
    
    return redirect("")
@bp.route('/Widgets/', methods = ["POST","GET"])
def widgets():
    if request.method == "POST":
        Astream.Widgets["StreamStats"] = request.form['StreamStats']
        Astream.Widgets["Casters"] = request.form['Casters']
        Astream.Widgets["PlayerStats"] = request.form['PlayerStats']
        Astream.Widgets["Overlay"] = request.form['Overlay']
        Astream.Widgets["Schedule"] = request.form['Schedule']
        Bstream.Widgets["StreamStats"] = request.form['StreamStats']
        Bstream.Widgets["Casters"] = request.form['Casters']
        Bstream.Widgets["PlayerStats"] = request.form['PlayerStats']
        Bstream.Widgets["Overlay"] = request.form['Overlay']
        Bstream.Widgets["Schedule"] = request.form['Schedule']
        return redirect("/")
    if request.method == "GET":
        return redirect("/")

@bp.route('/StatsWidget/', methods=['POST'])
def StatsWidget():
    if (request.form['XID'] == 'A'):
        Astream.Stats=[[request.form['FormPlayerA1'],request.form['FormPlayerA1Team'],request.form['FormPlayerA1ID']],[request.form['FormPlayerA2'],request.form['FormPlayerA2Team'],request.form['FormPlayerA2ID']]]
    elif (request.form['XID'] == 'B'):
        Bstream.Stats=[[request.form['FormPlayerB1'],request.form['FormPlayerB1Team'],request.form['FormPlayerB1ID']],[request.form['FormPlayerB2'],request.form['FormPlayerB2Team'],request.form['FormPlayerB2ID']]]  
    return redirect("/")

@bp.route('/OverlayWidget/', methods=['POST'])
def OverlayWidget():
    if (request.form['XID']== "A"):
        Astream.Team = [[request.form['LeftIDA'],request.form['LeftTeamLogoA'],request.form['LeftTeamA'],request.form['LeftAbbA']],[request.form['RightIDA'],request.form['RightTeamLogoA'],request.form['RightTeamA'],request.form['RightAbbA']]]
    elif (request.form['XID']== "B"):
        Bstream.Team = [[request.form['LeftIDB'],request.form['LeftTeamLogoB'],request.form['LeftTeamB'],request.form['LeftAbbB']],[request.form['RightIDB'],request.form['RightTeamLogoB'],request.form['RightTeamB'],request.form['RightAbbB']]]
    return redirect("/")

@bp.route('/CasterWidget/', methods=['POST'])
def CasterWidget():
    if (request.form['XID']== "A"):
        Astream.CasterGroup1 = [[request.form['AFormCaster1'],request.form['AFormCaster1Sub'],request.form['AFormCaster1ID']]
            ,[request.form['AFormCaster2'],request.form['AFormCaster2Sub'],request.form['AFormCaster2ID']]]
        Astream.CasterGroup2 = [[request.form['AFormCaster3'],request.form['AFormCaster3Sub'],request.form['AFormCaster3ID']]
            ,[request.form['AFormCaster4'],request.form['AFormCaster4Sub'],request.form['AFormCaster4ID']]
            ,[request.form['AFormCaster5'],request.form['AFormCaster5Sub'],request.form['AFormCaster5ID']]]
    elif (request.form['XID']== "B"):
        Bstream.CasterGroup1 = [[request.form['BFormCaster1'],request.form['BFormCaster1Sub'],request.form['BFormCaster1ID']]
                ,[request.form['BFormCaster2'],request.form['BFormCaster2Sub'],request.form['BFormCaster2ID']]]
        Bstream.CasterGroup2 = [[request.form['BFormCaster3'],request.form['BFormCaster3Sub'],request.form['BFormCaster3ID']]
                ,[request.form['BFormCaster4'],request.form['BFormCaster4Sub'],request.form['BFormCaster4ID']]
                ,[request.form['BFormCaster5'],request.form['BFormCaster5Sub'],request.form['BFormCaster5ID']]]
    
    return redirect("/")

@bp.route('/riot.txt/',  methods = ["POST","GET"])
def riot():
    return render_template('riot.txt')
#---------------------------------------------------------------------------------
# All routes for Overlays including Caster lower third, Schedule, Stats, and Team Vs overlays
#---------------------------------------------------------------------------------

@bp.route('/CastersOverlay/', methods=['GET'])
def castersoverlay():
    data = Casters.query.all()
    if request.args.get('stream') == 'A':
        return render_template('Overlays/CastersSelect.html', headings = headings.CasterHeadings, data = data, Group1 = Astream.CasterGroup1, Group2 = Astream.CasterGroup2, strm = "A")
    elif request.args.get('stream') == 'B':
        return render_template('Overlays/CastersSelect.html', headings = headings.CasterHeadings, data = data, Group1 = Bstream.CasterGroup1, Group2 = Bstream.CasterGroup2, strm = "B")   

@bp.route('/CastersOverlay/', methods=['POST'])
def castersoverlay_data():
    if request.args.get('stream') == 'A':
        Astream.CasterGroup1 = [[request.form['FormCaster1'],request.form['FormCaster1Sub'],request.form['FormCaster1ID']]
                    ,[request.form['FormCaster2'],request.form['FormCaster2Sub'],request.form['FormCaster2ID']]]
        Astream.CasterGroup2 = [[request.form['FormCaster3'],request.form['FormCaster3Sub'],request.form['FormCaster3ID']]
                    ,[request.form['FormCaster4'],request.form['FormCaster4Sub'],request.form['FormCaster4ID']]
                    ,[request.form['FormCaster5'],request.form['FormCaster5Sub'],request.form['FormCaster5ID']]]
    elif request.args.get('stream') == 'B':
        Bstream.CasterGroup1 = [[request.form['FormCaster1'],request.form['FormCaster1Sub'],request.form['FormCaster1ID']]
                    ,[request.form['FormCaster2'],request.form['FormCaster2Sub'],request.form['FormCaster2ID']]]
        Bstream.CasterGroup2 = [[request.form['FormCaster3'],request.form['FormCaster3Sub'],request.form['FormCaster3ID']]
                    ,[request.form['FormCaster4'],request.form['FormCaster4Sub'],request.form['FormCaster4ID']]
                    ,[request.form['FormCaster5'],request.form['FormCaster5Sub'],request.form['FormCaster5ID']]]
    return castersoverlay()

@bp.route('/Schedule/')
def scheduleoverlay():
    data = Match.query.all()
    teams = Teams.query.all()
    if request.args.get('stream') == 'A':
        print("A")
        print(Astream.Schedule)
        return render_template('Overlays/Schedule.html', data = data,teams = teams, schedule=Astream.Schedule, strm = "A")
        
    elif request.args.get('stream') == 'B':
        print("B")
        print(Bstream.Schedule)
        return render_template('Overlays/Schedule.html', data = data,teams = teams, schedule=Bstream.Schedule, strm = "B")  
           
@bp.route('/Schedule/', methods=['POST'])
def scheduleoverlay_data():
    if request.args.get('stream') == 'A':
        print("A")
        for idx, x in enumerate(Astream.Schedule, start=1):
            x[0]= request.form['MatchID'+str(idx)]
            x[1]= request.form['Team1'+str(idx)]
            x[2]= request.form['Team2'+str(idx)]
            x[3]= request.form['Time'+str(idx)]
            x[4]= request.form['Format'+str(idx)]
            x[5]= request.form['Team1name'+str(idx)]
            x[6]= request.form['Team2name'+str(idx)]
        print(Astream.Schedule)
    elif request.args.get('stream') == 'B':
        print("B")
        for idx, x in enumerate(Bstream.Schedule, start=1):
            x[0]= request.form['MatchID'+str(idx)]
            x[1]= request.form['Team1'+str(idx)]
            x[2]= request.form['Team2'+str(idx)]
            x[3]= request.form['Time'+str(idx)]
            x[4]= request.form['Format'+str(idx)]
            x[5]= request.form['Team1name'+str(idx)]
            x[6]= request.form['Team2name'+str(idx)] 
        print(Bstream.Schedule) 
    return scheduleoverlay()

@bp.route('/Overlay/', methods=['POST'])
def overlay_data():
    if request.args.get('stream') == 'A':
        Astream.Team = [[request.form['LeftID'],request.form['LeftTeamLogo'],request.form['LeftTeam'],request.form['LeftAbb']],[request.form['RightID'],request.form['RightTeamLogo'],request.form['RightTeam'],request.form['RightAbb']]]
    elif request.args.get('stream') == 'B':
        Bstream.Team = [[request.form['LeftID'],request.form['LeftTeamLogo'],request.form['LeftTeam'],request.form['LeftAbb']],[request.form['RightID'],request.form['RightTeamLogo'],request.form['RightTeam'],request.form['RightAbb']]]

    return overlay()

@bp.route('/Overlay/', methods=['GET'])
def overlay():
    data = Teams.query.all()
    if request.args.get('stream') == 'A':
        return render_template('Overlays/Overlay.html', data = data, LeftTeam = Astream.Team[0][2], RightTeam=Astream.Team[1][2], LeftTeamLogo = Astream.Team[0][1], RightTeamLogo=Astream.Team[1][1], LeftID = Astream.Team[0][0], RightID = Astream.Team[1][0], LeftAbb = Astream.Team[0][3] , RightAbb = Astream.Team[1][3], strm = "A")
    elif request.args.get('stream') == 'B':
        return render_template('Overlays/Overlay.html', data = data, LeftTeam = Bstream.Team[0][2], RightTeam=Bstream.Team[1][2], LeftTeamLogo = Bstream.Team[0][1], RightTeamLogo=Bstream.Team[1][1], LeftID = Bstream.Team[0][0], RightID = Bstream.Team[1][0], LeftAbb = Bstream.Team[0][3] , RightAbb = Bstream.Team[1][3], strm = "B") 

@bp.route('/Stats/', methods=['GET'])
def stats():
    OtherUtils.link_player_ID()
    OtherUtils.player_stats_average()
    data = Players.query.all()
    if request.args.get('stream') == 'A':
        return render_template('Overlays/Stats.html', data = data, player1name = Astream.Stats[0][0], player2name = Astream.Stats[1][0], player1team = Astream.Stats[0][1], player2team = Astream.Stats[1][1], player1id=Astream.Stats[0][2], player2id = Astream.Stats[1][2], strm = "A")
    elif request.args.get('stream') == 'B':
        return render_template('Overlays/Stats.html', data = data, player1name = Bstream.Stats[0][0], player2name = Bstream.Stats[1][0], player1team = Bstream.Stats[0][1], player2team = Bstream.Stats[1][1], player1id=Bstream.Stats[0][2], player2id = Bstream.Stats[1][2], strm = "B") 
    
@bp.route('/Stats/', methods=['POST'])
def stats_data():
    if request.args.get('stream') == 'A':
        Astream.Stats=[[request.form['FormPlayer1'],request.form['FormPlayer1Team'],request.form['FormPlayer1ID']],[request.form['FormPlayer2'],request.form['FormPlayer2Team'],request.form['FormPlayer2ID']]]
    elif request.args.get('stream') == 'B':
        Bstream.Stats=[[request.form['FormPlayer1'],request.form['FormPlayer1Team'],request.form['FormPlayer1ID']],[request.form['FormPlayer2'],request.form['FormPlayer2Team'],request.form['FormPlayer2ID']]]  
    return stats()

#---------------------------------------------------------------------------------
# All routes for form submitions
#---------------------------------------------------------------------------------
@bp.route('/submit', methods=['GET','POST'])
def submit():
    form = MusicUpload()
    OtherUtils.check_upload_file(form)
    DataBaseUtils.add_to_database(form)
    return MusicBP.music()

@bp.route('/teamsubmit', methods=['GET','POST'])
def teamsubmit():
    form = TeamRegister()
    OtherUtils.check_logo_upload(form)
    DataBaseUtils.add_team_to_database(form)
    return TeamsBP.teams()

@bp.route('/castersubmit', methods=['GET','POST'])
def castersubmit():
    DataBaseUtils.add_casters_to_database(CasterRegister())
    return CastersBP.casters()

@bp.route('/matchsubmit', methods=['GET','POST'])
def matchsubmit():
    DataBaseUtils.add_match_to_database(MatchRegister())
    return MatchesBP.match()

@bp.route('/playersubmit', methods=['GET','POST'])
def playersubmit():
    DataBaseUtils.add_players_to_database(PlayerRegister())
    return PlayersBP.players()

@bp.route('/StreamChange', methods=['POST'])
def streamchange():
    return PlayersBP.players()

#---------------------------------------------------------------------------------
# All routes for XMLs
#---------------------------------------------------------------------------------

@bp.route('/XML')
def xml():
    return render_template('XML/XML.html')

@bp.route('/Stats/API.xml')
def statsAPI():
    response = make_response()
    if request.args.get('stream') == 'A':
        response = make_response(render_template('XML/Stats.xml', player1 = Players.query.get(Astream.Stats[0][2]), player2 = Players.query.get(Astream.Stats[1][2])))
    elif request.args.get('stream') == 'B':
        response = make_response(render_template('XML/Stats.xml', player1 = Players.query.get(Bstream.Stats[0][2]), player2 = Players.query.get(Bstream.Stats[1][2])))
    response.headers['Content-Type'] = 'application/xml'
    return response

@bp.route('/Overlay/API.xml')
def overlayAPI():
    response = make_response()
    if request.args.get('stream') == 'A':
        Left = Teams.query.get(Astream.Team[0][0])
        Right = Teams.query.get(Astream.Team[1][0])
        response = make_response(render_template('XML/OverlayAPI.xml', Left=Left , Right=Right))
    elif request.args.get('stream') == 'B':
        response = make_response(render_template('XML/OverlayAPI.xml', Left = Teams.query.get(Bstream.Team[0][0]), Right = Teams.query.get(Bstream.Team[1][0])))
    response.headers['Content-Type'] = 'application/xml'
    return response

@bp.route('/Music/API.xml')
def musicAPI():
    response = make_response(render_template('XML/MusicAPI.xml', data = Music.query.all()))
    response.headers['Content-Type'] = 'application/xml'
    return response

@bp.route('/Casters/API.xml')
def castersAPI():
    response = make_response()
    if request.args.get('stream') == 'A':
        response = make_response(render_template('XML/CastersAPI.xml', Group1 = Astream.CasterGroup1, Group2 = Astream.CasterGroup2))
    elif request.args.get('stream') == 'B':
        response = make_response(render_template('XML/CastersAPI.xml', Group1 = Bstream.CasterGroup1, Group2 = Bstream.CasterGroup2))
    response.headers['Content-Type'] = 'application/xml'
    return response

@bp.route('/Match/API.xml')
def MatchAPI():
    teams = Teams.query.all()
    response = make_response()
    if request.args.get('stream') == 'A':
        response = make_response(render_template('XML/MatchAPI.xml', matches = Astream.Schedule, teams=teams))
    elif request.args.get('stream') == 'B':
        response = make_response(render_template('XML/MatchAPI.xml', matches = Bstream.Schedule, teams=teams))
    response.headers['Content-Type'] = 'application/xml'
    return response

@bp.route('/Standings/API.xml')
def StandingsAPI():
    Ateams = Teams.query.filter_by(description='Div 1A').order_by(Teams.wins.desc(),Teams.losses.asc())
    Bteams = Teams.query.filter_by(description='Div 1B').order_by(Teams.wins.desc(),Teams.losses.asc())
    Womens = Teams.query.filter_by(description='Womens').order_by(Teams.wins.desc(),Teams.losses.asc())
    odt = Teams.query.filter_by(description='ODTA').order_by(Teams.wins.desc(),Teams.losses.asc())
    odtb = Teams.query.filter_by(description='ODTB').order_by(Teams.wins.desc(),Teams.losses.asc())
    response = make_response()
    response = make_response(render_template('XML/StandingsAPI.xml', Ateams=Ateams, Bteams=Bteams, Womens=Womens, ODTA=odt, ODTB=odtb ))
    response.headers['Content-Type'] = 'application/xml'
    return response
        
@bp.route('/SuperTeams')
def SuperTeams():
    Scores = []
    players = Players.query.all()
    for i, player in enumerate(players):
        temp2 = []
        stats = MatchStas.query.filter_by(puuid=player.puid)
        temp2.append(player.puid)
        temp2.append(player.name)
        for i, stat in enumerate(stats):
            temp = 0
            temp += int(stat.assists)
            temp += (int(stat.kills)*2)
            temp += (int(stat.quadraKills)*5)
            temp += (round(int(stat.visionScore)/100)*5)
            temp += (int(stat.pentaKills)*10)
            if (stat.visionScore != 0):
                temp -= (round(int(stat.visionScore)/100)*5)
            temp += (int(stat.baronKills)*3)
            temp += int(stat.dragonKills)
            temp += (round(int(stat.totalMinionsKilled)/300)*3)
            temp2.append(temp)
        Scores.append(temp2) 
    response = make_response()
    response = make_response(render_template('XML/SuperTeamsAPI.xml', scores=Scores))
    response.headers['Content-Type'] = 'application/xml'
    return response
#---------------------------------------------------------------------------------
# All routes for Riot API
#---------------------------------------------------------------------------------

@bp.route('/RiotAPI')
def RiotAPI():
    Form = APIKey()
    return render_template('RiotAPI/RiotAPI.html',form = Form)

