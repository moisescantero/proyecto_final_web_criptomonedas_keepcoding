#aquí se crea o inicializa la aplicación flask
from flask import Flask

app = Flask(__name__, instance_relative_config=True)#creamos app y configuramos instancia relativa al fichero config.py
app.config.from_object("_config")#ruta al fichero config.py donde guardamos nuestra SECRET_KEY para evitar phising a nuestra web


from cryptoding_app import routes#importamos las rutas (routes.py) de nuestra aplicación flask



