from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.secret_key = "secretkey"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

with app.app_context():
    db.create_all()

@app.route("/login", methods=["GET", "POST"])
def login_view():  # Измените имя функции на login_view
    form = LoginForm()
    if form.validate_on_submit():  # Исправлено на validate_on_submit
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Сравнение паролей без хеширования
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html", form=form)  # Переместите return сюда

@app.route("/dashboard")
def dashboard():
    return "Welcome to the dashboard!"

@app.route("/", methods=['GET', "POST"])
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        new_user = User(username=username, password=password)  # Сохраняем пароль в открытом виде
        db.session.add(new_user)
        db.session.commit()

        flash("Регистрация прошла успешно!", 'success')
        return redirect(url_for('login_view'))  # Перенаправление на страницу входа
    return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)
