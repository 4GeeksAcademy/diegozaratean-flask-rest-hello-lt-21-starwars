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

from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

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

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "cualquier ocsa que se te ocurra"  # Change this! 1234abc.   ksdjfklasjfkasjfljaskfjasdkljflafdsfds.  123abd. jhaskdfhkajdshfkjashfkjashfkjashdk
jwt = JWTManager(app)

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
##.  rafael@gmial,. 123. asdkfjkalksfjlkasdjflkasdj === asdkfjkalksfjlkasdjflkasdj
###  david#gmail. 456.    iewuruqwruqwuruqweruqweu
# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    # busque el usuario con email email 
    user = User.query.filter_by(email=email).first()
    
    if user is None:
        return jsonify({"msg": "The user isn't in the system"}), 401

    print(user)
    print(user.serialize())
    print(user.email)
    print(user.password)
    
    if password != user.password :
        return jsonify({"msg": "Bad password"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    # Access the identity of the current user with get_jwt_identity
    user_email = get_jwt_identity()
    # return jsonify(logged_in_as=user_email), 200
    user = User.query.filter_by(email=user_email).first()
    print(user)
    response_body = {
        "msg": "Usuario encontrado",
        "user": user.serialize()
    }

    return jsonify(response_body), 200


# FINAL DE CODIGO

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
