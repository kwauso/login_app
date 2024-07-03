from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class User_db(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)

    def __init__(self, name, password):
        self.name = name
        self.password = password

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/create_account", methods = ["GET", "POST"])
def create_account():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        password = hashlib.sha256(password.encode())
        password = password.hexdigest()

        user = User_db(
            name = name,
            password = password
        )
        db.session.add(user)
        db.session.commit()

        return render_template("/index.html")
    return render_template("create_account.html")