import os
from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

from sqlalchemy.sql import func
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder="templates")
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.permanent_session_lifetime = timedelta(minutes=5)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self):
        return f'<User {self.name}>'

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        age = int(request.form['age'])
        password = request.form['password']
        user = User(name=name,
					email=email,
					username=username,
					age=age,
					password=password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('home'))

    return render_template("sign_up.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]

        # Check if the user exists in the database
        found_user = User.query.filter_by(email=email, username=username).first()

        if found_user and found_user.password == password:
            session["user_id"] = found_user.id
            return redirect(url_for("user", user_id=found_user.id))
        else:
            return redirect(url_for("login"))
    else:
        if "user_id" in session:
            return redirect(url_for("user", user_id=session["user_id"]))

        return render_template("login.html")


@app.route('/user/<int:user_id>/')
def user(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route("/user/<int:user_id>/browsebreakfast")
def browsebreakfast(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template("BrowseBreakfast.html", user=user)

@app.route("/user/<int:user_id>/browsebeverage")
def browsebeverage(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template("BrowseBeverage.html", user=user)

@app.route("/user/<int:user_id>/browsedessert")
def browsedessert(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template("BrowseDessert.html", user=user)

@app.route("/user/<int:user_id>/browsedinner")
def browsedinner(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template("BrowseDinner.html", user=user)

@app.route("/user/<int:user_id>/browselunch")
def browselunch(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template("BrowseLunch.html", user=user)

@app.route("/user/<int:user_id>/browsesoup")
def browsesoup(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template("BrowseSoup.html", user=user)

@app.route("/user/<int:user_id>/recipesubmission")
def recipesubmission(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template("RecipeSubmission.html", user=user)

@app.route("/logout")
def logout():
	session.pop("user_id", None)
	return redirect(url_for("login"))


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
		app.run(debug=True)