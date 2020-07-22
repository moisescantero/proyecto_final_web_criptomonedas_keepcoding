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
    
    hayregistros = ('SELECT * FROM movements;')#petición query para usar dentro de la base de datos y saber si hay registros en la tabla
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
            
                form.to_quantity.data = find_cryptos()#llamo a endpoint para conseguir la conversión entre monedas y cantidad introducida en form de html,
                    #cuando se hace un post se devuelve un formulario con los campos que yo he especificado y uno de ellos es el form.to_quantity.data
                    #donde tengo el valor del precio de la conversión.
                form.unit_price.data = form.to_quantity.data/float(request.values.get("from_quantity"))#form.unit_price.data es el valor de mi 
                    #campo creado al hacer el formulario y su definición es form.unit_price.data y así para cualquier campo del formulario.
                
                return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form
             
        elif request.form.get("cancel_button") == "Cancelar":
            return redirect(url_for("movements"))#redirigir a template o vista html para mostrar valores grabados en tabla movimientos.

        else:#si el botón pulsado es aceptar          
            
            if request.values.get("from_currency") == "EUR" and request.values.get("to_currency") == "BTC":#SI ORIGEN EUR Y DESTINO BTC
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
            
                return redirect(url_for("movements"))#redirigir a template o vista html para mostrar valores grabados en tabla movimientos.
                    
            elif request.values.get("from_currency") == "BTC" and request.values.get("to_currency") != "BTC":#SI ORIGEN BTC Y DESTINO DISTINTO BTC
                if request.values.get("from_currency") == "BTC" and request.values.get("to_currency") == "EUR":#SI ORIGEN BTC Y DESTINO EUR PARA RECUPERAR INVERSIÓN
                    
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
                    
                        return redirect(url_for("movements"))#redirigir a template o vista html para mostrar valores grabados en tabla movimientos.
                    
                    else:
                        return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form
                
                else:#SI ORIGEN ES BTC Y DESTINO ES OTRA CRIPTOMONEDA
                    if form.validate():
                        form.to_quantity.data = find_cryptos()#llamo a función para conseguir la conversión entre monedas y cantidad introducida en form de html,
                        #cuando se hace un post se devuelve un formulario con los campos que yo he especificado y uno de ellos es el form.to_quantity.data
                        #donde tengo el valor del precio de la conversión.
                        form.unit_price.data = form.to_quantity.data/float(request.values.get("from_quantity"))#form.unit_price.data es el valor de mi 
                        #campo creado al hacer el formulario y su definición es form.unit_price.data y así para cualquier campo del formulario.
                        
                        conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
                        cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
                        query_new_saldo_from = "INSERT INTO movements (date, time, from_currency,from_quantity,to_currency, to_quantity, unit_price ) VALUES (?, ?, ?, ?, ?, ?, ?);"#petición query para usar dentro de la base de datos
                        datos_saldo_from = (str(now.date()), time, request.values.get("from_currency"), request.values.get("from_quantity"), request.values.get("to_currency"), float(form.to_quantity.data), form.unit_price.data)#recuperar datos del formulario html usando request                    cur.execute(query,datos)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                        cur.execute(query_new_saldo_from,datos_saldo_from)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                        conn.commit()#EN INSERT HACER SIEMPRE COMMIT O NO GRABA EN BASE DE DATOS
                        conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES

                        return redirect(url_for("movements"))#redirigir a template o vista html para mostrar valores grabados en tabla movimientos.

                    else:
                        return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form

            elif request.values.get('from_currency') != "BTC" and request.values.get('to_currency') != "BTC":#SI ORIGEN ES CRIPTO Y DESTINO TAMBIÉN OTRA CRIPTOMONEDA
                if form.validate():
                    form.to_quantity.data = find_cryptos()#llamo a función para conseguir la conversión entre monedas y cantidad introducida en form de html,
                    #cuando se hace un post se devuelve un formulario con los campos que yo he especificado y uno de ellos es el form.to_quantity.data
                    #donde tengo el valor del precio de la conversión.
                    form.unit_price.data = form.to_quantity.data/float(request.values.get("from_quantity"))#form.unit_price.data es el valor de mi 
                    #campo creado al hacer el formulario y su definición es form.unit_price.data y así para cualquier campo del formulario.
                    
                    conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
                    cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
                    query_new_saldo_from = "INSERT INTO movements (date, time, from_currency,from_quantity,to_currency, to_quantity, unit_price ) VALUES (?, ?, ?, ?, ?, ?, ?);"#petición query para usar dentro de la base de datos
                    datos_saldo_from = (str(now.date()), time, request.values.get("from_currency"), request.values.get("from_quantity"), request.values.get("to_currency"), float(form.to_quantity.data), form.unit_price.data)#recuperar datos del formulario html usando request                    cur.execute(query,datos)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                    cur.execute(query_new_saldo_from,datos_saldo_from)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                    conn.commit()#EN INSERT HACER SIEMPRE COMMIT O NO GRABA EN BASE DE DATOS
                    conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES

                    return redirect(url_for("movements"))#redirigir a template o vista html para mostrar valores grabados en tabla movimientos.
                else:
                    return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form

            else:#SI ORIGEN == OTRACRIPTO Y DESTINO == BTC
                if form.validate():
                    form.to_quantity.data = find_cryptos()#llamo a función para conseguir la conversión entre monedas y cantidad introducida en form de html,
                    #cuando se hace un post se devuelve un formulario con los campos que yo he especificado y uno de ellos es el form.to_quantity.data
                    #donde tengo el valor del precio de la conversión.
                    form.unit_price.data = form.to_quantity.data/float(request.values.get("from_quantity"))#form.unit_price.data es el valor de mi 
                    #campo creado al hacer el formulario y su definición es form.unit_price.data y así para cualquier campo del formulario.
                    
                    conn = sqlite3.connect(app.config["BASE_DATOS"])#ABRIR CONEXIÓN A BASE DE DATOS(en ficehro _config.py)
                    cur = conn.cursor()#CREAR CURSOR PARA USAR DURANTE LA CONEXIÓN
                    query_new_saldo_from = "INSERT INTO movements (date, time, from_currency,from_quantity,to_currency, to_quantity, unit_price ) VALUES (?, ?, ?, ?, ?, ?, ?);"#petición query para usar dentro de la base de datos
                    datos_saldo_from = (str(now.date()), time, request.values.get("from_currency"), request.values.get("from_quantity"), request.values.get("to_currency"), float(form.to_quantity.data), form.unit_price.data)#recuperar datos del formulario html usando request                    cur.execute(query,datos)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                    cur.execute(query_new_saldo_from,datos_saldo_from)#ejecutar petición query(sqlite) con los datos obtenidos(request)
                    conn.commit()#EN INSERT HACER SIEMPRE COMMIT O NO GRABA EN BASE DE DATOS
                    conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES

                    return redirect(url_for("movements"))#redirigir a template o vista html para mostrar valores grabados en tabla movimientos.
                else:
                    return render_template("purchase.html", form=form)#retornar a template o vista html con los valores del diccionario que hay en form
            
@app.route("/status")
def status():
    
    conn = sqlite3.connect(app.config["BASE_DATOS"])#conexión a base de datos(en ficehro _config.py)
    cur = conn.cursor()#crear cursor para conexión
    hayregistros = ('SELECT * FROM movements')#petición query para usar dentro de la base de datos y saber si hay registros en la tabla
    registros = cur.execute(hayregistros).fetchall()#cursor ejecuta la query para comprobar si existen registros en la tabla movimientos
    conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES 
    
    if len(registros) == 0:#si no hay registros
        return render_template("without_moves.html")
    else:#si existen registros
        #CALCULAR SALDO EUROS INVERTIDOS
        conn = sqlite3.connect(app.config["BASE_DATOS"])#conexión a base de datos(en ficehro _config.py)
        cur = conn.cursor()#crear cursor para conexión
        
        query_saldo_disponible_EUR = 'SELECT SUM(to_quantity) FROM movements WHERE to_currency = "EUR";'
        cantidad_disponible_EUR=cur.execute(query_saldo_disponible_EUR).fetchall()#cantidad_from[0][0] es el valor float que necesito
        saldo_disponible_EUR = cantidad_disponible_EUR[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida
        
        query_saldo_gastado_EUR = 'SELECT SUM(from_quantity) FROM movements WHERE from_currency = "EUR";'
        cantidad_gastado_EUR=cur.execute(query_saldo_gastado_EUR).fetchall()#cantidad_from[0][0] es el valor float que necesito
        saldo_gastado_EUR = cantidad_gastado_EUR[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida
        
        diferencia_euro = []
        total_saldo_inversión_EUR = round((saldo_disponible_EUR - saldo_gastado_EUR),8)
        diferencia_euro.append(total_saldo_inversión_EUR)

        conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES    

        
        #CALCULAR TOTAL EUROS INVERTIDOS
        conn = sqlite3.connect(app.config["BASE_DATOS"])#conexión a base de datos(en ficehro _config.py)
        cur = conn.cursor()#crear cursor para conexión

        query_saldo_disponible_EUR = 'SELECT SUM(to_quantity) FROM movements WHERE to_currency = "EUR";'
        cantidad_disponible_EUR=cur.execute(query_saldo_disponible_EUR).fetchall()#cantidad_from[0][0] es el valor float que necesito
        total_saldo_disponible_EUR = cantidad_disponible_EUR[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida
        conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES    

    
        #CALCULAR VALOR ACTUAL DE CADA CRIPTOMONEDA EN EUROS
        dict_criptos = {"ADA": 0.0, "BCH": 0.0, "BNB": 0.0, "BSV": 0.0, "BTC": 0.0, "EOS": 0.0, "ETH": 0.0, 
                        "LTC": 0.0, "TRX": 0.0, "USDT": 0.0, "XLM": 0.0}

        conn = sqlite3.connect(app.config["BASE_DATOS"])#conexión a base de datos(en ficehro _config.py)
        cur = conn.cursor()#crear cursor para conexión

        for cripto in dict_criptos:
            
            query_saldo_disponible_cripto = ('SELECT SUM(to_quantity) FROM movements WHERE to_currency = "{}";'.format(cripto))
            cantidad_disponible_cripto=cur.execute(query_saldo_disponible_cripto).fetchall()#cantidad_from[0][0] es el valor float que necesito
            saldo_disponible_cripto = cantidad_disponible_cripto[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida
        
            query_saldo_gastado_cripto = ('SELECT SUM(from_quantity) FROM movements WHERE from_currency = "{}";'.format(cripto))
            cantidad_gastado_cripto=cur.execute(query_saldo_gastado_cripto).fetchall()#cantidad_from[0][0] es el valor float que necesito
            saldo_gastado_cripto = cantidad_gastado_cripto[0][0]#saldo_from es un float para comprobar si hay saldo suficiente de criptomoneda introducida

            if saldo_disponible_cripto != None and saldo_gastado_cripto != None:#si se ha invertido y gastado

                total_saldo_inversión_cripto = round((saldo_disponible_cripto - saldo_gastado_cripto),8)

                if total_saldo_inversión_cripto > 0.00:
                    #CONSULTA A API CON SALDO SOBRANTE PARA CONVERTIR A EUROS
                    APIKEY = "56bf6ce0-65f1-4f1f-82ef-b4d65deabe25"
                    URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
                    respuesta = requests.get(URL.format(total_saldo_inversión_cripto, cripto, "EUR", APIKEY))
                    mijson = respuesta.json()
                    price_currency = mijson.get("data").get("quote").get("EUR")["price"]

                    #guardar precio en euros para la criptomoneda concreta
                    dict_criptos[cripto] = round(price_currency,8)
                
                else:
                    pass

            elif saldo_disponible_cripto != None and saldo_gastado_cripto == None:#si se ha invertido pero no se ha gastado
                if saldo_disponible_cripto > 0.00:
                    APIKEY = "56bf6ce0-65f1-4f1f-82ef-b4d65deabe25"
                    URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"
                    respuesta = requests.get(URL.format(saldo_disponible_cripto, cripto, "EUR", APIKEY))
                    mijson = respuesta.json()
                    price_currency = mijson.get("data").get("quote").get("EUR")["price"]
                    dict_criptos[cripto] = round(price_currency,8)
                else:
                    pass
            else:
                pass
        #SUMANDO CANTIDAD DE EUROS PARA CADA CRIPTOMONEDA CONCRETA
        total_criptos_a_euro = []
        suma_criptos_a_euros = 0.0
        for cripto in dict_criptos:
            suma_criptos_a_euros += dict_criptos[cripto]
        total_criptos_a_euro.append(suma_criptos_a_euros)    
        
        #CALCULANDO EL VALOR ACTUAL
        valor_actual = []
        valor_actual.append(total_saldo_inversión_EUR + total_saldo_disponible_EUR + suma_criptos_a_euros)

        conn.close()#SIEMPRE CERRAR LA CONEXIÓN A BASE DE DATOS PARA EVITAR POSIBLES INTRUSIONES    
        print(dict_criptos)
        print(valor_actual)
        #renderizar lo que hay en las lista pasándolo al template status y que se muestre según especifiacamos usando jinja
        return render_template("status.html",diferencia_euro=diferencia_euro,
                            cantidad_disponible_EUR=cantidad_disponible_EUR,
                            dict_criptos=dict_criptos, total_criptos_a_euro=total_criptos_a_euro,
                            valor_actual=valor_actual)
    

