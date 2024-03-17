
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
    ID = StringField('Match ID', validators=[InputRequired('A Match ID is required!')])
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

class CasterRegister(FlaskForm):
    Name=StringField("Caster Name", validators=[InputRequired('Enter Caster Name')])
    Subheading=StringField("Caster Subheading")
    Submit = SubmitField('Submit', validators=[InputRequired()])

class MatchRegister(FlaskForm):
    Match_code = StringField("Match Code")
    Team1 = StringField("Team1", validators=[InputRequired('Please select a team')])
    Team2 = StringField("Team1", validators=[InputRequired('Please select a team')])
    Team1name = HiddenField()
    Team2name = HiddenField()
    Time = StringField("Team1", validators=[InputRequired('Please select a team')])
    Format = StringField("Team1", validators=[InputRequired('Please select a team')])

class PlayerRegister(FlaskForm):
    Name=StringField("Player Name", validators=[InputRequired('Enter Player Name')])
    Team = SelectField(u'Team', coerce=str)
    Submit = SubmitField('Submit', validators=[InputRequired()])

ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'BMP'}
class Bid(FlaskForm):
    Price = IntegerField('Your Bid', validators=[InputRequired("A bid is required!")])
    Submit = SubmitField('Submit', validators=[InputRequired()])
