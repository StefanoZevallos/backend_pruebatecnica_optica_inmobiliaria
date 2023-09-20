from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from utilitarios import conexion
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv
from models import *
from urllib.parse import quote_plus
from controllers import (RegistrosController , 
                         LoginController,UsuarioController)



from flask_jwt_extended import JWTManager
# convierte un string en formato json a un diccionario
from json import load
from datetime import timedelta

# sirve para cargar mis variables declaradas en el archivo .env como si fueran variables de entorno
load_dotenv()


app = Flask(__name__)

if environ.get("PYTHON_VERSION"):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get("DATABASE_URL")
else:    
    passwordBd = environ.get("DATABASE_URL").split(":")[2].split("@localhost")[0]
    passwordConvertida = quote_plus(passwordBd)
    urlBd = environ.get("DATABASE_URL").replace(passwordBd, passwordConvertida)
    #print(passwordBd)
    app.config['SQLALCHEMY_DATABASE_URI'] = urlBd

# servira para firmar las tokens
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1, minutes=15)


JWTManager(app)

# CORS > Cross Origin Resource Sharing (sirve para indicar quien puede tener acceso a mi API, indicando el dominio (origins), las cabeceras (allow_headers), y los metodos (methods))
CORS(app, origins='*')
api = Api(app)

conexion.init_app(app)

Migrate(app, conexion)

# rutas

api.add_resource(RegistrosController, '/registro')
api.add_resource(LoginController, '/login')
api.add_resource(UsuarioController,'/perfil')




if __name__ == '__main__':
    app.run(debug=True)