
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
    APIKEY = PasswordField('APIKey')
    sumbit = SubmitField('submit')

class MusicUpload(FlaskForm):
    Title = StringField('Title', validators=[InputRequired('A Title is required!')])
    Audio = FileField('Audio', validators=[FileRequired('Audio is required!')])
    Author = StringField('Author', validators=[InputRequired("An author is required!")])
    Submit = SubmitField('Submit', validators=[InputRequired()])

class TeamRegister(FlaskForm):
    Name=StringField("Team Name", validators=[InputRequired('Enter Team Name')])
    Abbreviation=StringField("Team Abbreviation", validators=[InputRequired('Enter Team Abbreviation')])
    LogoTXT = FileField('LogoTXT', validators=[FileRequired('A Logo TXT is required!')])
    LogoBL = FileField('LogoBL', validators=[FileRequired('A Logo BL is required!')])
    LogoBR = FileField('LogoBR', validators=[FileRequired('A Logo BR is required!')])
    LogoTOP = FileField('LogoTOP', validators=[FileRequired('A Logo TOP is required!')])
    Submit = SubmitField('Submit', validators=[InputRequired()])

class ROLF(FlaskForm):
    Rolf = FileField('ROLF', validators=[FileRequired('ROLF file is required!')])
    Submit = SubmitField('Submit', validators=[InputRequired()])

class CasterRegister(FlaskForm):
    Name=StringField("Caster Name", validators=[InputRequired('Enter Caster Name')])
    Subheading=StringField("Caster Subheading")
    Submit = SubmitField('Submit', validators=[InputRequired()])

class MatchRegister(FlaskForm):
    Team1 = StringField("Team1", validators=[InputRequired('Please select a team')])
    Team2 = StringField("Team1", validators=[InputRequired('Please select a team')])
    Team1name = HiddenField()
    Team2name = HiddenField()
    Time = StringField("Team1", validators=[InputRequired('Please select a team')])
    Format = StringField("Team1", validators=[InputRequired('Please select a team')])

class PlayerRegister(FlaskForm):
    Name=StringField("Player Name", validators=[InputRequired('Enter Player Name')])
    Team = StringField("Team Abbreviated", validators=[InputRequired('Team Abbreviated Name')])
    Submit = SubmitField('Submit', validators=[InputRequired()])

ALLOWED_FILE = {'png', 'jpg', 'JPG', 'PNG', 'BMP'}
class Bid(FlaskForm):
    Price = IntegerField('Your Bid', validators=[InputRequired("A bid is required!")])
    Submit = SubmitField('Submit', validators=[InputRequired()])