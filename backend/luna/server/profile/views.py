from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user
from luna.server.profile.forms import PersonForm
from luna.server.repositories import PersonRepository, CityRepository
from luna.server.models import Person, Role
from brazilnum.util import clean_id

profile_blueprint = Blueprint('profile', __name__,)
person_repository = PersonRepository()
city_repository = CityRepository()


@profile_blueprint.before_request
def admin_not_welcome():
    if current_user.is_authenticated and current_user.has_role(Role.ADMIN):
        return redirect(url_for('admin.index'))


@profile_blueprint.route('/perfil', methods=['GET', 'POST'])
@login_required
def profile():
    first_time = False
    person = person_repository.findByUser(current_user.id)
    if person is None:
        first_time = True
        person = Person(user_id=current_user.id)
    form = PersonForm(
        obj=person,
        federative_unit_id=str(person.city.federative_unit_id) if person.city else '',
        contact=next(('{}{}'.format(c.ddd, c.num) for c in person.contacts), None),
        email=next((email.email for email in person.emails), current_user.username))
    if form.federative_unit_id.data != '':
        form.city_id.choices += [
            (str(c.id), c.name)
            for c
            in city_repository.allByFederativeUnit(int(form.federative_unit_id.data), order_by=[('name',)])
        ]
    if form.validate_on_submit():
        form.populate_obj(person)
        person.cpf = clean_id(person.cpf)
        if person.postal_code:
            person.postal_code = clean_id(person.postal_code)
        person = dict(person)
        person['city_id'] = None if person['city_id'] == '' else int(person['city_id'])
        person['emails'] = [form.email.data]
        contact = clean_id(form.contact.data)
        person['contacts'] = [dict(ddd=contact[:2], num=contact[2:])]
        if person['id'] is not None:
            person_repository.update(person['id'], person)
        else:
            person_repository.create(person)
        flash('Perfil salvo com sucesso!', 'success')
        if first_time:
            return redirect(url_for('main.dashboard'))
        return redirect(url_for('profile.profile'))
    return render_template('profile/form.html', form=form)
