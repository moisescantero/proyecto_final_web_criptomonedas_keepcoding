#using API key to make a conversion

import requests
from configparser import *
from flask import Flask, render_template, request, redirect, url_for
 


config = ConfigParser()
config.read('./config.ini')
APIKEY = config['COINMARKET_API']['APIKEY']



def find_cryptos():

    URL = "https://pro-api.coinmarketcap.com/v1/tools/price-conversion?amount={}&symbol={}&convert={}&CMC_PRO_API_KEY={}"

    respuesta = requests.get(URL.format( request.values.get("from_quantity"), request.values.get("from_currency"), request.values.get("to_currency"), APIKEY))
    
    mijson = respuesta.json()
    to_currency = request.values.get("to_currency")
    
    return mijson.get("data").get("quote").get(to_currency)["price"]
    
