from cryptoding_app import app#importar mi app web flask
from flask import Flask, render_template, request, redirect, url_for, flash#importar funcionalidad flask para hacer peticiones, redirecciones,etc
import sqlite3, requests#importar para usar la base de datos y hacer peticones
from datetime import datetime#importar para usar la fecha y hora del sistema y añadir en base de datos
from flask_wtf import FlaskForm, Form#clase básica del formulario para heredar campos, tipo de campos, validaciones, etc
from wtforms import StringField, FloatField, SubmitField, HiddenField, SelectField, Field
from wtforms.validators import DataRequired, Length, ValidationError
from showing_coins_api import showing_coins


def valida_posibilidad_compra(form, field):
    #conversión posible si monedas distintas, si de EUR a BTC y si de BTC a otras criptos
    if field.data == form.from_currency.data:#solo convertir entre monedas distintas
        raise ValidationError("Solo conversión entre monedas distintas.")
        
    elif field.data != "BTC" and form.from_currency.data == "EUR":#solo convertir de EUR a BTC
        raise ValidationError("Solo conversión de EUR a BTC.")

    elif field.data == "EUR" and form.from_currency.data != "BTC":#solo convertir de BTC a otras criptomonedas
        raise ValidationError("Solo conversión de otras criptomonedas a BTC.")

    else:#si las monedas de compra son permitidas se comprueba si existe saldo y es suficiente
        conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
        cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
        query_saldo_to = "SELECT SUM(to_quantity) FROM movements WHERE to_currency = '{}'".format(request.values.get('from_currency'))
        cantidad_to=cur.execute(query_saldo_to).fetchall()#cantidad_from[0][0] es el valor float que necesito
        saldo_to = cantidad_to[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida

        
        query_saldo_from = "SELECT SUM(from_quantity) FROM movements WHERE from_currency = '{}'".format(request.values.get('from_currency'))
        cantidad_from=cur.execute(query_saldo_from).fetchall()#cantidad_from[0][0] es el valor float que necesito
        saldo_from = cantidad_from[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida

        conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES                            
        
        if saldo_to == None and saldo_from == None:#no hay saldo para invertir(saldo_to) y no hay saldo gastado(saldo_from)
            raise ValidationError("Debe comprar saldo para después invertir.")
        
        elif saldo_to != None and saldo_from == None:#hay saldo para invertir(saldo_to) pero no hay saldo gastado(saldo_from)
            if saldo_to >= float(request.values.get('from_quantity')):
                saldo_total = saldo_to
            else:
                raise ValidationError("Saldo insuficiente para invertir.")

        elif saldo_to != None and saldo_from != None:#hay saldo para invertir(saldo_to) y saldo gastado(saldo_from)
            if (saldo_to - saldo_from) >= float(request.values.get('from_quantity')):
                saldo_total = saldo_to-saldo_from     
            else:
                raise ValidationError("Saldo insuficiente.")


def validate_length(form, field):#validas campo cantidad from sea positiva
    if field.data < 0:
        raise ValidationError("Debe introducir valores positivos.")
"""
def valida_saldo(form,field):
    conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
    cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
    query_saldo_to = "SELECT SUM(to_quantity) FROM movements WHERE to_currency = '{}'".format(request.values.get('from_currency'))
    cantidad_to=cur.execute(query_saldo_to).fetchall()#cantidad_from[0][0] es el valor float que necesito
    saldo_to = cantidad_to[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida

    
    query_saldo_from = "SELECT SUM(from_quantity) FROM movements WHERE from_currency = '{}'".format(request.values.get('from_currency'))
    cantidad_from=cur.execute(query_saldo_from).fetchall()#cantidad_from[0][0] es el valor float que necesito
    saldo_from = cantidad_from[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida

    conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES                            
    
    if saldo_to == None and saldo_from == None:#no hay saldo para invertir(saldo_to) y no hay saldo gastado(saldo_from)
        raise ValidationError("Debe comprar saldo para después invertir.")
    
    elif saldo_to != None and saldo_from == None:#hay saldo para invertir(saldo_to) pero no hay saldo gastado(saldo_from)
        if saldo_to > float(request.values.get('from_quantity')):
            saldo_total = saldo_to
        else:
            raise ValidationError("Saldo insuficiente para invertir.")

    elif saldo_to != None and saldo_from != None:#hay saldo para invertir(saldo_to) y saldo gastado(saldo_from)
        if (saldo_to - saldo_from) > float(request.values.get('from_quantity')):
            saldo_total = saldo_to-saldo_from     
        else:
            raise ValidationError("Saldo insuficiente.")
"""    
    

    
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

   

