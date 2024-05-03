import os
from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_migrate import Migrate


from sqlalchemy.sql import func
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder="templates")
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.permanent_session_lifetime = timedelta(minutes=100)

migrate=Migrate(app, db)
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

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_admin = db.Column(db.String(100), nullable=False)
    email_admin = db.Column(db.String(80), unique=True, nullable=False)
    password_admin = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Admin {self.name_admin}>'

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)
    taste = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('recipe_submissions', lazy=True))

    def __repr__(self):
        return f'<RecipeSubmission {self.recipe_name}>'

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

@app.route("/adminlogin", methods=["POST", "GET"])
def adminlogin():
    if request.method == "POST":
        session.permanent = True
        email_admin = request.form["email_admin"]
        name_admin = request.form["name_admin"]
        password_admin = request.form["password_admin"]

        # Check if the admin exists in the database
        found_admin = Admin.query.filter_by(email_admin=email_admin, name_admin=name_admin).first()

        if found_admin and found_admin.password_admin == password_admin:
            session["admin_id"] = found_admin.id
            return redirect(url_for("admin", admin_id=found_admin.id))
        else:
            return redirect(url_for("adminlogin"))
    else:
        if "admin_id" in session:
            return redirect(url_for("admin", admin_id=session["admin_id"]))

        return render_template("admin_login.html")

@app.route('/user/<int:user_id>/')
def user(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    return render_template('user.html', user=user)

@app.route('/admin/<int:admin_id>/')
def admin(admin_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)
    return render_template('admin.html', admin=admin)

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

@app.route("/user/<int:user_id>/recipesubmission", methods=["GET", "POST"])
def recipesubmission(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    if request.method == "POST":
        recipe_name = request.form["recipe_name"]
        description = request.form["description"]
        ingredients = request.form["ingredients"]
        steps = request.form["steps"]
        difficulty = int(request.form.get("rating1", 1))
        time_required = int(request.form.get("rating2", 1))
        taste = int(request.form.get("rating3", 1))

        # Create a new Recipe object
        recipe = Recipe(
            recipe_name=recipe_name,
            description=description,
            ingredients=ingredients,
            steps=steps,
            difficulty=difficulty,
            time_required=time_required,
            taste=taste,
            user_id=user_id
        )

        # Add the recipe to the database session and commit changes
        db.session.add(recipe)
        db.session.commit()

        # Redirect to a success page or home page
        return redirect(url_for('user', user_id=user_id))
    user = User.query.get_or_404(user_id)
    # Render the RecipeSubmission.html page for GET requests
    return render_template("RecipeSubmission.html", user=user)

@app.route("/logout")
def logout():
	session.pop("user_id", None)
	return redirect(url_for("login"))

@app.route("/adminlogout")
def adminlogout():
	session.pop("admin_id", None)
	return redirect(url_for("adminlogin"))

if __name__ == "__main__":
	with app.app_context():
		db.create_all()
		app.run(debug=True)


# @app.route('/signupadmin', methods=('GET', 'POST'))
# def signupadmin():
#     if request.method == 'POST':
#         email_admin = request.form['email_admin']
#         name_admin = request.form['name_admin']
#         password_admin = request.form['password_admin']
#         admin = Admin(email_admin=email_admin,
# 					name_admin=name_admin,
# 					password_admin=password_admin)
#         db.session.add(admin)
#         db.session.commit()

#         return redirect(url_for('home'))

#     return render_template("signupadmin.html")
