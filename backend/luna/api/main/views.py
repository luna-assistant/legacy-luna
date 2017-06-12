# project/server/main/views.py


#################
#### imports ####
#################

from flask import Blueprint, json


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################


@main_blueprint.route('/')
def version():
    return json.jsonify(dict(version='0.1.0'))
