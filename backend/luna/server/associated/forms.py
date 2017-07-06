from luna.server.profile.forms import PersonForm
from wtforms import BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo


class AssociatedForm(PersonForm):
    create_user = BooleanField('Criar Usuário')
    # username = StringField('Nome de Usuário', [Length(min=6, max=40)])
    # password = PasswordField('Senha', [Length(min=6, max=40)])
    # confirm = PasswordField(
    #     'Confirmação',
    #     validators=[
    #         DataRequired(),
    #         EqualTo(
    #             'password', message='A confirmação deve ser igual à senha informada.')
    #     ]
    # )
