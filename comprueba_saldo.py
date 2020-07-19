from cryptoding_app import app#importar mi app web flask
import sqlite3#importar para usar la base de datos y hacer peticones
from flask import request

"""
if form.validate():
    conn = sqlite3.connect(app.config['BASE_DATOS'])
    cur = conn.cursor()
    Saldo = "SELECT sum(to_quantity) from compras WHERE from_quantity = '{}'".format(request.values.get('MonedaFrom'))
    cantidadFrom=cur.execute(Saldo).fetchall()
    saldoFrom = cantidadFrom[0]
    Saldo = "SELECT sum(to_currency) from compras WHERE from_currency = '{}'".format(request.values.get('MonedaFrom'))
    cantidadTo=cur.execute(Saldo).fetchall()
    saldoTo = cantidadTo[0]
    if saldoFrom[0] is not None or saldoTo[0] is not None:
        if saldoFrom[0] and saldoTo[0] is not None:
            saldo = saldoFrom[0] - saldoTo[0]
        if saldoFrom[0] == None and saldoTo[0] is not None:
            saldo = saldoTo[0]
        else:
            saldo = saldoFrom[0]
        return saldo
    Cantidad = request.values.get('Q_Form')
    if saldo > Cantidad:
        query = "INSERT INTO compras (date,time,from_currency,from_quantity,to_currency,to_quantity,P_U) values (?,?,?,?,?,?,?);"
        datos =(now.date(),time,request.values.get('MonedaFrom'), request.values.get('MonedaTo'), request.values.get('Q_Form'),round(float(form.Q_to.data), 8),round(float(form.P_U.data), 8))
    else:
        errorsaldo = ('Saldo insuficiente. No tienes suficiente cantidad de {} para comprar: {} - {}. Por favor, intentalo con una cantidad menor o con otra criptomoneda de la que disponga con más saldo.'.format(request.values.get('MonedaFrom'),request.values.get('Q_Form'),request.values.get('MonedaTo')))
        return render_template('compras.html',form=form, error_saldo=errorsaldo)
"""