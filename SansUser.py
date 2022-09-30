from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
from passlib.hash import pbkdf2_sha256
from flask_migrate import Migrate

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/MovieDatabase'
db = SQLAlchemy(app)

class UsersAll(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    user = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(800), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    migrate = Migrate(app, db)

    @staticmethod
    def add_UsersAll(user, password):
        new = UsersAll(user = user, password = password)
        db.session.add(new)
        db.session.commit()

    @staticmethod
    def get_UsersAll():
        return UsersAll.query.all()

    @staticmethod
    def get_UsersAll2(id):
        return UsersAll.query.filter_by(id=id).first()

    @staticmethod
    def delete_UsersAll_by_id(id):
        mv=UsersAll.query.filter_by(id=id).delete()
        db.session.commit()
        return(mv)

    @staticmethod
    def put_UsersAll_by_id(id):
        mv=UsersAll.query.filter_by(id=id).put()
        db.session.commit()
        return(mv)

    @staticmethod
    def update_UsersAll_by_id(id, user, password):
        mv = UsersAll.query.filter_by(id=id).first()
        mv.user = user
        mv.password = password
        db.session.commit()
        return (mv)

class AllUsers(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        UsersAll.add_UsersAll(user = data["user"], password = pbkdf2_sha256.hash(data["password"]))
        return " "

    def get(self):
        data = UsersAll.get_UsersAll()
        print(data)
        li = []
        dic = {}
        for i in data:
            li.append({"user":i.user, "password":i.password})
        return(jsonify(li))

class one_user(Resource):
    def put(self, id):
        data = request.get_json()
        UsersAll.update_UsersAll_by_id(id, data["user"], data["password"])
        if data:
            data.update({"id":data.get('id'), "user": data.get('user'), "password":data.get('password')})
            return jsonify({'message': 'Updated', 'status': HTTPStatus.OK})
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})

    def delete(self, id):
        data = UsersAll.delete_UsersAll_by_id(id)
        if data:
            return jsonify({'message':'Deleted', 'status':HTTPStatus.OK})
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})

    def get(self, id):
        data = UsersAll.get_UsersAll2(id)
        print(data)
        res=[]
        if data != None:
            res.append({"user":data.user, "password":data.password})
            return(jsonify(res))
            return jsonify({'message': 'Data Present', 'status': HTTPStatus.OK})
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})

api.add_resource(AllUsers, "/users")
api.add_resource(one_user, "/users/<int:id>")

app.run()

