# luna/server/main/views.py


#################
#### imports ####
#################

from flask_login import login_required, current_user
from flask import render_template, Blueprint, redirect, url_for
from luna.server.models import Role


################
#### config ####
################

main_blueprint = Blueprint('main', __name__,)

@main_blueprint.before_request
def admin_not_welcome():
    if current_user.is_authenticated and current_user.has_role(Role.ADMIN):
        return redirect(url_for('admin.index'))


################
#### routes ####
################

@main_blueprint.route('/')
@login_required
def dashboard():
    return render_template('main/dashboard.html')

