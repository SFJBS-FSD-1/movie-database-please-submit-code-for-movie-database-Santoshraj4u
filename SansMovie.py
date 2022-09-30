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
            # dic["title"] = i.title
            # dic["year"] = i.year
            # dic["genre"] = i.genre
            print(dic)
            print(i.title)
            print(i.year)
            print(i.genre)
            li.append({"title":i.title, "year":i.year, "genre":i.genre})

        # print(li)
        # movie_list - jsonify(li)
        return(jsonify(li))

# class one_movie(Resource):
#     def get(self, id):
#         data = Movie.get_movie()
#         res=[]
#         for i in data:
#             if i.id==id:
#                 res.append({"title":i.title, "year":i.year, "genre":i.genre})
#                 return(jsonify(res))
#         else:
#             return "Movie not found"

class one_movie(Resource):
    def get(self, id):
        data = Movie.get_movie2(id)
        print(data)
        res=[]
        if data != None:
            res.append({"title":data.title, "year":data.year, "genre":data.genre})
            return(jsonify(res))
        else:
            return "Movie not found"

api.add_resource(AllMovies, "/movies")
api.add_resource(one_movie, "/movies/<int:id>")
app.run()



# api.add_resource(AllMovies, "/movies")
# app.run()
