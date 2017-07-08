from flask import Blueprint, render_template, redirect, url_for
from flask.views import MethodView
from flask_login import current_user
from luna.server.models import Role


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.before_request
def admin_required():
    if not current_user.is_authenticated or not current_user.has_role(Role.ADMIN):
        return redirect(url_for('main.dashboard'))


@admin_blueprint.route('/')
def index():
    return render_template('admin/index.html')


class ModuleTypeAdmin(MethodView):

    def get(self, id):
        return render_template('admin/module_types/index.html')

    def post(self):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass


class ModuleAdmin(MethodView):

    def get(self, id):
        return render_template('admin/index.html')

    def post(self):
        pass

    def delete(self, id):
        pass

    def put(self, id):
        pass


def register_admin(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    admin_blueprint.add_url_rule(url, defaults={pk: None},
                                 view_func=view_func, methods=['GET', ])
    admin_blueprint.add_url_rule(url, view_func=view_func, methods=['POST', ])
    admin_blueprint.add_url_rule('%s<%s:%s>' % (url, pk_type, pk),
                                 view_func=view_func,
                                 methods=['GET', 'PUT', 'DELETE'])


register_admin(ModuleTypeAdmin, 'module_types', '/tipo_modulo/')
register_admin(ModuleAdmin, 'modules', '/modulo/')
