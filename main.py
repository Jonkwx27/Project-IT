import os
from flask import Flask, redirect, url_for, render_template, request, session, flash, send_from_directory
from datetime import timedelta
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from models import Recipe, db, User, Admin, Comment


UPLOAD_FOLDER = 'uploads'  # Directory to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

basedir = os.path.abspath(os.path.dirname(__file__))

UPLOAD_FOLDER = 'uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder="templates")
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#db = SQLAlchemy(app)
# app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'uploads')
db.init_app(app)  

app.permanent_session_lifetime = timedelta(minutes=100)

migrate=Migrate(app, db)




# Check if the filename extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")

################################################################## User Route ################################################################

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

@app.route("/user/<int:user_id>/browse_recipe")
def browse_recipe(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)

    categories = ["Breakfast", "Lunch", "Dinner", "Dessert", "Beverage", "Soup"]
    selected_category = request.args.get("category", "All")
    
    if selected_category == "All":
        recipes = Recipe.query.all()
    else:
        recipes = Recipe.query.filter_by(category=selected_category).all()
    
    return render_template("browse_recipe.html", recipes=recipes, categories=categories, selected_category=selected_category, user=user)

@app.route("/user/<int:user_id>/recipe/<int:recipe_id>")
def recipe(user_id,recipe_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    recipe = Recipe.query.get_or_404(recipe_id)

    comments = Comment.query.all()

    return render_template("recipe.html", user=user, recipe=recipe, comments=comments)

# @app.route('/recipes')
# def recipe_details():
#     recipe = Recipe.query.first()
#     comments = Comment.query.all()  
#     return render_template('in-depth.html', recipe=recipe, comments=comments)

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if request.method == 'POST':
        comment_text = request.form['comment']
        rating = request.form['rating']
        recipe_id = request.form['recipe_id']  

        if 'image' in request.files:
            image = request.files['image']
            if image.filename != '':
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = url_for('uploaded_file', filename=filename)
            else:
                image_url = None
        else:
            image_url = None

        comment = Comment(comment=comment_text, rating=rating, recipe_id=recipe_id, image_url=image_url)
        
        try:
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('recipe_details'))
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            db.session.rollback()
            return "Error occurred while submitting the comment"
        
# @app.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
        user = User.query.get_or_404(user_id)
        submitted_by = f"{user.username} (ID: {user.id})"
        category = request.form["category"]

        if "recipe_image" in request.files:
            recipe_image = request.files["recipe_image"]
            if recipe_image.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if recipe_image and allowed_file(recipe_image.filename):
                filename = secure_filename(recipe_image.filename)
                # Construct the absolute path to save the image
                image_path = os.path.join(app.root_path, 'static/uploads', filename)
                # Save the image to the correct directory
                recipe_image.save(image_path)
                # Save the relative path to the image file in the database
                image_path_relative = 'uploads/' + filename
            else:
                flash('Invalid file type')
                return redirect(request.url)
        else:
            image_path_relative = None

        recipe = Recipe(
            recipe_name=recipe_name,
            description=description,
            ingredients=ingredients,
            steps=steps,
            difficulty=difficulty,
            time_required=time_required,
            taste=taste,
            image_path=image_path_relative,
            user_id=user_id,
            submitted_by=submitted_by, 
            category=category
        )

        # Add the recipe to the database session and commit changes
        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for('user', user_id=user_id))
    
    user = User.query.get_or_404(user_id)
    return render_template("RecipeSubmission.html", user=user)


@app.route("/logout")
def logout():
	session.pop("user_id", None)
	return redirect(url_for("login"))


##################################################################### Admin Route #########################################################################



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

@app.route('/admin/<int:admin_id>/')
def admin(admin_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)
    return render_template('admin.html', admin=admin)

@app.route("/admin/<int:admin_id>/pending_submissions")
def pending_submissions(admin_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))

    # Query pending recipe submissions
    pending_recipes = Recipe.query.filter_by(approved=False).all()
    
    return render_template("pending_submissions.html", recipes=pending_recipes, admin_id=admin_id)

@app.route("/admin/<int:admin_id>/approve_recipe/<int:recipe_id>", methods=["POST"])
def approve_recipe(admin_id, recipe_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))
    
    # Find the recipe by ID
    recipe = Recipe.query.get_or_404(recipe_id)
  
    recipe.approved = True
    db.session.commit()
    
    return redirect(url_for("pending_submissions", admin_id=admin_id))


@app.route("/admin/<int:admin_id>/reject_recipe/<int:recipe_id>", methods=["POST"])
def reject_recipe(admin_id, recipe_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)

    # Find the recipe by ID
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    # Delete the associated image file
    if recipe.image_path:
        image_path = os.path.join(app.root_path, 'static', recipe.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    return redirect(url_for("pending_submissions", admin_id=admin_id))


@app.route("/adminlogout")
def adminlogout():
	session.pop("admin_id", None)
	return redirect(url_for("adminlogin"))


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
		app.run(debug=True)