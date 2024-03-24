from flask import Blueprint, render_template, request, flash, redirect, url_for, make_response,session
from flask_login import login_user, login_required, logout_user
from ..forms import MusicUpload, Bid, TeamRegister, CasterRegister, PlayerRegister, MatchRegister, ROLF, APIKey, Login
from ..models import Item, Music, Teams, Casters, Players, Match, ROLFFile, User
from .. import db
from ..Streams import Stream, Headings
from ..replay_metadata import *
from sqlalchemy import *
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from ..Streams import Stream, Headings
import os
headings = Headings
bp = Blueprint('LoginBP', __name__)

@bp.route('/signup')
@login_required
def signup():
    return render_template('Login/Signup.html')

@bp.route('/signup', methods=['POST'])
@login_required
def signup_post():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first() # if this returns a user, then the email already exists in database
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return redirect(url_for('/Signup'))
    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(username=username, password=generate_password_hash(password, method='scrypt'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect('/login')

@bp.route('/login')
def login():
    form = Login()
    return render_template('Login/Login.html', form=form)

@bp.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(username=username).first()
    if user == None:
        print('This 1', flush=True)
        return redirect('/login')
        
    if not check_password_hash(user.password, password):
        print('This 2', flush=True)
        return redirect('/login')

    session['username']=username
    login_user(user, remember=remember)
    return redirect('/')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')