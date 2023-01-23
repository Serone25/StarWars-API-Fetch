"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet
#from models import Person
import json

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

people=[
    {
    "id": "0",
    "name": "Luke Skywalker",
	"height": "172",
	"mass": "77",
	"hair_color": "blond",
	"skin_color": "fair",
	"eye_color": "blue"
    },
    {
    "id":"1",
    "name": "C-3PO",
	"height": "167",
	"mass": "75",
	"hair_color": "n/a",
	"skin_color": "gold",
	"eye_color": "yellow"
    }
]

planets = [
    {
    "id":"0",
    "name": "Tatooine",
	"rotation_period": "23",
	"orbital_period": "304",
	"diameter": "10465",
	"climate": "arid",
	"gravity": "1 standard",
	"terrain": "desert"
    },
    {
    "id":"1",
    "name": "Alderaan",
	"rotation_period": "24",
	"orbital_period": "364",
	"diameter": "12500",
	"climate": "temperate",
	"gravity": "1 standard",
	"terrain": "grasslands, mountains"
    }
]


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/people',methods=['GET'])
def handle_characters():
    
    return jsonify(people), 200

@app.route('/people/<int:people_id>',methods=['GET'])
def handle_character(people_id):
    person = people[people_id]
    person = filter(lambda element: element["id"] == people_id, people)
    return jsonify(person), 200

#Cojo los datos del array planets
@app.route('/planets',methods=['GET'])
def handle_planets():
    
    return jsonify(planets), 200

#Cojo los datos de la base de datos en models.py
@app.route('/planet/<id>',methods=['GET'])
def handle_planet():
    #planet = Planet.query.get(id)
    #print(planet.serialize())       #Llamo al metodo serialize para ver el objeto

    planet = Planet.query.filter_by(id=id).one()
    planet = planet.serialize()
    return jsonify(planet), 200

#Cojo todos los datos de la base de datos
@app.route('/allplanets',methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()            #Creo un array y le meto todos los objetos
    result = []                             #Array vacío
    for planet in planets:                  #Por cada elemento en el array planets
        result.append(planets.serialize())  #meteme en el array vacio el objeto serializado

    #mismo resultado escrito de otras dos maneras:
    #result = [planet.serialize() for planet in planets]
    #result = list(map(lambda planet : planet.serialize(),planets))

    return jsonify(result), 200

@app.route('/planet',methods=['POST'])
def create_planet():
    data = request.data
    #print(data)
    data = json.loads(data)
    planet = Planet(name = data["name"], description = data["description"])
    db.session.add(planet)
    db.session.commit()
    return jsonify(planet), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
