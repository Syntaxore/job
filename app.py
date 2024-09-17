from flask import Flask, request, render_template, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secretkey"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

# Создание таблиц в базе данных
with app.app_context():
    db.create_all()

# Маршрут для входа
@app.route("/login", methods=["GET", "POST"])
def login_view():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash("Пользователь с таким именем не существует", "danger")
        elif check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Вход выполнен успешно!", "success")
            return redirect(url_for("base"))
        else:
            flash("Неверный логин или пароль", "danger")
    return render_template("login.html")

@app.route("/base", methods=['GET', "POST"])
def base():
    return render_template("base.html")

# Главная страница
@app.route("/", methods=['GET', "POST"])
def home():
    return render_template("home.html")

# Маршрут для регистрации
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Пользователь с таким именем уже существует!", "danger")
            return redirect(url_for('register'))
        new_user = User(username=username, password=generate_password_hash(password))
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Регистрация прошла успешно!", 'success')
            return redirect(url_for('login_view'))
        except Exception as e:
            db.session.rollback()
            flash("Ошибка при регистрации: " + str(e), "danger")
    return render_template('register.html')

# Маршрут для выхода из системы
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Вы вышли из системы", "success")
    return redirect(url_for("home"))

@app.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id:
        g.user = User.query.get(user_id)
    else:
        g.user = None

if __name__ == "__main__":
    app.run(debug=True)
