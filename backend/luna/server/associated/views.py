from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user
from luna.server.associated.forms import AssociatedForm
from luna.server.models import Person
from luna.server.repositories import PersonRepository, PeopleAssociatedRepository
from brazilnum.util import clean_id


associated_blueprint = Blueprint('associated', __name__,)

person_repository = PersonRepository()
person_associated_repository = PeopleAssociatedRepository()

@associated_blueprint.route('/associados', methods=['GET', 'POST'])
@login_required
def associated():
    form = AssociatedForm()
    return render_template('associated/form.html',form=form)


@associated_blueprint.route('/associados/adicionar', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return redirect(url_for('associated.associated'))

    form = AssociatedForm()

    if form.validate_on_submit():

        person = Person()

        form.populate_obj(person)
        person.cpf = clean_id(person.cpf)

        person = dict(person)
        person['emails'] = [form.email.data]

        person = person_repository.create(person)
        person_associated_repository.create(dict(person_id=current_user.person().id, associated_id=person.id))

        flash('Associado adicionado com sucesso!', 'success')


    return render_template('associated/form.html', form=form)

@associated_blueprint.route('/associados/visualizar/<person_id>', methods=['GET'])
@login_required
def show(person_id):
    person = person_repository.find(person_id)
    return render_template('associated/modals/show.html', person=person)
