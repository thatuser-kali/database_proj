import os
from flask import Flask, render_template, url_for, request, redirect, logging
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
import mysql.connector


mydb = mysql.connector.connect(host="localhost", user="root", password="", database="project")
cursor = mydb.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

# Login and SignUp Pages
@app.route("/userLogin", methods=["POST", "GET"])
def userLogin():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        cursor.execute("SELECT * FROM user WHERE email='" + email + "' AND password='" + password + "'")
        data =[]
        data = cursor.fetchall()

        if data is None:
            return render_template("user_login.html")
        else:
            return redirect(url_for("user", name=data))
    return render_template("user_login.html")

UPLOAD_FOLDER = "C:/Users/malik/Desktop/Flask/static/img/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/userSign", methods=["POST", "GET"])
def userSign():
    if request.method == "POST":
         firstname = request.form.get("firstname")
         lastname = request.form.get("lastname")
         email = request.form.get("email")
         password = request.form.get("password")
         confirm = request.form.get("confirm")
         dob = request.form.get("dob")
         gender = request.form.get("gender")
         
         if password == confirm:
            query = "INSERT INTO users (firstname, lastname, gender, date_of_birth, email, password) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (firstname, lastname, gender, dob, email, password ))
            mydb.commit()
            return redirect(url_for("userLogin"))
         else:
            return render_template("user_signup.html")
            
    return render_template("user_signup.html")

@app.route("/adminLogin", methods=["POST", "GET"])
def adminLogin():
    if request.method == "POST":
        adminname = request.form.get("adminname")
        password = request.form.get("password")
        cursor.execute("SELECT * FROM admin WHERE adminname='" + adminname + "' AND password='" + password + "'")
        data = cursor.fetchone()

        if data is None:
            return render_template("admin_login.html")
        else:
            return redirect(url_for("admin"))
    return render_template("admin_login.html")

@app.route("/logout")
def logout():
    return render_template("index.html")

#Profile Pages
@app.route("/userProf/<name>", methods=["GET", "POST"])
def user(name):
    return render_template("user_prof.html", name=name)

@app.route("/adminProf", methods=["GET"])
def admin():
    cursor.execute("SELECT * FROM users")
    data = cursor.fetchall()
    return render_template("admin_prof.html", users= data)
    
@app.route("/userProfEdit")
def useredit():
    return render_template("/user_edit.html")


if __name__ == "__main__":
    app.run(debug=True)
