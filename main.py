#from flask import Flask;
#print("hi")

from flask import Flask,request,jsonify

app = Flask(__name__)

user_list=[{"name":"Ajay","age":20},{"name":"Vijay","age":30}]
#user_list.update()

@app.route("/",methods=["GET"])
def home_get():
    if request.method == "GET":
        json_data=jsonify(user_list)

        return json_data

@app.route("/",methods=["POST"])
def home_post():
    if request.method == "POST":
        data = request.get_json()
        user_list.append(data)
        return user_list

@app.route("/",methods=["POST"])
def home_post():
    if request.method == "POST":
        data = request.get_json()
        user_list.append(data)
        returen user_list

app.run()