# luna/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from luna.server.validators import CPF
from luna.server.repositories import UserRepository
from luna.server.repositories import PersonRepository
from brazilnum.util import clean_id
from flask_login import current_user

def unique_username(message='O campo informado já existe'):

    def _unique_username(form, field):
        user = UserRepository().findByUsername(field.data)
        if user:
            raise ValidationError(message)

    return _unique_username



class LoginForm(FlaskForm):
    email = EmailField(
        'Email', [
            DataRequired(message = 'O campo Email é obrigatório'),
            Email(message = 'Por favor, informe um email válido')
        ]
    )
    password = PasswordField('Senha', [DataRequired(message = 'O campo Senha é obrigatório')])


class NewPasswordForm(FlaskForm):
    cpf = StringField('CPF', [
        DataRequired(),
        Length(max=14),
        CPF()
    ])
    password = PasswordField(
        'Nova senha',
        validators=[DataRequired(message='O campo Senha é obrigatório'), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirmação',
        validators=[
            DataRequired(message='O campo de confirmação da senha é obrigatório'),
            EqualTo(
                'password', message='A confirmação deve ser igual à senha informada.')
        ]
    )


class RegisterForm(FlaskForm):
    module = StringField(
        'Identificador do Módulo',
        validators=[
            DataRequired(message = 'O campo Identificado do Módulo é obrigatório'),
            Length(min=6)
        ]
    )
    email = EmailField(
        'Email', [
            DataRequired(message = 'O campo Email é obrigatório'),
            Email(message = 'Por favor, informe um email válido'),
            unique_username(message='Esse Email já foi cadastrado')
        ]
    )
    password = PasswordField(
        'Senha',
        validators=[DataRequired(message = 'O campo Senha é obrigatório'), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirmação',
        validators=[
            DataRequired(message = 'O campo de confirmação da senha é obrigatório'),
            EqualTo(
                'password', message='A confirmação deve ser igual à senha informada.')
        ]
    )
