from wtforms import Form, EmailField
from wtforms import StringField, IntegerField, BooleanField ,PasswordField, RadioField, SelectMultipleField, widgets

from wtforms import validators

class UserForm(Form):
    matricula = IntegerField('Matricula', [validators.DataRequired(message='El campo es requerido')])
    nombre = StringField('Nombre', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=1, max=50)])
    apellido = StringField('Apellido', [validators.DataRequired(message='El campo es requerido'), validators.Length(min=1, max=50)])
    email = EmailField('Correo', [validators.Email(message='Ingrese un correo valido'),])

class Distacia(Form):
    x1 = IntegerField('x1', [validators.DataRequired(message='Ingrese un numero valido')])
    y1 = IntegerField('y1', [validators.DataRequired(message='Ingrese un numero valido')])
    x2 = IntegerField('x2', [validators.DataRequired(message='Ingrese un numero valido')])
    y2 = IntegerField('y2', [validators.DataRequired(message='Ingrese un numero valido')])

class Pizzas(Form):
    nombreP = StringField('Nombre', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=1, max=50)
    ])
    direccionP = StringField('Dirección', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=1, max=50)
    ])
    telefonoP = StringField('Teléfono', [
        validators.DataRequired(message='El campo es requerido'),
        validators.Length(min=1, max=50)
    ])
    numPizzasP = IntegerField('Cantidad', [
        validators.DataRequired(message='Ingrese un número válido')
    ])

    tamP = RadioField('Tamaño', 
        choices=[
            ('chica', 'Chica $40'),
            ('mediana', 'Mediana $80'),
            ('grande', 'Grande $120')
        ],
        validators=[validators.DataRequired(message='Seleccione un tamaño')]
    )

    ingP = SelectMultipleField('Ingredientes',
        choices=[
            ('jamon', 'Jamón $10'),
            ('pina', 'Piña $10'),
            ('champi', 'Champiñones $10')
        ],
        option_widget=widgets.CheckboxInput(),
        widget=widgets.ListWidget(prefix_label=False)
    )