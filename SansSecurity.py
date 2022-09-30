from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
from passlib.hash import pbkdf2_sha256
from flask_migrate import Migrate
import jwt
import os
import uuid
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, JWTManager, jwt_required, get_jwt_identity, get_jwt



app = Flask(__name__)
api = Api(app)
jwt = JWTManager()
jwt.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/MovieDatabase'
app.config['SECRET_KEY'] = 'Your Secret Key'
db = SQLAlchemy(app)
migrate = Migrate(app,db)

block_list = set()

@jwt.token_in_blocklist_loader
def check_if_token_in_block_list(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in block_list

class SecUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    public_id = db.Column(db.String(80), unique=True)
    user = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(800), nullable=False)

    @staticmethod
    def add_SecUser(user, password):
        data = SecUser.query.filter_by(user=user).first()
        if data == None:
            hashed = pbkdf2_sha256.hash(password)
            public_id = str(uuid.uuid4())
            new = SecUser(user = user, password = hashed, public_id = public_id)
            db.session.add(new)
            db.session.commit()
            return jsonify({"Message":"User Created"})
        else:
            return jsonify({"Message": "User Already exitst"})

    @staticmethod
    def checkPassword(user, password):
        data = SecUser.query.all()
        for p in data:
            if user == p.user:
                if pbkdf2_sha256.verify(password, p.password):
                    token = jwt.encode({"public_id":p.public_id,
                                        "exp":datetime.utcnow()+timedelta(seconds=30)},app.config["SECRET_KEY"])
                    #print(token)
                    return jsonify({"Message":"Correct password","Token":token})
                else:
                    return jsonify({"Message": "InCorrect user or password"})
        else:
            return jsonify({"Message": "User doesn't exitst"})

class signup(Resource):
    def post(self):
        data = request.get_json()
        data = SecUser.add_SecUser(user=data["user"], password=data["password"])
        return data

class login(Resource):
    def post(self):
        data = request.get_json()
        data = SecUser.checkPassword(user=data["user"], password=data["password"])
        return data

def token_required(f):
    def decorated(*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers:
            token=request.headers["x-access-token"]
        if not token:
            return jsonify({"Message":"Token is missing"})
        else:
            try:
                data = jwt.decode(token,app.config['SECRET_KEY'],algorithms=['HS256'])
                current_user = SecUser.query.filter_by(public_id=data["public_id"]).first()
                if current_user:
                    return f()
                else:
                    return jsonify({"Message":"Token is invalid"})
            except:
                return jsonify({"Message": "Token is missing"})
    return decorated

@app.route("/users", methods=["GET","POST"])
#@token_required
def show_users():
    data = SecUser.query.all()
    names_dict = {}
    for name in data:
        names_dict[name.id] = name.user
    return jsonify(names_dict)

@app.route("/token", methods=["GET","POST"])
def createtoken():
    data = request.get_json()
    user = data["user"]
    password = data["password"]
    check_user = SecUser.query.filter_by(user=data["user"]).first()
    if check_user:
        #token = create_access_token(identity=user)
        #return jsonify({"token":token})
        access_token = create_access_token(identity=user,fresh=True)
        refresh_token = create_refresh_token(identity=user)
        return jsonify({"access_token": access_token, "refresh_token":refresh_token})

@app.route("/test", methods=["POST","GET"])
#@jwt_required()
@jwt_required(optional=True)
def mytest():
    current_user = get_jwt_identity()
    #print(current_user)
    if current_user:
        return jsonify({"Message":"Thanks for wearing the Bladge"})
    else:
        return jsonify({"Message": "Warning!!"})

@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user, fresh=False)
    return jsonify({"new_access_token": new_access_token})

@app.route("/revoke", methods=["POST"])
@jwt_required()
def revoke_token():
    jti = get_jwt()["jti"]
    block_list.add(jti)
    return jsonify({"Message": "Logged out successfully"})

api.add_resource(signup, "/signup")
api.add_resource(login, "/login")

if __name__ == "__main__":
    app.run(port=5001)
    #app.run()
