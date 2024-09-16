from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=['GET', "POST"])
def home():
    return render_template("register.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        return f"Вы зарегистрированы! Логин: {username}, Пароль: {password}"
    return render_template("register.html")

if __name__ == "__main__":
    app.run(debug=True)
