from cryptoding_app import app#importar mi app web flask
from flask import Flask, render_template, request, redirect, url_for, flash#importar funcionalidad flask para hacer peticiones, redirecciones,etc
import sqlite3, requests#importar para usar la base de datos y hacer peticones
from datetime import datetime#importar para usar la fecha y hora del sistema y añadir en base de datos
from wtforms.validators import ValidationError
from listing_using_api import listing_cryptos
from conversion_using_api import find_cryptos
from showing_coins_api import showing_coins
from cryptoding_app.forms import ProductForm#importar clase productform para usar formularios



@app.route("/")
def movements():
    conn = sqlite3.connect(app.config["BASE_DATOS"])#conexión a base de datos(en ficehro _config.py)
    cur = conn.cursor()#crear cursor para conexión
    
    hayregistros = ('SELECT * FROM movements')#petición query para usar dentro de la base de datos y saber si hay registros en la tabla
    registros = cur.execute(hayregistros).fetchall()#cursor ejecuta la query para comprobar si existen registros en la tabla movimientos

    if len(registros) == 0:#si no hay registros
        return render_template("without_moves.html")
    else:#si existen registros
        query = 'SELECT * FROM movements;'#petición query para usar dentro de la base de datos
        movements = cur.execute(query).fetchall()#cursor ejecuta la query para guardar en movements consultando todos los registros
        conn.close()
        return render_template("movements.html", movements=movements)

@app.route("/purchase", methods=['GET','POST'])
def purchase():
    form = ProductForm(request.form)
    
    now = datetime.now()
    time = str(now.time())
    time = time[0:8]
    
    if request.method == "GET":#PETICIÓN GET SOLO PARA OBTENER DATOS
        
        return render_template("purchase.html", form=form)
    
    else:#PETICIÓN POST PARA ENVIAR DATOS SIEMPRE (NO SE VEN LOS DATOS EN EL NAVEGADOR Y ES MÁS SEGURO)
        
            if request.form.get("calc_button") == "Calcular":
                if form.validate():
                    form.to_quantity.data = find_cryptos()#llamo a endpoint para conseguir la conversión entre monedas y cantidad introducida en form de html,
                        #cuando se hace un post se devuelve un formulario con los campos que yo he especificado y uno de ellos es el form.to_quantity.data
                        #donde tengo el valor del precio de la conversión.
                    form.unit_price.data = form.to_quantity.data/float(request.values.get("from_quantity"))#form.unit_price.data es el valor de mi 
                        #campo creado al hacer el formulario y su definición es form.unit_price.data y así para cualquier campo del formulario.
                    
                    return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form
                else:
                    return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form
            
            elif request.form.get("cancel_button") == "Cancelar":
                return redirect(url_for("movements"))#redirigir a template o vista html para mostrar valores grabados en tabla movimientos.
    
            else:#si el botón pulsado es aceptar          
                
                if request.values.get("from_currency") == "EUR" and request.values.get("to_currency") == "BTC":
                    if form.validate():
                        form.to_quantity.data = find_cryptos()#llamo a endpoint para conseguir la conversión entre monedas y cantidad introducida en form de html,
                        #cuando se hace un post se devuelve un formulario con los campos que yo he especificado y uno de ellos es el form.to_quantity.data
                        #donde tengo el valor del precio de la conversión.
                        form.unit_price.data = form.to_quantity.data/float(request.values.get("from_quantity"))#form.unit_price.data es el valor de mi 
                        #campo creado al hacer el formulario y su definición es form.unit_price.data y así para cualquier campo del formulario.
            
                        conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en fichero _config.py)
                        cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
                        query = "INSERT INTO movements (date, time, from_currency,from_quantity,to_currency, to_quantity, unit_price ) VALUES (?, ?, ?, ?, ?, ?, ?);"#petición query para usar dentro de la base de datos
                        datos = (str(now.date()), time, request.values.get("from_currency"), request.values.get("from_quantity"), request.values.get("to_currency"), float(form.to_quantity.data), form.unit_price.data)#recuperar datos del formulario html usando request                    cur.execute(query,datos)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                        cur.execute(query,datos)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                        conn.commit()#EN INSERT HACER SIEMPRE COMMIT O NO GRABA EN BASE DE DATOS
                        conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES
                    else:
                        #manejo de errores
                        return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form
                            
                elif request.values.get("from_currency") == "BTC" and request.values.get("to_currency") != "BTC":#si origen BTC y destino no
                    if request.values.get("from_currency") == "BTC" and request.values.get("to_currency") == "EUR":#comprueba si origen BTC y destino EUR convierte para recuperar inversión
                        if form.validate():
                            form.to_quantity.data = find_cryptos()#llamo a función para conseguir la conversión entre monedas y cantidad introducida en form de html,
                            #cuando se hace un post se devuelve un formulario con los campos que yo he especificado y uno de ellos es el form.to_quantity.data
                            #donde tengo el valor del precio de la conversión.
                            form.unit_price.data = form.to_quantity.data/float(request.values.get("from_quantity"))#form.unit_price.data es el valor de mi 
                            #campo creado al hacer el formulario y su definición es form.unit_price.data y así para cualquier campo del formulario.
                            
                            conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
                            cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
                            query_btc_eur = "INSERT INTO movements (date, time, from_currency,from_quantity,to_currency, to_quantity, unit_price ) VALUES (?, ?, ?, ?, ?, ?, ?);"#petición query para usar dentro de la base de datos
                            datos_btc_eur = (str(now.date()), time, request.values.get("from_currency"), request.values.get("from_quantity"), request.values.get("to_currency"), float(form.to_quantity.data), form.unit_price.data)#recuperar datos del formulario html usando request                    cur.execute(query,datos)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                            cur.execute(query_btc_eur,datos_btc_eur)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                            conn.commit()#EN INSERT HACER SIEMPRE COMMIT O NO GRABA EN BASE DE DATOS
                            conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES
                        
                        else:
                            #manejo de errores
                            return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form
                           
                    else:#si origen es BTC y destino es distinto de EUR entonces es que son las otras criptomonedas
                        if form.validate():

                            form.to_quantity.data = find_cryptos()#llamo a función para conseguir la conversión entre monedas y cantidad introducida en form de html,
                            #cuando se hace un post se devuelve un formulario con los campos que yo he especificado y uno de ellos es el form.to_quantity.data
                            #donde tengo el valor del precio de la conversión.
                            form.unit_price.data = form.to_quantity.data/float(request.values.get("from_quantity"))#form.unit_price.data es el valor de mi 
                            #campo creado al hacer el formulario y su definición es form.unit_price.data y así para cualquier campo del formulario.
                            
                            conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
                            cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
                            query_saldo_from = "SELECT SUM(to_quantity) FROM movements WHERE to_currency = '{}'".format(request.values.get('from_currency'))
                            cantidad_from=cur.execute(query_saldo_from).fetchall()#cantidad_from[0][0] es el valor float que necesito
                            saldo_from = cantidad_from[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida
                            conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES
                            
                            if saldo_from != None:
                                
                                if saldo_from >= float(request.values.get("from_quantity")):
                                    saldo_from -= float(request.values.get("from_quantity"))
                                    
                                    conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
                                    cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
                                    query_new_saldo_from = "INSERT INTO movements (date, time, from_currency,from_quantity,to_currency, to_quantity, unit_price ) VALUES (?, ?, ?, ?, ?, ?, ?);"#petición query para usar dentro de la base de datos
                                    datos_saldo_from = (str(now.date()), time, request.values.get("from_currency"), request.values.get("from_quantity"), request.values.get("to_currency"), float(form.to_quantity.data), form.unit_price.data)#recuperar datos del formulario html usando request                    cur.execute(query,datos)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                                    cur.execute(query_new_saldo_from,datos_saldo_from)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                                    conn.commit()#EN INSERT HACER SIEMPRE COMMIT O NO GRABA EN BASE DE DATOS
                                    conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES
                                
                                    print("Has invertido {} {} y te quedan {} {}".
                                    format(request.values.get("from_quantity"),request.values.get("from_currency"),saldo_from,request.values.get("from_currency")))
                                
                                else:
                                    print("ERROR: Estás inviertiendo {} {} y solo te quedan {} {}".
                                    format(request.values.get("from_quantity"),request.values.get("from_currency"),saldo_from,request.values.get("from_currency")))
                            else:
                                print("ERROR: no has comprado {}".format(request.values.get("from_currency")))

                            """
                            query_saldo_from = "SELECT sum(to_quantity) from movements WHERE from_currency = '{}'".format(request.values.get('from_currency'))
                            cantidad_from=cur.execute(query_saldo_from).fetchall()#cantidad_from[0][0] es el valor float que necesito
                            saldo_from = cantidad_from[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida
                            """
                                        
                            
                            print("Vas a invertir {} {} y consigues {} {}.".format(request.values.get('from_quantity'),request.values.get('from_currency'),form.to_quantity.data,request.values.get('to_currency')))
                        
                        else:
                            #manejo de errores
                            return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form
                           
                elif request.values.get('from_currency') != "BTC" and request.values.get('to_currency') != "BTC":
                    print("Comprando saldo de {} a {}.".format(request.values.get('from_currency'),request.values.get('to_currency')))
                else:
                    print("Comprando saldo de {} a {}.".format(request.values.get('from_currency'),request.values.get('to_currency')))
                """
                conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
                cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
                query = 'INSERT INTO movements (date, time, from_currency,from_quantity,to_currency, to_quantity, unit_price ) VALUES (?, ?, ?, ?, ?, ?, ?);'#petición query para usar dentro de la base de datos
                datos = (str(now.date()), time, request.values.get("from_currency"), request.values.get("from_quantity"), request.values.get("to_currency"), float(form.to_quantity.data), form.unit_price.data)#recuperar datos del formulario html usando request
                
                cur.execute(query,datos)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                conn.commit()#EN INSERT HACER SIEMPRE COMMIT O NO GRABA EN BASE DE DATOS
                conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES
                print("*Insertados en base de datos {},{},{},{},{},{},{}".format(str(now.date()), time, request.values.get("from_currency"), request.values.get("from_quantity"), request.values.get("to_currency"), float(form.to_quantity.data), form.unit_price.data ))
                """
                return redirect(url_for("movements"))#redirigir a template o vista html para mostrar valores grabados en tabla movimientos.

        
@app.route("/status")
def status():
    
    conn = sqlite3.connect(app.config["BASE_DATOS"])#conexión a base de datos(en ficehro _config.py)
    cur = conn.cursor()#crear cursor para conexión

    query = 'SELECT to_currency, to_quantity FROM movements;'#petición query para usar dentro de la base de datos
    
    cur.execute(query)#ejecutar petición query(sqlite) con los datos obtenidos(request)

    conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES    
    return render_template("status.html")

