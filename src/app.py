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
from models import db, User, Estudio
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# INCION DE CODIGO
# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
# deberia traerme todos los usuarios
    print('holaaaaaaaaaaaa')
    all_users = User.query.all()
    print(all_users)
    result = list(map(lambda user: user.serialize(),all_users))
    print(result)
    
    response_body = {
        "msg": "deberia traerme todos los usuarios "
    }

    return jsonify(result), 200


@app.route('/estudio', methods=['GET'])
def get_estudios():
    all_estudios = Estudio.query.all()
    result = list(map(lambda item: item.serialize(),all_estudios))

    return jsonify(result), 200

@app.route('/estudio/<int:estudio_id>', methods=['GET'])
def get_estudio(estudio_id):
    estudio = Estudio.query.filter_by(id=estudio_id).first()

    return jsonify(estudio.serialize()), 200    


@app.route('/estudio', methods=['POST'])
def crear_estudio():
    print(request.get_json())
    print(request.get_json()['nombre'])


    body = request.get_json()    
    estudio = Estudio(nombre=body['nombre'],logo=body['logo'],slogan=body['slogan'] )
    db.session.add(estudio)
    db.session.commit()
    response_body = {
        "msg": "crear un estudio "
    }

    return jsonify(response_body), 200

# FINAL DE CODIGO

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
