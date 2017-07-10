# luna/server/main/views.py

from flask_login import login_required, current_user
from flask import render_template, Blueprint, redirect, url_for
from luna.server.models import Role
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
    return render_template('main/dashboard.html', modules_by_room=modules_by_room)
