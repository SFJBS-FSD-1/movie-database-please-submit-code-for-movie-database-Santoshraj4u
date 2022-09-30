from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/MovieDatabase'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(80), nullable=False)

    @staticmethod
    def add_movie(title, year, genre):
        new = Movie(title = title, year = year, genre = genre)
        db.session.add(new)
        db.session.commit()

    @staticmethod
    def get_movie():
        return Movie.query.all()

    @staticmethod
    def get_movie2(id):
        return Movie.query.filter_by(id=id).first()

    @staticmethod
    def delete_movie_by_id(id):
        mv=Movie.query.filter_by(id=id).delete()
        db.session.commit()
        return(mv)

    @staticmethod
    def put_movie_by_id(id):
        mv=Movie.query.filter_by(id=id).put()
        db.session.commit()
        return(mv)

    @staticmethod
    def update_movie_by_id(id, title, year, genre):
        mv = Movie.query.filter_by(id=id).first()
        mv.title = title
        mv.year = year
        mv.genre = genre
        db.session.commit()
        #return (mv)

class AllMovies(Resource):
    def post(self):
        data = request.get_json()
        print(data)
        Movie.add_movie(title = data["title"], year = data["year"], genre = data["genre"])
        return " "

    def get(self):
        data = Movie.get_movie()
        print(data)
        li = []
        dic = {}
        for i in data:
            # print(dic)
            # print(i.title)
            # print(i.year)
            # print(i.genre)
            li.append({"title":i.title, "year":i.year, "genre":i.genre})
        return(jsonify(li))

class one_movie(Resource):
    def put(self, id):
        data = request.get_json()
        Movie.update_movie_by_id(id, data["title"], data["year"], data["genre"])
        if data:
            data.update({"id":data.get('id'), "title": data.get('title'), "year":data.get('year'), "genre":data.get('genre')})
            return jsonify({'message': 'Updated', 'status': HTTPStatus.OK})
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})

    def delete(self, id):
        data = Movie.delete_movie_by_id(id)
        if data:
            return jsonify({'message':'Deleted', 'status':HTTPStatus.OK})
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})

    def get(self, id):
        data = Movie.get_movie2(id)
        print(data)
        res=[]
        if data != None:
            res.append({"title":data.title, "year":data.year, "genre":data.genre})
            return(jsonify(res))
            return jsonify({'message': 'Data Present', 'status': HTTPStatus.OK})
        else:
            return jsonify({'message':'Not found', 'status':HTTPStatus.NOT_FOUND})

api.add_resource(AllMovies, "/movies")
api.add_resource(one_movie, "/movies/<int:id>")

app.run()

