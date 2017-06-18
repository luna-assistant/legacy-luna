# luna/server/main/views.py


#################
#### imports ####
#################

from flask_login import login_required
from flask import render_template, Blueprint


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)


################
#### routes ####
################

@main_blueprint.route('/')
@login_required
def dashboard():
    return render_template('main/dashboard.html')

