from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import md5 # imports the md5 module to generate a hash
from myemail import Email
from name import Name
from password import Password
# from sqlalchemy import exc
app = Flask(__name__)
app.secret_key = 'KeepItSecretKeepItSafe'
mysql = MySQLConnector(app,'fakebook_db')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=["POST"])
def register_user():
    try:
        f_name = request.form["f_name"]
        l_name = request.form["l_name"]
        email = request.form["email"]
        Name(f_name, l_name)
        Email(email)
        pwd = request.form["pwd"]
        confi_pwd = request.form["confi_pwd"]
        Password(pwd,confi_pwd)
        pwd = md5.new(pwd).hexdigest();
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VAlUES(:first_name, :last_name, :email, :password, NOW(), NOW())"
        data = {
            "first_name": f_name,
            "last_name": l_name,
            "email": email,
            "password": pwd
        }
        mysql.query_db(query, data)
        return redirect("/home")
    except Exception as e:
        flash(str(e))
    return redirect("/")

@app.route('/login', methods=["POST"])
def login_user():
    email = request.form["email"]
    password = request.form["pwd"]
    print email, password
    user_query = "SELECT * FROM users WHERE users.email = :email LIMIT 1"
    query_data = {'email': email}
    user = mysql.query_db(user_query, query_data)
    if len(user) != 0:
        encrypted_password = md5.new(password).hexdigest();
        if user[0]["password"] == encrypted_password:
        # this means we have a successful login!
            return redirect("/home")
        else:
            flash("******INVALID PASSWORD******")
            return redirect("/")
    else:
        flash("******INVALID EMAIL******")
        return redirect("/")


@app.route('/home')
def home_page():
    return render_template("home.html")
app.run(debug=True)
