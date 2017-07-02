from wtforms.validators import ValidationError
from brazilnum.cpf import validate_cpf


class CPF(object):
    
    def __init__(self, message=None):
        if not message:
            message = 'Field must be a valid CPF'
        self.message = message
    
    def __call__(self, form, field):
        if field.data and not validate_cpf(field.data):
            raise ValidationError(self.message)