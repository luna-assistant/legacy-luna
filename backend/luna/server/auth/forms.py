# luna/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    email = EmailField(
        'Email', [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Senha', [DataRequired()])


class NewPasswordForm(FlaskForm):
    email = EmailField(
        'Email do Usuário',
        validators=[
            DataRequired(),
            Length(min=10)
        ]
    )


class RegisterForm(FlaskForm):
    module = StringField(
        'Identificador do Módulo',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    email = EmailField(
        'Email', [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField(
        'Senha',
        validators=[DataRequired(), Length(min=6, max=25)]
    )
    confirm = PasswordField(
        'Confirmação',
        validators=[
            DataRequired(),
            EqualTo(
                'password', message='A confirmação deve ser igual à senha informada.')
        ]
    )
