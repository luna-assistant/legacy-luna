# luna/server/main/views.py

from flask_login import login_required, current_user
from flask import render_template, Blueprint, redirect, url_for, flash, request
from luna.server.models import Role
from luna.server.main.forms import NewModuleForm
from luna.server.repositories import ModuleRepository
from collections import defaultdict

main_blueprint = Blueprint('main', __name__,)


@main_blueprint.before_request
def admin_not_welcome():
    if current_user.is_authenticated and current_user.has_role(Role.ADMIN):
        return redirect(url_for('admin.index'))


@main_blueprint.route('/')
@login_required
def dashboard():
    person_id = current_user.person.id if current_user.has_role(Role.COMMON) else current_user.person.associated_to.id
    modules = ModuleRepository().allByPerson(person_id)
    modules_by_room = defaultdict(list)
    for module in modules:
        modules_by_room[module.room].append(module)
    return render_template('main/dashboard.html',form=NewModuleForm(),modules_by_room=modules_by_room)


@main_blueprint.route('/modulo/adicionar', methods=['POST'])
@login_required
def module_add():
    form = NewModuleForm()

    if form.validate_on_submit():
        module_repository = ModuleRepository()
        module = module_repository.findByIdentifier(form.identifier.data)

        form.populate_obj(module)

        module.person_id = current_user.person.id

        module_repository.update(module.id, module)

        flash('Módulo adicionado com sucesso!', 'success')
    return redirect(url_for('main.dashboard'))


@main_blueprint.route('/pedido', methods=['POST'])
@login_required
def help():
    flash('Pedido de ajuda enviado à todos os associados. Aguente firme!', 'success')
    return redirect(url_for('main.dashboard'))
