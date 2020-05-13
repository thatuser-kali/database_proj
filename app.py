import os
from flask import Flask, render_template, url_for, request, redirect, logging
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from flask_sqlalchemy import  SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=('mysql://root:''@localhost/mybook_lazy')
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")

# Login and SignUp Pages
@app.route("/userLogin", methods=["POST", "GET"])
def userLogin():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        usernamedb = db.execute("SELECT username FROM admin WHERE username:=username", {"username":username}).fetchone()
        passworddb = db.execute("SELECT password FROM admin WHERE password:=password", {"password":password}).fetchone()

        if usernamedb  is None:
            return render_template("user_login.html")
        else:
            for pass_word in passworddb:
                if sha256_crypt.verfiy(password, pass_word):
                    return redirect(url_for("userProf"))
                else:
                    return render_template("user_login.html")
    return render_template("user_login.html")
    

@app.route("/userSign", methods=["POST", "GET"])
def userSign():
    if request.method == "POST":
         firstname = request.form["firstname"]
         lastname = request.form["lastname"]
         username = request.form["username"]
         email = request.form["email"]
         password = request.form["password"]
         confirm = request.form["confirm"]
         dob = request.form["dob"]
         gender = request.form["gender"]
         profilePic = request.files["profilePic"]
         profilePic.save(profilePic.filename)
         
         pic=profilePic.filename

         if profilePic.filename == "":
            return redirect(url_for("userSign"))

         if password == confirm:
            db.execute("INSERT INTO users (f_name, l_name, username, email, password, DOB, gender, profilePic) VALUES (:firstname, :lastname, :username, :email, :password, :DOB, :gender, :profilePic)",
            {"f_name":firstname, "l_name":lastname, "username":username, "email":email, "password":password, "DOB":dob, "gender":gender, "profilePic":pic})
            db.commit()
            return redirect(url_for("userLogin"))
         else:
            return render_template("user_signup.html")
            
    return render_template("user_signup.html")

@app.route("/adminLogin", methods=["POST", "GET"])
def adminLogin():
    if request.method == "POST":
        adminname = request.form["adminname"]
        password = request.form["password"]

        adminnamedb = db.execute("SELECT adminname FROM admin WHERE adminname:=adminname", {"adminname":adminname}).fetchone()
        passworddb = db.execute("SELECT password FROM admin WHERE password:=password",{"password":password}).fetchone()

        if adminnamedb  is None:
            return render_template("admin_login.html")
        else:
            for pass_word in passworddb:
                if sha256_crypt.verfiy(password, pass_word):
                    return redirect(url_for("admin"))
                else:
                    return render_template("admin_login.html")
                    
    return render_template("admin_login.html")

@app.route("/logout")
def logout():
    return render_template("index.html")


#Profile Pages
@app.route("/userProf")
def user():
    return render_template("user_prof.html")

@app.route("/adminProf")
def admin():
    return render_template("admin_prof.html")
    

@app.route("/userProfEdit")
def useredit():
    if pic:
        filename = secure_filename(profilePic.filename)
        profilePic.save(os.path.join(app.config["IMAGE_UPLOADS"], filename))
    return render_template("/user_edit.html")


if __name__ == "__main__":
    app.run(debug=True)
