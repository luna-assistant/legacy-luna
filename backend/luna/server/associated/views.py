from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required
from luna.server.associated.forms import AssociatedForm

associated_blueprint = Blueprint('associated', __name__,)

@associated_blueprint.route('/associados', methods=['GET', 'POST'])
@login_required
def associated():
    return render_template('associated/form.html')
