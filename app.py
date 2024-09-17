from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "secretkey"


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)  # Исправлено здесь
    password = db.Column(db.String(150), nullable=False)

with app.app_context():
    db.create_all()

@app.route("/", methods=['GET', "POST"])
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация прошла успешно!", 'success')
        return redirect(url_for('register'))
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
