import io
import os
import base64
from ..models import Item, Music, Teams, Casters, Players, Match, ROLFFile
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
   stmt = select(Players.id)
   res = db.session.execute(stmt) 
   insert_string = []
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
      fig = Figure()
      axis = fig.add_subplot(111)
      Xaxis = list(range(1, len(Gold)+1))
      Title = []
      
      for i in Xaxis:
         Title.append('Game {}'.format(i))
      axis.set_title('Gold over number of games : {}'.format(player.name))
      axis.set_xlabel('Number of Games')
      axis.set_ylabel('Gold amount')
      axis.bar(Xaxis, Gold, tick_label = Title,width = 0.8, color = ['gold'])
      output = io.BytesIO()
      fig.savefig(output, format='png')
      encoded = base64.b64encode(output.getvalue()).decode('utf-8')
      FigureCanvas(fig).print_png(output)
      insert_string.append("<img src='data:image/png;base64,{}'>".format(encoded))
   print(Title)#
   return render_template("Plot.html", Plotimg=''.join(insert_string))