from flask import Flask,request,render_template,session,url_for,redirect
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.secret_key="my secretkey"

app.config["SQLALCHEMY_DATABASE_URI"]='mysql+pymysql://root:@localhost:3306/flask_db'
app.config["SQLALCHEMY_TRACK_MODIFICATION"]=False

db=SQLAlchemy(app)

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(100),unique=True)
    password=db.Column(db.String(100))

class Student(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))
    course=db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        exsiting_user=User.query.filter_by(username=username).first()
        if exsiting_user:
         return "Username Alreary exsits!"
    
        new_user=User(username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        
        return "Account Create Successfully"
    
    return render_template("register.html")

@app.route("/",methods=["POST","GET"])
def login():
    if request.method=="POST":
        username=request.form["username"]
        password=request.form["password"]

        user=User.query.filter_by(username=username,password=password).first()

        if user:
            session["user"]=user.username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid Login"
    return render_template("login.html")

@app.route("/dashboard",methods=["POST","GET"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    
    students=Student.query.all()
    return render_template("dashboard.html",students=students)

@app.route("/add",methods=["POST","GET"])
def add():
    if "user" not in session:
        return redirect(url_for("login"))
    
    if request.method=="POST":
        name=request.form["name"]
        email=request.form["email"]
        course=request.form["course"]

        new_student=Student(name=name,email=email,course=course)
        db.session.add(new_student)
        db.session.commit()

        return redirect(url_for("dashboard"))
    return render_template("add.html")

@app.route("/edit/<int:id>",methods=["POST","get"])
def edit(id):
    if "user" not in session:
        return redirect(url_for("login"))
    
    student=Student.query.get(id)
    if request.method=="POST":
        student.name=request.form["name"]
        student.email=request.form["email"]
        student.course=request.form["course"]
        db.session.commit()

        return redirect(url_for("dashboard"))
    return render_template("edit.html",student=student)

@app.route("/delete/<int:id>",methods=["POST","GET"])
def delete(id):
    if "user" not in session:
        return redirect(url_for("login"))
    student=Student.query.get(id)
    
    if request.method=="POST":
        student.name=request.form["name"]
        student.email=request.form["email"]
        student.course=request.form["course"]

        db.session.delete(student)
        db.session.commit()
        return redirect("dashboard")
    
@app.route("/logout")
def logout():
    session.pop("user",None)
    return redirect(url_for("login"))

if __name__== "__main__":
    app.run(debug=True)

    

    
