#import flask - from the package import class
from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import Blueprint, render_template, request
db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
    
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='utroutoru'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///auction_alchemy.db'
    #initialize db with flask app
    
    db.init_app(app)

    bootstrap = Bootstrap(app)
    UPLOAD_FOLDER = '/static/img'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'LoginBP.login'
    login_manager.init_app(app)
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)

    #create a user loader function takes userid and returns User# importing here to avoid circular references
    
    @app.errorhandler(403)
    def forbidden(error):
        return render_template('Errors/forbidden.html', title = '403'), 403
    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('Errors/pagenotfound.html', title = '404'), 404
    @app.errorhandler(410)
    def page_gone(error):
        return render_template('Errors/gone.html', title = '410'), 410
    @app.errorhandler(500)
    def internal_error(error):
        return render_template('Errors/internalservererror.html', title = '500'), 500

    app.register_error_handler(403, forbidden)
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(410, page_gone)
    app.register_error_handler(500, internal_error)

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import Main 
    from .BluePrints import MatchesBP, CastersBP, MusicBP, PlayersBP, TeamsBP, ROLFBP, Plot, RiotAPIBP, TournementsBP, LoginBP
    app.register_blueprint(Main.bp)
    app.register_blueprint(ROLFBP.bp)
    app.register_blueprint(MatchesBP.bp)
    app.register_blueprint(CastersBP.bp)
    app.register_blueprint(MusicBP.bp)
    app.register_blueprint(PlayersBP.bp)
    app.register_blueprint(TeamsBP.bp)
    app.register_blueprint(Plot.bp)
    app.register_blueprint(RiotAPIBP.bp)
    app.register_blueprint(TournementsBP.bp)
    app.register_blueprint(LoginBP.bp)
    return app

