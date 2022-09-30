from flask import Flask
import os
app=Flask(__name__)



@app.route("/")
def Home_page():
    return("<h1>Welcome to home page</h1>")

port = int(os.environ.get("PORT",5000))

if __name__ == "__main__":
    app.run(port=port)