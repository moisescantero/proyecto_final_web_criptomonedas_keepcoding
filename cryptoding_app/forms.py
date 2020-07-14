from flask_wtf import FlaskForm, Form#clase básica del formulario para heredar campos, tipo de campos, validaciones, etc
from wtforms import StringField, FloatField, SubmitField, HiddenField, SelectField, Field
from wtforms.validators import DataRequired, Length, ValidationError
from listing_using_api import showing_coins, listing_cryptos
from conversion_using_api import find_cryptos

def valida_posibilidad_compra(form, field):
    if field.data == form.from_currency.data:#solo convertir entre monedas distintas
        raise ValidationError("Solo conversión entre monedas distintas.")
    elif field.data != "BTC" and form.from_currency.data == "EUR":#solo convertir de EUR a BTC
        raise ValidationError("Solo conversión de EUR a BTC.")
    elif field.data == "EUR" and form.from_currency.data != "BTC":#solo convertir de BTC a otras criptomonedas
        raise ValidationError("Solo conversión de otras criptomonedas a BTC.")



def validate_length(form, field):#validas campo cantidad from sea positiva
    if field.data < 0:
        raise ValidationError("Debe introducir valores positivos.")


coins_list = showing_coins()

class ProductForm(FlaskForm):
    id = HiddenField('id')
    
    from_currency = SelectField(u"Moneda de origen:", choices=[(coin, coin) for coin in coins_list])#en variable from_currency definir lista
                #desplegable con valores de criptomonedas

    from_quantity = FloatField("Cantidad invertida: ", validators=[DataRequired(message="Debe introducir números."), validate_length])#campo para cantidad definido con float y validado como requerido
    
    to_currency = SelectField(u"Moneda de destino:", choices=[(coin, coin) for coin in coins_list], validators=[valida_posibilidad_compra])
                #lista desplegable para moneda destino con valores de coins_list y con validator específico
    
    to_quantity = HiddenField("Cantidad obtenida: ")
    unit_price = HiddenField("Precio unitario: ")

    calc_button = SubmitField("Calcular")
    accept_button = SubmitField("Aceptar")
    cancel_button = SubmitField("Cancelar")

   

