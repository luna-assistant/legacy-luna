from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required

profile_blueprint = Blueprint('profile', __name__,)

@profile_blueprint.route('/perfil', methods=['GET', 'POST'])
def profile():
    return redirect(url_for("main.dashboard"))
    
