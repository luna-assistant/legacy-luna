# luna/server/user/forms.py


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', [DataRequired()])
    password = PasswordField('Senha', [DataRequired()])


class RegisterForm(FlaskForm):
    module = StringField(
        'Identificador do Módulo',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    username = StringField(
        'Nome do Usuário',
        validators=[
            DataRequired(),
            Length(min=6, max=40)
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
            EqualTo('password', message='A confirmação deve ser igual à senha informada.')
        ]
    )
