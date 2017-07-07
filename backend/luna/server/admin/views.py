from flask import Blueprint, json, current_app
from flask.views import MethodView
from flask_login import current_user
from luna.server.models import Role


admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.before_request
def admin_required():
    if not current_user.is_authenticated or not current_user.has_role(Role.ADMIN):
        return current_app.login_manager.unauthorized()
