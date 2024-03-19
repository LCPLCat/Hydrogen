import io
import os
import base64
from ..models import Item, Music, Teams, Casters, Players, Match, ROLFFile, MatchStas
from sqlalchemy import *
from .. import db
from flask import Response, Blueprint, render_template
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flask import Flask
import numpy as np
import string
plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True
bp = Blueprint('Plot', __name__)

@bp.route('/print-plot')
def plot_png():
   stmt = select(Players.puid)
   res = db.session.execute(stmt) 
   insert_string = []
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
      fig = Figure()
      axis = fig.add_subplot(111)
      Xaxis = list(range(1, len(Gold)+1))
      Title = []
      for i in Xaxis:
         Title.append('Game {}'.format(i))
      axis.set_title('Gold over number of games : {}'.format(player.name))
      axis.set_xlabel('Number of Games')
      axis.set_ylabel('Gold amount')
      axis.bar(Xaxis, Gold, tick_label = Title,width = 0.1, color = ['gold'])
      output = io.BytesIO()
      fig.savefig(output, format='png')
      encoded = base64.b64encode(output.getvalue()).decode('utf-8')
      FigureCanvas(fig).print_png(output)
      insert_string.append("<img src='data:image/png;base64,{}'>".format(encoded))

      fig = Figure()
      axis = fig.add_subplot(111)
      Xaxis = list(range(1, len(Deaths)+1))
      Title = []
      for i in Xaxis:
         Title.append('Game {}'.format(i))
      axis.set_title('Deaths over number of games : {}'.format(player.name))
      axis.set_xlabel('Number of Games')
      axis.set_ylabel('Deaths amount')
      axis.bar(Xaxis, Deaths, tick_label = Title,width = 0.1, color = ['black'])
      output = io.BytesIO()
      fig.savefig(output, format='png')
      encoded = base64.b64encode(output.getvalue()).decode('utf-8')
      FigureCanvas(fig).print_png(output)
      insert_string.append("<img src='data:image/png;base64,{}'>".format(encoded))

      fig = Figure()
      axis = fig.add_subplot(111)
      Xaxis = list(range(1, len(Kills)+1))
      Title = []
      for i in Xaxis:
         Title.append('Game {}'.format(i))
      axis.set_title('Kills over number of games : {}'.format(player.name))
      axis.set_xlabel('Number of Games')
      axis.set_ylabel('Kills amount')
      axis.bar(Xaxis, Kills, tick_label = Title,width = 0.1, color = ['darkred'])
      output = io.BytesIO()
      fig.savefig(output, format='png')
      encoded = base64.b64encode(output.getvalue()).decode('utf-8')
      FigureCanvas(fig).print_png(output)
      insert_string.append("<img src='data:image/png;base64,{}'>".format(encoded))

      fig = Figure()
      axis = fig.add_subplot(111)
      Xaxis = list(range(1, len(Dmg)+1))
      Title = []
      for i in Xaxis:
         Title.append('Game {}'.format(i))
      axis.set_title('Dmg over number of games : {}'.format(player.name))
      axis.set_xlabel('Number of Games')
      axis.set_ylabel('Dmg amount')
      axis.bar(Xaxis, Dmg, tick_label = Title,width = 0.1, color = ['red'])
      output = io.BytesIO()
      fig.savefig(output, format='png')
      encoded = base64.b64encode(output.getvalue()).decode('utf-8')
      FigureCanvas(fig).print_png(output)
      insert_string.append("<img src='data:image/png;base64,{}'>".format(encoded))

      fig = Figure()
      axis = fig.add_subplot(111)
      Xaxis = list(range(1, len(CreepScore)+1))
      Title = []
      for i in Xaxis:
         Title.append('Game {}'.format(i))
      axis.set_title('CreepScore over number of games : {}'.format(player.name))
      axis.set_xlabel('Number of Games')
      axis.set_ylabel('CreepScore amount')
      axis.bar(Xaxis, CreepScore, tick_label = Title,width = 0.1, color = ['darkblue'])
      output = io.BytesIO()
      fig.savefig(output, format='png')
      encoded = base64.b64encode(output.getvalue()).decode('utf-8')
      FigureCanvas(fig).print_png(output)
      insert_string.append("<img src='data:image/png;base64,{}'>".format(encoded))

      fig = Figure()
      axis = fig.add_subplot(111)
      Xaxis = list(range(1, len(Assists)+1))
      Title = []
      for i in Xaxis:
         Title.append('Game {}'.format(i))
      axis.set_title('Assists over number of games : {}'.format(player.name))
      axis.set_xlabel('Number of Games')
      axis.set_ylabel('Assists amount')
      axis.bar(Xaxis, Assists, tick_label = Title,width = 0.1, color = ['purple'])
      output = io.BytesIO()
      fig.savefig(output, format='png')
      encoded = base64.b64encode(output.getvalue()).decode('utf-8')
      FigureCanvas(fig).print_png(output)
      insert_string.append("<img src='data:image/png;base64,{}'>".format(encoded))

   print(Title)#
   return render_template("Plot.html", Plotimg=''.join(insert_string))