from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from settings import make_hash_from_password, make_salt, make_pepper



app = Flask(__name__)

app.jinja_env.globals["make_hash_from_password"] = make_hash_from_password

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

LOGIN_NAME_FLAG = 0
LOGIN_PASS_FLAG = 0

class User_db(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(), unique = True, nullable = False)
    password = db.Column(db.String(), nullable = False)
    salt = db.Column(db.String(), nullable = False)

    def __init__(self, name, password, salt):
        self.name = name
        self.password = password
        self.salt = salt

class Peppers_db(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    pepper = db.Column(db.String(), nullable = False)

    def __init__(self, pepper):
        self.pepper = pepper

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    global LOGIN_NAME_FLAG, LOGIN_PASS_FLAG
    if request.method == "POST":
        onetime_salt = make_salt(8)
        name = request.form.get("name")
        db_user = db.session.query(User_db).filter(User_db.name == name).all()
        user = db_user
        while LOGIN_NAME_FLAG == 0:
            if db_user == []:
                error_message = "Please enter valid name."
                return render_template("login.html", LOGIN_NAME_FLAG = LOGIN_NAME_FLAG, error_message = error_message)
            else:
                LOGIN_NAME_FLAG = 1
                break
        password = request.form.get("password")
        print(password)
        return render_template("login.html", LOGIN_NAME_FLAG = LOGIN_NAME_FLAG, onetime_salt = onetime_salt)
        
    return render_template("login.html", LOGIN_NAME_FLAG = LOGIN_NAME_FLAG)

@app.route("/create_account", methods = ["GET", "POST"])
def create_account():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        salt = make_salt(8)
        pepper = make_pepper(8)
        password = make_hash_from_password(password, salt, 1)
        password = make_hash_from_password(password, pepper, 1)

        user = User_db(
            name = name,
            password = password,
            salt = salt
        )
        db.session.add(user)
        db.session.commit()

        pepper = Peppers_db(
            pepper = pepper
        )

        db.session.add(pepper)
        db.session.commit()

        return render_template("/index.html")
    return render_template("create_account.html")