import json
import requests
import os
from dotenv import load_dotenv
load_dotenv()
global RIOT_KEY
RIOT_KEY = os.environ['RIOT_KEY']

def account_Puuid_by_riot_name(Name, Tag):
    return requests.get('https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/'+Name+'/'+Tag+"?api_key="+RIOT_KEY).json()

def game_IDs_by_account_Puuid(puuid):
    return requests.get('https://sea.api.riotgames.com/lol/match/v5/matches/by-puuid/'+puuid+'/ids?type=tourney&start=0&count=1&api_key='+RIOT_KEY).json()

def game_stats_by_game_ID(MatchID):
    return requests.get('https://sea.api.riotgames.com/lol/match/v5/matches/'+MatchID+"?api_key="+RIOT_KEY).json()

def CreateTournament(ProviderID):
    return None

def CreateTournamentCode(TournamentID, NumCodes, Config={"enoughPlayers": True,"pickType": "TOURNAMENT_DRAFT","spectatorType": "ALL","teamSize": 5}):
    return requests.post("https://americas.api.riotgames.com/lol/tournament/v5/codes?tournamentId="+TournamentID+"&count="+NumCodes+"&api_key="+RIOT_KEY, data=Config).json()

def GetGameDetails(TournamentCode):
    return None

def GetLobbyEvents(TournamentCode):
    return None