# luna/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    email = EmailField(
        'Email', [
            DataRequired(message = 'O campo Email é obrigatório'),
            Email(message = 'Por favor, informe um email válido')
        ]
    )
    password = PasswordField('Senha', [DataRequired(message = 'O campo Senha é obrigatório')])


class NewPasswordForm(FlaskForm):
    email = EmailField(
        'Email do Usuário',
        validators=[
            DataRequired(message = 'O campo Email é obrigatório'),
            Length(min=10)
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
            Email(message = 'Por favor, informe um email válido')
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
