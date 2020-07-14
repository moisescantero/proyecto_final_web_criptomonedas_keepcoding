#using API key to make a conversion

import requests
from configparser import *
from flask import Flask, render_template, request, redirect, url_for
 

"""#esconder la APIKEY en fichero config.ini NO FUNCIONA
config = ConfigParser()
config.read("config.ini")
APIKEY = config["APIKEY"]
"""


def find_cryptos():
    APIKEY = "56bf6ce0-65f1-4f1f-82ef-b4d65deabe25"

    URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"

    respuesta = requests.get(URL.format( request.values.get("from_quantity"), request.values.get("from_currency"), request.values.get("to_currency"), APIKEY))
    
    mijson = respuesta.json()
    to_currency = request.values.get("to_currency")
    
    return mijson.get("data").get("quote").get(to_currency)["price"]
    
