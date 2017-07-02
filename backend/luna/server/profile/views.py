from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required
from luna.server.profile.forms import PersonForm

profile_blueprint = Blueprint('profile', __name__,)


@profile_blueprint.route('/perfil', methods=['GET', 'POST'])
@login_required
def profile():
    form = PersonForm(request.form)
    if form.validate_on_submit():
        pass
    return render_template('profile/form.html', form=form)
