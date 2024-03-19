from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response
from ..forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey, MatchID
from ..models import Item, Music, Teams, Casters, Players, Match, ROLFFile, MatchStas
from ..OtherUtils import * 
from .. import db
from ..Streams import Stream, Headings
from ..replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from ..Streams import Stream, Headings
import os
import json
import requests
from types import SimpleNamespace
from dotenv import load_dotenv
load_dotenv()
global RIOT_KEY
RIOT_KEY = os.environ['RIOT_KEY']
bp = Blueprint('RiotAPIBP', __name__)
 
@bp.route('/RiotAPI', methods=['GET','POST'])
def MatchGetStats():
    Form = MatchID()
    return render_template('RiotAPI/RiotAPI.html', form = Form)

@bp.route('/RiotAPI/', methods=['POST'])
def MatchSubmitStats():
    GetStatsRIOTAPI(request.form['Match ID'])
    return render_template('RiotAPI/RiotAPI.html')

def GetMatchIDFromPlayer(name):
    gameName = name.split("#")[0]
    tagLine = name.split("#")[1]
    global RIOT_KEY
    json = requests.get('https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'+gameName+'/'+tagLine+"?api_key="+RIOT_KEY).json()
    puuid=json['puuid']
    json = requests.get('https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/'+puuid+'/ids?type=tourney&start=0&count=1&api_key='+RIOT_KEY).json()
    GetStatsRIOTAPI(json[0])
    link_player_PUUID()
    #player_stats_average()


def GetStatsRIOTAPI(Match_id):
    global RIOT_KEY
    #TimeLine = requests.get('https://sea.api.riotgames.com/lol/match/v5/matches/'+Match_id+"/timeline?api_key="+RIOT_KEY).json()
    #print(TimeLine['metadata']['participants'])
    json = requests.get('https://sea.api.riotgames.com/lol/match/v5/matches/'+Match_id+"?api_key="+RIOT_KEY).json()
    JsonExtract(json['info'], json['metadata'])

def link_player_PUUID():
    players = Players.query.all()
    stats = MatchStas.query.all()
    for i, match in enumerate(stats):
        name = match.riotIdGameName + "#" + match.riotIdTagline
        for i, player in enumerate(players):
            #print(player)
            if player.name == name:
                player.puid = str(match.puuid)
                #print(match.puuid)
    db.session.commit()
    

def JsonExtract(info, metadata):
    stats = MatchStas.query.all()
    
    con = sqlite3.connect("./instance/auction_alchemy.db")
    cur = con.cursor()
    cur.execute("BEGIN;")
    for i, player in enumerate(info['participants']):
        name = player['puuid']+metadata['matchId']
        for i, match in enumerate(stats):
            if name == match.id2:
                return
        statment = f"""INSERT INTO StatsRiotAPI VALUES(
            "{player['puuid']+metadata['matchId']}",
            "{info['gameId']}",
            "{player['allInPings']}",
            "{player['assistMePings']}",
            "{player['assists']}",
            "{player['baronKills']}",
            "{player['basicPings']}",
            "{player['bountyLevel']}",
            "{player['champExperience']}",
            "{player['champLevel']}",
            "{player['championId']}",
            "{player['championName']}",
            "{player['championTransform']}",
            "{player['commandPings']}",
            "{player['consumablesPurchased']}",
            "{player['damageDealtToBuildings']}",
            "{player['damageDealtToObjectives']}",
            "{player['damageDealtToTurrets']}",
            "{player['damageSelfMitigated']}",
            "{player['dangerPings']}",
            "{player['deaths']}",
            "{player['detectorWardsPlaced']}",
            "{player['doubleKills']}",
            "{player['dragonKills']}",
            "{player['eligibleForProgression']}",
            "{player['enemyMissingPings']}",
            "{player['enemyVisionPings']}",
            "{player['firstBloodAssist']}",
            "{player['firstBloodKill']}",
            "{player['firstTowerAssist']}",
            "{player['firstTowerKill']}",
            "{player['gameEndedInEarlySurrender']}",
            "{player['gameEndedInSurrender']}",
            "{player['getBackPings']}",
            "{player['goldEarned']}",
            "{player['goldSpent']}",
            "{player['holdPings']}",
            "{player['individualPosition']}",
            "{player['inhibitorKills']}",
            "{player['inhibitorTakedowns']}",
            "{player['inhibitorsLost']}",
            "{player['item0']}",
            "{player['item1']}",
            "{player['item2']}",
            "{player['item3']}",
            "{player['item4']}",
            "{player['item5']}",
            "{player['item6']}",
            "{player['itemsPurchased']}",
            "{player['killingSprees']}",
            "{player['kills']}",
            "{player['lane']}",
            "{player['largestCriticalStrike']}",
            "{player['largestKillingSpree']}",
            "{player['largestMultiKill']}",
            "{player['longestTimeSpentLiving']}",
            "{player['magicDamageDealt']}",
            "{player['magicDamageDealtToChampions']}",
            "{player['magicDamageTaken']}",
            "{player['needVisionPings']}",
            "{player['neutralMinionsKilled']}",
            "{player['nexusKills']}",
            "{player['nexusLost']}",
            "{player['nexusTakedowns']}",
            "{player['objectivesStolen']}",
            "{player['objectivesStolenAssists']}",
            "{player['onMyWayPings']}",
            "{player['participantId']}",
            "{player['pentaKills']}",
            "{player['physicalDamageDealt']}",
            "{player['physicalDamageDealtToChampions']}",
            "{player['physicalDamageTaken']}",
            "{player['placement']}",
            "{player['playerAugment1']}",
            "{player['playerAugment2']}",
            "{player['playerAugment3']}",
            "{player['playerAugment4']}",
            "{player['playerScore0']}",
            "{player['playerScore1']}",
            "{player['playerScore10']}",
            "{player['playerScore11']}",
            "{player['playerScore2']}",
            "{player['playerScore3']}",
            "{player['playerScore4']}",
            "{player['playerScore5']}",
            "{player['playerScore6']}",
            "{player['playerScore7']}",
            "{player['playerScore8']}",
            "{player['playerScore9']}",
            "{player['playerSubteamId']}",
            "{player['profileIcon']}",
            "{player['pushPings']}",
            "{player['puuid']}",
            "{player['quadraKills']}",
            "{player['riotIdGameName']}",
            "{player['riotIdTagline']}",
            "{player['role']}",
            "{player['sightWardsBoughtInGame']}",
            "{player['spell1Casts']}",
            "{player['spell2Casts']}",
            "{player['spell3Casts']}",
            "{player['spell4Casts']}",
            "{player['subteamPlacement']}",
            "{player['summoner1Casts']}",
            "{player['summoner1Id']}",
            "{player['summoner2Casts']}",
            "{player['summoner2Id']}",
            "{player['summonerId']}",
            "{player['summonerLevel']}",
            "{player['summonerName']}",
            "{player['teamEarlySurrendered']}",
            "{player['teamId']}",
            "{player['teamPosition']}",
            "{player['timeCCingOthers']}",
            "{player['timePlayed']}",
            "{player['totalAllyJungleMinionsKilled']}",
            "{player['totalDamageDealt']}",
            "{player['totalDamageDealtToChampions']}",
            "{player['totalDamageShieldedOnTeammates']}",
            "{player['totalDamageTaken']}",
            "{player['totalEnemyJungleMinionsKilled']}",
            "{player['totalHeal']}",
            "{player['totalHealsOnTeammates']}",
            "{player['totalMinionsKilled']}",
            "{player['totalTimeCCDealt']}",
            "{player['totalTimeSpentDead']}",
            "{player['totalUnitsHealed']}",
            "{player['tripleKills']}",
            "{player['trueDamageDealt']}",
            "{player['trueDamageDealtToChampions']}",
            "{player['trueDamageTaken']}",
            "{player['turretKills']}",
            "{player['turretTakedowns']}",
            "{player['turretsLost']}",
            "{player['unrealKills']}",
            "{player['visionClearedPings']}",
            "{player['visionScore']}",
            "{player['visionWardsBoughtInGame']}",
            "{player['wardsKilled']}",
            "{player['wardsPlaced']}",
            "{player['win']}"
            )"""
        cur.execute(statment)
    cur.execute("COMMIT;")
    con.close()