
import requests, sqlite3
from configparser import ConfigParser
from cryptoding_app import app

"""
#esconder la APIKEY en fichero config.ini NO FUNCIONA
config = ConfigParser()
config.read('./config.ini')
APIKEY = config["COINMARKET_API"]["APIKEY"]
"""

def listing_cryptos():
        
    conn = sqlite3.connect(app.config["BASE_DATOS"])#conexión a base de datos(en ficehro _config.py)
    cur = conn.cursor()#crear cursor para conexión

    APIKEY = "56bf6ce0-65f1-4f1f-82ef-b4d65deabe25"
    
    URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map?CMC_PRO_API_KEY={}&symbol=BTC,ETH,XRP,LTC,BCH,BNB,USDT,EOS,BSV,XLM,ADA,TRX"

    respuesta = requests.get(URL.format(APIKEY))
        
    mijson = respuesta.json()
    for i in range (0, 11):
    
        crypto_dict = {i:{"id": [], "name": [], "symbol": []}}#crear diccionario
        crypto_id = crypto_dict.get(i)["id"] = mijson["data"][i]["id"]#guardar id cryptomoneda cogido de la API
        crypto_name = crypto_dict.get(i)["name"] = mijson["data"][i]["name"]#guardar name cryptomoneda cogido de la API
        crypto_symbol = crypto_dict.get(i)["symbol"] = mijson["data"][i]["symbol"]#guardar symbol cryptomoneda cogido de la API
        
        query = 'INSERT INTO cryptos (name, symbol) VALUES (?, ?);'#query para insertar en tabla cryptos name y symbol
        datos = crypto_name, crypto_symbol#guardar valores de name y symbol en variable datos

        cur.execute(query,datos)#cursor ejecuta la query para insertar valores de name y symbol en base de datos
        conn.commit()#comentar para grabar los datos en la base

    conn.close()#cerrar conexión con la base de datos
    return crypto_dict


result = listing_cryptos()
