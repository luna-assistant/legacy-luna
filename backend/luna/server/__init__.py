# luna/server/__init__.py


#################
#### imports ####
#################

import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension

from peewee import PostgresqlDatabase


################
#### config ####
################

app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)


app_settings = os.getenv('APP_SETTINGS', 'luna.server.config.DevelopmentConfig')
app.config.from_object(app_settings)


####################
#### extensions ####
####################

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
toolbar = DebugToolbarExtension(app)


####################
######## db ########
####################

db = PostgresqlDatabase(
    app.config.get('DB_DATABASE'),
    user=app.config.get('DB_USERNAME'),
    password=app.config.get('DB_PASSWORD'),
    host=app.config.get('DB_HOST'),
    port=app.config.get('DB_PORT')
)

# This hook ensures that a connection is opened to handle any queries
# generated by the request.
@app.before_request
def _db_connect():
    db.connect()

# This hook ensures that the connection is closed when we've finished
# processing the request.
@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


###################
### blueprints ####
###################

from luna.server.auth.views import auth_blueprint
from luna.server.main.views import main_blueprint
from luna.server.profile.views import profile_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(profile_blueprint)


###################
### flask-login ####
###################

from luna.server.repositories import UserRepository

login_manager.login_view = "auth.login"
login_manager.login_message_category = 'danger'


@login_manager.user_loader
def load_user(username):
    return next(UserRepository().findByField('username', username), None)


########################
#### error handlers ####
########################

@app.errorhandler(401)
def unauthorized_page(error):
    return render_template("errors/401.html"), 401


@app.errorhandler(403)
def forbidden_page(error):
    return render_template("errors/403.html"), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@app.errorhandler(500)
def server_error_page(error):
    return render_template("errors/500.html"), 500
