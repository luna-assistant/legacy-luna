from flask_wtf import FlaskForm
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length, Email
from luna.server.validators import CPF


class PersonForm(FlaskForm):
    name = StringField('Nome', [
        DataRequired(),
        Length(max=100)
    ])
    cpf = StringField('CPF', [
        DataRequired(),
        Length(max=14),
        CPF()
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
    city_id = StringField('Munícipio')  # TODO: ChoiceField
    

