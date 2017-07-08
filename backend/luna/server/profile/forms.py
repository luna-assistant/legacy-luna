from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from luna.server.validators import CPF
from luna.server.repositories import PersonRepository
from brazilnum.util import clean_id
from flask_login import current_user


def unique_cpf(message='O campo informado já existe'):
    def _unique_cpf(form, field):
        person = PersonRepository().findByCpf(clean_id(field.data))
        if person and person.user_id != current_user.id:
            raise ValidationError(message)
    return _unique_cpf


class PersonForm(FlaskForm):
    name = StringField('Nome', [
        DataRequired(),
        Length(max=100)
    ])
    cpf = StringField('CPF', [
        DataRequired(),
        Length(max=14),
        CPF(),
        unique_cpf()
    ])
    email = StringField('Email', [
        DataRequired(),
        Email()
    ])
    birth = DateField('Data de Nascimento', format='%d/%m/%Y', validators=[
        DataRequired()
    ])
    
    facebook = StringField('Facebook')  # TODO: Facebook API
    twitter = StringField('Twitter')  # TODO: Twitter API
    
    address = StringField('Endereço')
    complement = StringField('Complemento')
    postal_code = StringField('CEP', [
        Length(max=9)
    ])
    neighborhood = StringField('Bairro')
    # city_id = StringField('Munícipio')  # TODO: ChoiceField
    

