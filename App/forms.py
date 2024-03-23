
from flask_wtf import FlaskForm
from wtforms.fields import (TextAreaField, SubmitField, StringField,
                            PasswordField, SelectField, MultipleFileField, HiddenField)
from wtforms import FloatField, BooleanField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo,NumberRange
from flask_wtf.file import FileRequired, FileField, DataRequired
from . import db
from .models import Teams


class Testform(FlaskForm):
    user_name = StringField('Name')
    email = StringField('Email Address')
    sumbit = SubmitField('submit')

class APIKey(FlaskForm):
    sumbit = SubmitField('submit')

class MatchID(FlaskForm):
    Players = SelectField(u'Players', coerce=str, validators=[InputRequired('Please select a player')])
    Submit = SubmitField('Submit', validators=[InputRequired()])

class MusicUpload(FlaskForm):
    Title = StringField('Title', validators=[InputRequired('A Title is required!')])
    Audio = FileField('Audio', validators=[FileRequired('Audio is required!')])
    Author = StringField('Author', validators=[InputRequired("An author is required!")])
    Submit = SubmitField('Submit', validators=[InputRequired()])

class TeamRegister(FlaskForm):
    Name=StringField("Team Name", validators=[InputRequired('Enter Team Name')])
    Abbreviation=StringField("Team Abbreviation", validators=[InputRequired('Enter Team Abbreviation')])
    Description=StringField("Team Description", validators=[InputRequired('Enter Team Description')])
    Colour = StringField('Colour', validators=[FileRequired('A Colour is required!')])
    LogoBlue = FileField('LogoBlue', validators=[FileRequired('A Logo Blue is required!')])
    LogoRed = FileField('LogoRed', validators=[FileRequired('A Logo Red is required!')])
    Submit = SubmitField('Submit', validators=[InputRequired()])

class ROLF(FlaskForm):
    Rolf = FileField('ROLF', validators=[FileRequired('ROLF file is required!')])
    Submit = SubmitField('Submit', validators=[InputRequired()])

class TournementRegister(FlaskForm):
    Name=StringField("Tournement Name", validators=[InputRequired("Enter Tournment Name")])
    Submit = SubmitField('Submit', validators=[InputRequired()])

class CasterRegister(FlaskForm):
    Name=StringField("Caster Name", validators=[InputRequired('Enter Caster Name')])
    Subheading=StringField("Caster Subheading")
    Submit = SubmitField('Submit', validators=[InputRequired()])

class MatchRegister(FlaskForm):
    Tournament = SelectField(u'Tournament', coerce=str)
    Team1 = SelectField(u'Team1', coerce=str)
    Team2 = SelectField(u'Team2', coerce=str)
    Team1name = HiddenField()
    Team2name = HiddenField()
    Time = StringField("Time", validators=[InputRequired('Please select a team')])
    Format = StringField("Format", validators=[InputRequired('Please select a team')])
    enoughPlayers = SelectField(u'Require All Players', choices=[(True, 'True'), (False, 'False')])
    mapType = SelectField(u'Map', choices=[('SUMMONERS_RIFT', 'Summoners Rift'), ('HOWLING_ABYSS', 'Howling Abyss')])
    pickType = SelectField(u'Draft', choices=[('TOURNAMENT_DRAFT', 'Tournament Draft'), ('DRAFT_MODE', 'Draft Mode'), ('ALL_RANDOM', 'All Random'), ('BLIND_PICK', 'Blind Pick')])
    spectatorType = SelectField(u'Spectaors', choices=[('ALL', 'All'), ('LOBBYONLY', 'Lobby Only'), ('NONE', 'None')])
    teamSize = SelectField(u'Team size', choices=[(5, 5), (2, 2), (3, 3), (4, 4), (1, 1)])

class PlayerRegister(FlaskForm):
    Name=StringField("Player Name", validators=[InputRequired('Enter Player Name')])
    Team = SelectField(u'Team', coerce=str)
    Submit = SubmitField('Submit', validators=[InputRequired()])

ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'BMP'}
class Bid(FlaskForm):
    Price = IntegerField('Your Bid', validators=[InputRequired("A bid is required!")])
    Submit = SubmitField('Submit', validators=[InputRequired()])
