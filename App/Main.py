from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response, Response
from .forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey
from .models import Item, Music, Teams, Casters, Players, Match, ROLFFile
from . import db
from .Streams import Stream, Headings
from .replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from .BluePrints import MatchesBP, PlayersBP, TeamsBP, CastersBP, PlayersBP, MusicBP, ROLFBP
from . import OtherUtils, DataBaseUtils
import os
import time
from dotenv import load_dotenv
load_dotenv()
import requests
bp = Blueprint('main', __name__)
os.environ
global CLIENT_ID
CLIENT_ID = os.environ['CLIENT_ID']
global CLIENT_SECRET
CLIENT_SECRET = os.environ['CLIENT_SECRET']
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
    data = Casters.query.all()
    data1 = Teams.query.all()
    
    return render_template('Home.html', headings = headings.CasterHeadings, data = data, data1 =data1, AStream = Astream, BStream=Bstream, Group1 = Astream.CasterGroup1
                           , Group2 = Astream.CasterGroup2, Group3 = Bstream.CasterGroup1, Group4 = Bstream.CasterGroup2
                           , strm = "A", AWidgets = Astream.Widgets, BWidgets = Bstream.Widgets, code = TwitchAuthData)
    

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
    
    return text

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
#---------------------------------------------------------------------------------
# All routes for Matches
#---------------------------------------------------------------------------------
'''
@bp.route('/Matches/')
def match():
    data = Match.query.all()
    teams = Teams.query.all()
    return render_template('Matches.html', headings = headings.MatchHeadings, data = data,teams=teams)

@bp.route('/Matches/Add')
def matchadd():
    data = Match.query.all()
    teams = Teams.query.all()
    return render_template('MatchAdd.html', data = data, teams=teams)

@bp.route('/Matches/Edit', methods=['POST'])
def matchsave():
    data = Match.query.filter_by(id=request.form['id']).first()
    teams = Teams.query.all()
    return render_template('MatchEdit.html', matches = data, teams=teams)

@bp.route('/Matches/Decide', methods=['POST'])
def matchdecide():
    data = Match.query.filter_by(id=request.form['id']).first()
    teams = Teams.query.all()
    return render_template('MatchDecide.html', match = data, teams=teams)

@bp.route('/Matches/Decided', methods=['POST'])
def matchdecide_submit():
    data = Match.query.filter_by(id=request.form['matchid']).first()
    print(request.form['winnerid'])
    print(request.form['loserid'])
    winner = Teams.query.filter_by(id=request.form['winnerid']).first()
    loser = Teams.query.filter_by(id=request.form['loserid']).first()
    loser.losses = int(loser.losses) + 1
    winner.wins = int(winner.wins) + 1
    data.winner = winner.id
    data.loser = loser.id
    data.decided = 1
    db.session.commit()
    return match()

@bp.route('/Matches/Swap', methods=['POST'])
def matchswap():
    data = Match.query.filter_by(id=request.form['matchid']).first()
    winner = Teams.query.filter_by(id=request.form['winnerid']).first()
    loser = Teams.query.filter_by(id=request.form['loserid']).first()
    loser.losses = int(loser.losses) - 1
    winner.wins = int(winner.wins) - 1
    loser.wins = int(loser.wins) + 1
    winner.losses = int(winner.losses) + 1
    data.loser = winner.id
    data.winner = loser.id
    db.session.commit()
    return match()

#Matches Del
@bp.route('/Matches/', methods=['POST'])
def matchdel():
    db.session.delete(Match.query.get(request.form['id']))
    db.session.commit()
    data = Match.query.get(request.form['id'])
    teams = Teams.query.all()
    return match()

@bp.route('/MatchChanged/', methods=['POST'])
def matchchanged():
    temp = Match.query.filter_by(id=request.form['id']).first()
    print(request.form['id'])
    temp.team1 = request.form['Team1']
    temp.team2 = request.form['Team2']
    temp.time = request.form['Time']
    temp.format = request.form['Format']
    db.session.commit()
    return match()



#---------------------------------------------------------------------------------
# All routes for Casters
#---------------------------------------------------------------------------------

@bp.route('/Casters/')
def casters():
    data = Casters.query.all()
    return render_template('Casters.html', headings = headings.CasterHeadings , data = data)

@bp.route('/CastersAdd/')
def castersadd():
    headings = ("#", "Name", "SubHeading", "Actions")
    data = Casters.query.all()
    Form = CasterRegister()
    return render_template('CastersAdd.html',form = Form, headings = headings, data = data)

#Caster Del
@bp.route('/Casters/', methods=['POST'])
def casterdel():
    headings = ("#", "Name", "SubHeading", "Actions")
    db.session.delete(Casters.query.get(request.form['id']))
    db.session.commit()
    data = Casters.query.all()
    return render_template('Casters.html', headings = headings, data = data)

@bp.route('/CasterEdit/', methods=['POST'])
def casteredit():
    temp = Casters.query.get(request.form['id'])
    return render_template('CasterEdit.html', data = temp)

#Caster Edit
@bp.route('/CasterChanged/', methods=['POST'])
def casterchanged():
    temp = Casters.query.filter_by(id=request.form['id']).first()
    temp.name = request.form['Name']
    temp.subname = request.form['SubName']
    db.session.commit()
    return casters()

#---------------------------------------------------------------------------------
# All routes for Teams
#---------------------------------------------------------------------------------

@bp.route('/Teams/')
def teams():
    data = Teams.query.all()
    return render_template('Teams.html', headings = headings.TeamHeadings, data = data)

@bp.route('/TeamsAdd/')
def teamadd():
    data = Teams.query.all()
    Form = TeamRegister()
    return render_template('TeamAdd.html',form = Form, headings = headings.TeamHeadings, data = data)

#Team Del
@bp.route('/Teams/', methods=['POST'])
def teamdel():
    headings = ("#", "Title", "Author","Music", "Actions")
    db.session.delete(Teams.query.get(request.form['id']))
    db.session.commit()
    data = Teams.query.all()
    return render_template('Teams.html', headings = headings.TeamHeadings, data = data)

@bp.route('/TeamsEdit/', methods=['POST'])
def teamedit():
    temp = Teams.query.get(request.form['id'])
    return render_template('TeamEdit.html', data = temp)

#Caster Edit
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

#---------------------------------------------------------------------------------
# All routes for Music
#---------------------------------------------------------------------------------

@bp.route('/Music/')
def music():
    data = Music.query.all()
    return render_template('Music.html', headings = headings.MusicHeadings, data = data)

@bp.route('/MusicAdd/')
def musicadd():
    data = Music.query.all()
    Form = MusicUpload()
    return render_template('MusicAdd.html', form = Form, headings = headings.MusicHeadings, data = data)

#Music Del
@bp.route('/Music/', methods=['POST'])
def musicdel():
    db.session.delete(Music.query.get(request.form['id']))
    db.session.commit()
    data = Music.query.all()
    return render_template('Music.html', headings = headings.MusicHeadings, data = data)

@bp.route('/MusicEdit/', methods=['POST'])
def musicedit():
    Musictemp = Music.query.get(request.form['id'])
    return render_template('MusicEdit.html', data = Musictemp)

#Music Edit
@bp.route('/MusicChanged/', methods=['POST'])
def musicchanged():
    temp = Music.query.filter_by(id=request.form['id']).first()
    temp.title = request.form['Title']
    temp.author = request.form['Author']
    if request.form['Audio'] != "":
        temp.audio = request.form['Audio']
    db.session.commit()
    return music()

#---------------------------------------------------------------------------------
# All routes for Player
#---------------------------------------------------------------------------------

@bp.route('/Players/')
def players():
    data = Players.query.all()
    return render_template('Players.html', headings = headings.PlayerHeadings, data = data)

@bp.route('/PlayersAdd/')
def playeradd():
    Form = PlayerRegister()
    data = Players.query.all()
    return render_template('PlayersAdd.html', form = Form, data =data )

@bp.route('/PlayersEdit/', methods=['POST'])
def playeredit():
    temp = Players.query.get(request.form['id'])
    return render_template('PlayersEdit.html', data = temp)

@bp.route('/PlayersChanged/', methods=['POST'])
def playerchanged():
    temp = Players.query.filter_by(id=request.form['id']).first()
    temp.name = request.form['Name']
    temp.team = request.form['Team']
    db.session.commit()
    return players()

#Players Del
@bp.route('/Players/', methods=['POST'])
def playerdel():
    db.session.delete(Players.query.get(request.form['id']))
    db.session.commit()
    data = Players.query.all()
    return render_template('Players.html', headings = headings.PlayerHeadings, data = data)
'''
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
        Astream.Team = [[request.form['LeftID'],request.form['LeftTeamLogo'],request.form['LeftTeam']],[request.form['RightID'],request.form['RightTeamLogo'],request.form['RightTeam']]]
    elif request.args.get('stream') == 'B':
        Bstream.Team = [[request.form['LeftID'],request.form['LeftTeamLogo'],request.form['LeftTeam']],[request.form['RightID'],request.form['RightTeamLogo'],request.form['RightTeam']]]

    return overlay()

@bp.route('/Overlay/', methods=['GET'])
def overlay():
    data = Teams.query.all()
    if request.args.get('stream') == 'A':
        return render_template('Overlays/Overlay.html', data = data, LeftTeam = Astream.Team[0][2], RightTeam=Astream.Team[1][2], LeftTeamLogo = Astream.Team[0][1], RightTeamLogo=Astream.Team[1][1], LeftID = Astream.Team[0][0], RightID = Astream.Team[1][0], strm = "A")
    elif request.args.get('stream') == 'B':
        return render_template('Overlays/Overlay.html', data = data, LeftTeam = Bstream.Team[0][2], RightTeam=Bstream.Team[1][2], LeftTeamLogo = Bstream.Team[0][1], RightTeamLogo=Bstream.Team[1][1], LeftID = Bstream.Team[0][0], RightID = Bstream.Team[1][0], strm = "B") 

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
        response = make_response(render_template('XML/OverlayAPI.xml', Left = Teams.query.get(Astream.Team[0][0]), Right = Teams.query.get(Astream.Team[1][0])))
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
    response = make_response()
    if request.args.get('stream') == 'A':
        response = make_response(render_template('XML/MatchAPI.xml', matches = Astream.Schedule))
    elif request.args.get('stream') == 'B':
        response = make_response(render_template('XML/MatchAPI.xml', matches = Bstream.Schedule))
    response.headers['Content-Type'] = 'application/xml'
    return response

#---------------------------------------------------------------------------------
# All routes for Riot API
#---------------------------------------------------------------------------------

@bp.route('/RiotAPI')
def RiotAPI():
    Form = APIKey()
    return render_template('RiotAPI/RiotAPI.html',form = Form)

