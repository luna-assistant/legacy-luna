from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from luna.server.validators import CPF
from luna.server.repositories import PersonRepository, ModuleTypeRepository
from brazilnum.util import clean_id
from flask_login import current_user


module_type_repository = ModuleTypeRepository()


class NewModuleForm(FlaskForm):
    identifier = StringField('Identificador', [DataRequired()])
    name = StringField('Nome', [DataRequired()])
    room = StringField('Cômodo', [DataRequired()])
    module_type = StringField('Tipo', [DataRequired()])
