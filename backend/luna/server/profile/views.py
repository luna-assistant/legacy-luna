from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user
from luna.server.profile.forms import PersonForm
from luna.server.repositories import PersonRepository
from luna.server.models import Person
from brazilnum.util import clean_id

profile_blueprint = Blueprint('profile', __name__,)
person_repository = PersonRepository()


@profile_blueprint.route('/perfil', methods=['GET', 'POST'])
@login_required
def profile():
    person = person_repository.findByUser(current_user.id)
    if person is None:
        person = Person(user_id=current_user.id)
    form = PersonForm(obj=person, email=next(
        (email.email for email in person.emails), current_user.username))
    if form.validate_on_submit():
        form.populate_obj(person)
        person.cpf = clean_id(person.cpf)
        if person.postal_code:
            person.postal_code = clean_id(person.postal_code)
        person = dict(person)
        person['emails'] = [form.email.data]
        if person['id'] is not None:
            person_repository.update(person['id'], person)
        else:
            person_repository.create(person)
        flash('Perfil salvo com sucesso!', 'success')
        return redirect(url_for('profile.profile'))
    return render_template('profile/form.html', form=form)
