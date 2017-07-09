from flask import Blueprint, render_template, redirect, url_for, flash
from flask.views import MethodView
from flask_login import current_user
from luna.server.models import Role, ModuleType, Information, Command, Module
from luna.server.repositories import ModuleRepository, ModuleTypeRepository, \
    InformationRepository, CommandRepository
from luna.server.admin.forms import ModuleTypeForm, ModuleForm, \
    InformationForm, CommandForm


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.before_request
def admin_required():
    if not current_user.is_authenticated or \
       not current_user.has_role(Role.ADMIN):
        return redirect(url_for('main.dashboard'))


@admin_blueprint.route('/')
def index():
    return render_template('admin/index.html')


@admin_blueprint.route('modulo/<identifier>/status/atualizar')
def modules_toggle_status(identifier):
    module_repository = ModuleRepository()
    module = module_repository.findByIdentifier(identifier)
    if module is None:
        flash('Módulo não encontrado', 'error')
        return redirect(url_for('admin.modules'))

    status = module.is_active

    module.is_active = not status

    module = module_repository.update(module.id, module)

    msg = 'Ativado' if module.is_active else 'Desativado'
    flash('Módulo {} com sucesso'.format(msg), 'success')

    return redirect(url_for('admin.modules'))


class ModuleTypeAdmin(MethodView):

    module_type_repository = ModuleTypeRepository()
    information_repository = InformationRepository()
    command_repository = CommandRepository()

    def get(self, id):
        if id is not None:
            module_type = self.module_type_repository.find(id)
            if module_type is None:
                flash('Tipo de Módulo não encontrado', 'error')
                return redirect(url_for('admin.module_types'))
            form = ModuleTypeForm(obj=module_type)
            return render_template('admin/module_types/show.html',
                                   module_type=module_type,
                                   form=form)
        return render_template('admin/module_types/index.html',
                               module_types=self.module_type_repository.all(),
                               form=ModuleTypeForm())

    def post(self, id):
        if id is not None:
            return self.put(id)

        form = ModuleTypeForm()
        if form.validate_on_submit():
            module_type = ModuleType(**form.data)
            module_type = self.module_type_repository.create(module_type)
            for info in form.informations:
                information = Information(module_type_id=module_type.id)
                info.form.populate_obj(information)
                self.information_repository.create(information)
            for cmd in form.commands:
                command = Command(module_type_id=module_type.id)
                cmd.form.populate_obj(command)
                self.command_repository.create(command)
            flash('Tipo de Módulo cadastrado com sucesso', 'success')
            return redirect(url_for('admin.module_types'))
        return render_template('admin/module_types/index.html',
                               module_types=self.module_type_repository.all(),
                               form=form)

    def delete(self, id):
        return redirect(url_for('admin.module_types'))

    def put(self, id):
        module_type = self.module_type_repository.find(id)
        if module_type is None:
            flash('Tipo de Módulo não encontrado', 'error')
            return redirect(url_for('admin.module_types'))
        form = ModuleTypeForm(obj=module_type)
        if form.validate_on_submit():
            module_type = ModuleType(**{**dict(module_type), **form.data})
            module_type = self.module_type_repository.update(
                module_type.id, module_type)
            self.information_repository.deleteByModuleType(module_type.id)
            for info in form.informations:
                information = Information(module_type_id=module_type.id)
                info.form.populate_obj(information)
                self.information_repository.create(information)
            self.command_repository.deleteByModuleType(module_type.id)
            for cmd in form.commands:
                command = Command(module_type_id=module_type.id)
                cmd.form.populate_obj(command)
                self.command_repository.create(command)
            flash('Tipo de Módulo atualizado com sucesso', 'success')
            return redirect(url_for('admin.module_types'))
        return render_template('admin/module_types/index.html',
                               module_types=self.module_type_repository.all(),
                               form=ModuleTypeForm(),
                               edit_form=form,
                               module_type=module_type)


class ModuleAdmin(MethodView):

    module_repository = ModuleRepository()
    module_type_repository = ModuleTypeRepository()
    information_repository = InformationRepository()
    command_repository = CommandRepository()

    def get(self, id):
        if id is not None:
            module = self.module_repository.find(id)
            if module is None:
                flash('Módulo não encontrado', 'error')
                return redirect(url_for('admin.modules'))
            form = ModuleForm(obj=module)
            return render_template('admin/modules/show.html',
                                   module=module,
                                   form=form)
        return render_template('admin/modules/index.html',
                               modules=self.module_repository.all(),
                               form=ModuleForm())

    def post(self, id):
        if id is not None:
            return self.put(id)

        form = ModuleForm()
        print(form.data)
        if form.validate_on_submit():
            for x in range(form.quantity.data):
                module = Module(**form.data)
                self.module_repository.create(module)
            flash('Módulo(s) cadastrado(s) com sucesso', 'success')
            return redirect(url_for('admin.modules'))
        return render_template('admin/modules/index.html',
                               modules=self.module_repository.all(),
                               form=form)

    def delete(self, id):
        return redirect(url_for('admin.module_types'))

    def put(self, id):
        return redirect(url_for('admin.module_types'))


def register_admin(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    admin_blueprint.add_url_rule(url, defaults={pk: None},
                                 view_func=view_func, methods=['GET', ])
    admin_blueprint.add_url_rule(url, defaults={pk: None},
                                 view_func=view_func, methods=['POST', ])
    admin_blueprint.add_url_rule('%s<%s:%s>' % (url, pk_type, pk),
                                 view_func=view_func,
                                 methods=['GET', 'POST', 'PUT', 'DELETE'])


register_admin(ModuleTypeAdmin, 'module_types', '/tipo_modulo/')
register_admin(ModuleAdmin, 'modules', '/modulo/')
