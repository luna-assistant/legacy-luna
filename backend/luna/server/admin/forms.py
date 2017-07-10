from flask_wtf import FlaskForm
from wtforms import StringField, DateField, IntegerField, TextAreaField, SelectField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from luna.server.validators import CPF
from luna.server.repositories import PersonRepository, InformationTypeRepository, CommandTypeRepository ,\
    ModuleTypeRepository
from brazilnum.util import clean_id
from flask_login import current_user


module_type_repository = ModuleTypeRepository()
information_type_repo = InformationTypeRepository()
information_type_repo = InformationTypeRepository()
command_type_repo = CommandTypeRepository()


class InformationForm(FlaskForm):
    name = StringField('Nome', [DataRequired(message='Nome da Informação não pode ficar vazio.')])
    identifier = IntegerField('Identificador', [DataRequired(message='Identificador da Informação não pode ficar vazio.')])
    description = StringField('Descrição')
    information_type_id = SelectField('Tipo', coerce=int, choices=[(t.id, t.description) for t in information_type_repo.all()], validators=[
        DataRequired(message='Especifique o tipo, por favor.')
    ])


class CommandForm(FlaskForm):
    name = StringField('Nome', [DataRequired(message='Nome do Comando não pode ficar vazio.')])
    identifier = IntegerField('Identificador', [DataRequired(message='Identificador do Comando não pode ficar vazio.')])
    description = StringField('Descrição')
    command_type_id = SelectField('Tipo', coerce=int, choices=[(t.id, t.description) for t in command_type_repo.all()], validators=[
        DataRequired(message='Especifique o tipo, por favor.')
    ])


class ModuleTypeForm(FlaskForm):
    name = StringField('Nome', [DataRequired(message='Nome não pode ficar vazio.')])
    description = TextAreaField('Descrição')
    icon = StringField('Ícone', [DataRequired(message='Especifique um ícone, por favor.')])
    informations = FieldList(FormField(InformationForm), min_entries=1)
    commands = FieldList(FormField(CommandForm), min_entries=1)
    is_active = BooleanField('Já está disponível?', default=True)


class ModuleForm(FlaskForm):
    quantity = IntegerField('Quantidade', [DataRequired(message='Quantidade não pode ficar vazio.')], default=1)
    module_type_id = SelectField('Tipo', coerce=int, choices=[(t.id, t.name) for t in module_type_repository.all()], validators=[
        DataRequired(message='Especifique o tipo, por favor.')
    ])
