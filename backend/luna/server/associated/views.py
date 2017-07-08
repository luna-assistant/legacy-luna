from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user
from luna.server.associated.forms import AssociatedForm
from luna.server.models import Person, User
from luna.server.repositories import PersonRepository, PeopleAssociatedRepository, \
    UserRepository
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
        phone = clean_id(form.contact.data)

        person = dict(person)
        person['emails'] = [form.email.data]
        person['contacts'] = [{
            'ddd': phone[0:2],
            'num': phone[2:]
        }]


        if form.create_user.data:
            user = User(
                username=form.email.data,
                password='mudar@123'
            )

            user = UserRepository().create(user)

            person['user_id'] = user.id

        person = person_repository.create(person)
        person_associated_repository.create(dict(person_id=current_user.person.id, associated_id=person.id))

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
        email = next(person.emails, None)
        form.email.data = email.email if email else ''
        contact = next(person.contacts, None)
        form.contact.data = '{}{}'.format(contact.ddd, contact.num) if contact else ''
        return render_template('associated/modals/edit.html', form=form, person_id=person_id)

    if form.validate_on_submit():
        form.populate_obj(person)

        person.cpf = clean_id(person.cpf)
        phone = clean_id(form.contact.data)

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
        return render_template('associated/form.html',form=form, person_id=person_id, error_edit=True)

    return redirect(url_for('associated.index'))

@associated_blueprint.route('/associados/excluir/<associated_id>', methods=['GET', 'POST'])
@login_required
def delete(associated_id):

    person_id = current_user.person.id
    person = person_repository.find(associated_id)

    if request.method == 'GET':
        return render_template('associated/modals/delete.html', person=person, person_id=associated_id)

    if request.method == 'POST':
        person_associated_repository.deleteAssociation(person_id, associated_id)

        if not person.user_id:
            person_repository.delete(associated_id)

        flash('Associado removido com sucesso!', 'success')

    return redirect(url_for('associated.index'))
