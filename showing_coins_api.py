from cryptoding_app import app#importar mi app web flask
import sqlite3#importar para usar la base de datos
from listing_using_api import listing_cryptos

def showing_coins():

    conn = sqlite3.connect(app.config["BASE_DATOS"])#conexión a base de datos(en ficehro _config.py)
    cur = conn.cursor()#crear cursor para conexión

    query = 'SELECT symbol FROM cryptos;'#petición query para usar dentro de la base de datos
    coins = cur.execute(query).fetchall()#cursor ejecuta la query para guardar en variable movements

    new_list = ["EUR"]
    for word in coins:
        for j in word:
            new_list.append(j)
    
    conn.close()
    return new_list
    

#result = showing_coins()