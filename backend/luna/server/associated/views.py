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
def index():
    form = AssociatedForm()
    return render_template('associated/form.html',form=form)


@associated_blueprint.route('/associados/adicionar', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'GET':
        return redirect(url_for('associated.index'))

    form = AssociatedForm()

    if form.validate_on_submit():
                
        person = Person()

        form.populate_obj(person)
        person.cpf = clean_id(person.cpf)
        phone = clean_id(form.contacts.data)

        person = dict(person)
        person['emails'] = [form.email.data]
        person['contacts'] = [{
            'ddd': phone[0:2],
            'num': phone[2:]
        }]

        person = person_repository.create(person)
        person_associated_repository.create(dict(person_id=current_user.person().id, associated_id=person.id))

        flash('Associado adicionado com sucesso!', 'success')


    return render_template('associated/form.html', form=form)

@associated_blueprint.route('/associados/visualizar/<person_id>', methods=['GET'])
@login_required
def show(person_id):
    person = person_repository.find(person_id)
    return render_template('associated/modals/show.html', person=person)

@associated_blueprint.route('/associados/editar/<person_id>', methods=['GET', 'POST'])
@login_required
def edit(person_id):

    person = person_repository.find(person_id)
    form = AssociatedForm(obj=person)

    if request.method == 'GET':
        form.email.data = next(person.emails()).email
        contact = next(person.contacts()) if person.contacts() != None else ''
        form.contacts.data = contact.ddd + contact.num if contact else ''
        return render_template('associated/modals/edit.html', form=form, person_id=person_id)

    if form.validate_on_submit():
        form.populate_obj(person)

        person.cpf = clean_id(person.cpf)
        phone = clean_id(form.contacts.data)

        person = dict(person)
        person['emails'] = [form.email.data]
        person['contacts'] = [{
            'ddd': phone[0:2],
            'num': phone[2:]
        }]

        person = person_repository.update(person_id, person)

        flash('Associado atualizado com sucesso!', 'success')
    else:
        print(form.errors)
        return render_template('associated/form.html',form=form, person_id=person_id)

    return redirect(url_for('associated.index'))
