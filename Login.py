from flask import Flask, request, jsonify, render_template
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from http import HTTPStatus
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost/MovieDatabase'
db = SQLAlchemy(app)

class UsersAll(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # this is the primary key
    user = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(800), nullable=False)

@app.route("/")
def home_page():
    print("rendring home page")
    return render_template("home.html")

@app.route("/login",methods=['GET','POST'])
def login_page():
    return render_template("login.html")

@app.route("/register",methods=['GET','POST'])
def register_page():
    if request.method == "POST":
        user = request.form["user"]
    else:
        return render_template("register.html")

# api.add_resource(AllUsers, "/users")
# api.add_resource(one_user, "/users/<int:id>")
#
app.run()