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
from models import db, User, Character, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


# .....................take all user, character or planet..................
@app.route('/users', methods=['GET'])
def get_all_user():
    users = User.query.all()
    user_list =  list(map(lambda user: user.serialize(), users))
    return ({"results":user_list}), 200

@app.route('/characters', methods=['GET'])
def get_all_characters():
    characters = Character.query.all()
    character_list =  list(map(lambda character: character.serialize(), characters))
    return ({"results":character_list}), 200

@app.route('/planets', methods=['GET'])
def get_all_planets():
    planets = Planet.query.all()
    planet_list =  list(map(lambda planet: planet.serialize(), planets))
    return ({"results":planet_list}), 200

@app.route('/user/<int:id>', methods=['GET'])
def get_one_user(id):
    user = User.query.get(id)
    return {"results":user.serialize()}, 200

@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    user = Planet.query.get(id)
    return {"results":planet.serialize()}, 200

@app.route('/character/<int:id>', methods=['GET'])
def get_one_character(id):
    character = Character.query.get(id)
    return {"results":character.serialize()}, 200

# .....................................Delete one user, characters or planet.............................

@app.route('/character/<int:id>', methods=['DELETE'])
def delete_one_character(id):

    character = Character.query.get(id)
    db.session.delete(character)
    db.session.commit()
    return {"delete":character.serialize()}, 200

@app.route('/planet/<int:id>', methods=['DELETE'])
def delete_one_planet(id):

    planet = Planet.query.get(id)
    db.session.delete(planet)
    db.session.commit()
    return {"delete":planet.serialize()}, 200

@app.route('/user/<int:id>', methods=['DELETE'])
def delete_one_user(id):

    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return {"delete":user.serialize()}, 200

# ...............................Create one character, user or planets....................

@app.route('/user', methods=['POST'])
def create_one_user():

    user = request.get_json()
    new_user = User(email=user["email"], password=user["password"], is_active=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"created":new_user.serialize()}), 200

@app.route('/planet', methods=['POST'])
def create_one_planet():

    planet = request.get_json()
    new_planet = Planet(name=planet["name"], diameter=planet["diameter"], mass=planet["mass"],  orbit=planet["orbit"])
    db.session.add(new_planet)
    db.session.commit()
    return jsonify({"created":new_planet.serialize()}), 200

@app.route('/character', methods=['POST'])
def create_one_character():

    character = request.get_json()
    new_character = Character(name=character["name"], heigth=character["heigth"], weigth=character["weigth"],  eyes_color=character["eyes_color"])
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"created":new_character.serialize()}), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
