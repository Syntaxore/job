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

# Модель объявления о работе
class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(50), nullable=False)
    schedule = db.Column(db.String(50), nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    number = db.Column(db.String(15), nullable=False)

    user = db.relationship('User', backref=db.backref('jobs', lazy=True))

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
            return redirect(url_for("main"))
        else:
            flash("Неверный пароль", "danger")
    return render_template("login.html")

# Главная страница
@app.route("/main", methods=['GET', "POST"])
def main():
    if g.user is None:
        flash("Пожалуйста, авторизуйтесь, чтобы просматривать объявления.", "danger")
        return redirect(url_for("login_view"))

    jobs = Job.query.all()  # Получаем все вакансии
    return render_template("main.html", jobs=jobs)

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

# Маршрут для личного кабинета
@app.route("/profile")
def profile():
    if g.user is None:
        flash("Пожалуйста, войдите в систему, чтобы получить доступ к личному кабинету.", "danger")
        return redirect(url_for("login_view"))
    return render_template("profile.html", user=g.user)

# Маршрут для создания вакансии
@app.route("/create", methods=["GET", "POST"])
def create():
    if g.user is None:
        flash("Пожалуйста, войдите в систему, чтобы создать вакансию.", "danger")
        return redirect(url_for("login_view"))

    if request.method == "POST":
        title = request.form['title']
        salary = request.form['salary']
        schedule = request.form['schedule']
        requirements = request.form['requirements']
        number = request.form['number']

        new_job = Job(title=title, salary=salary, schedule=schedule, requirements=requirements, user_id=g.user.id, number=number)
        db.session.add(new_job)
        db.session.commit()
        flash("Вакансия успешно создана!", "success")
        return redirect(url_for("main"))

    return render_template("create.html")

@app.before_request
def load_user():
    user_id = session.get("user_id")
    if user_id:
        g.user = User.query.get(user_id)
    else:
        g.user = None


if __name__ == "__main__":
    app.run(debug=True)
