# project/server/__init__.py


#################
#### imports ####
#################

import os

from decouple import config
from flask import Flask, json
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


################
#### config ####
################

app = Flask(
    __name__,
    template_folder='../client/templates',
    static_folder='../client/static'
)


app_settings = config('APP_SETTINGS', 'luna.api.config.DevelopmentConfig')
app.config.from_object(app_settings)


####################
#### extensions ####
####################

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


###################
### blueprints ####
###################

from luna.api.main.views import main_blueprint
app.register_blueprint(main_blueprint)


########################
#### error handlers ####
########################

@app.errorhandler(401)
def unauthorized_page(error):
    return json.jsonify(dict(message='401: Unauthorized')), 401


@app.errorhandler(403)
def forbidden_page(error):
    return json.jsonify(dict(message='403: Forbidden')), 403


@app.errorhandler(404)
def page_not_found(error):
    return json.jsonify(dict(message='404: Page not found')), 404


@app.errorhandler(500)
def server_error_page(error):
    return json.jsonify(dict(message='500: Server error')), 500
