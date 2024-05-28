import os
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify, request
from datetime import timedelta
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import Recipe, db, User, Admin, Comment, Category, CategoryGroup, FavouriteRecipe
from sqlalchemy.sql import func
from sqlalchemy import or_
from datetime import datetime



app = Flask(__name__, template_folder="templates")
app.secret_key = "hello"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads')
db.init_app(app)
migrate = Migrate(app, db)
app.permanent_session_lifetime = timedelta(minutes=100)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Check if the filename extension is allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(directory, filename):
    base, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename

    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{extension}"
        counter += 1

    return new_filename

@app.route("/")
def home():
    return render_template("home.html")

################################################################## User Route #######################################################################

######### Signup And Login ##########
@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        age = int(request.form['age'])
        password = generate_password_hash(request.form['password'])
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

        if found_user and check_password_hash(found_user.password, password):
            session["user_id"] = found_user.id
            return redirect(url_for("browse_recipes", user_id=found_user.id))
        else:
            # Incorrect email/username or password
            flash("Invalid email/username or password. Please try again.", "error")
            return redirect(url_for("login"))
    else:
        if "user_id" in session:
            return redirect(url_for("browse_recipes", user_id=session["user_id"]))

        return render_template("login.html")


########### Browse Recipe #############
@app.route("/user/<int:user_id>/browse_recipes")
def browse_recipes(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)

    # Fetch all categories from the database
    categories = Category.query.order_by(Category.name).all()  # Sort categories alphabetically

    selected_category = request.args.get("category", "All")
    search_query = request.args.get("search_query", "")

    query = Recipe.query.filter_by(approved=True)

    # Retrieve all groups and their associated categories
    groups = CategoryGroup.query.order_by(CategoryGroup.name).all()
    for group in groups:
        group.categories = Category.query.filter_by(group_id=group.id).order_by(Category.name).all()

    if selected_category != "All":
        category = Category.query.filter_by(name=selected_category).first()
        if category:
            query = query.filter(Recipe.categories.contains(category))
    
    if search_query:
        query = query.filter(Recipe.recipe_name.ilike(f"%{search_query}%"))

    recipes = query.all()

    return render_template("browse_recipes.html", recipes=recipes, groups=groups, categories=categories, selected_category=selected_category, search_query=search_query, user=user, user_id=user_id)

################### In-Depth Recipe ###################
@app.route("/user/<int:user_id>/recipe/<int:recipe_id>")
def recipe(user_id, recipe_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    recipe = Recipe.query.get_or_404(recipe_id)
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    favourite_recipe = FavouriteRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()
    favourited_recipe_ids = [fr.recipe_id for fr in FavouriteRecipe.query.filter_by(user_id=user_id).all()]
    # Get the source from the query parameter, default to 'browse_recipe' if not provided
    source = request.args.get('source', 'browse_recipe')

    return render_template("recipe.html", user=user, recipe=recipe, favourite_recipe=favourite_recipe, favourited_recipe_ids=favourited_recipe_ids, comments=comments, source=source)

@app.route('/user/<int:user_id>/submit_comment/<int:recipe_id>', methods=['POST'])
def submit_comment(user_id, recipe_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    if request.method == 'POST':
        comment = request.form['comment']
        rating = request.form['rating']
        recipe_id = request.form['recipe_id']  
        user = User.query.get_or_404(user_id)

        submitted_by = f"{user.username} (ID: {user.id})"

        image_url_relative = None

        if 'image' in request.files:
            image = request.files['image']
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                upload_directory = app.config['UPLOAD_FOLDER']
                
                # Generate a unique filename
                unique_filename = generate_unique_filename(upload_directory, filename)
                
                image_url = os.path.join(upload_directory, unique_filename)
                image.save(image_url)
                image_url_relative = os.path.join('uploads', unique_filename)
                image_url=None
        else:
            image_url= None

        comment = Comment(comment=comment, rating=rating, submitted_by=submitted_by ,recipe_id=recipe_id, image_url=image_url_relative, user_id=user_id)
        
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('recipe', user_id=session["user_id"], recipe_id=recipe_id))
        
    user = User.query.get_or_404(user_id)
    return render_template("RecipeSubmission.html", user=user)

############## Recipe Submission ################
@app.route("/user/<int:user_id>/recipesubmission", methods=["GET", "POST"])
def recipesubmission(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    if request.method == "POST":
        # Handle form submission
        recipe_name = request.form["recipe_name"]
        description = request.form["description"]
        ingredients = request.form["ingredients"]
        steps = request.form.getlist("steps[]")
        serving_size = int(request.form.get("serving_size", 1))
        difficulty = int(request.form.get("rating1", 1))
        time_required = int(request.form.get("rating2", 1))
        user = User.query.get_or_404(user_id)
        submitted_by = f"{user.username} (ID: {user.id})"

        # Get selected categories
        category_ids = request.form.getlist('categories[]')
        categories = Category.query.filter(Category.id.in_(category_ids)).all()

        if "recipe_image" in request.files:
            recipe_image = request.files["recipe_image"]
            if recipe_image.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if recipe_image and allowed_file(recipe_image.filename):
                filename = secure_filename(recipe_image.filename)
                upload_directory = app.config['UPLOAD_FOLDER']
                
                # Generate a unique filename
                unique_filename = generate_unique_filename(upload_directory, filename)
                
                image_path = os.path.join(upload_directory, unique_filename)
                recipe_image.save(image_path)
                image_path_relative = os.path.join('uploads', unique_filename)
            else:
                flash('Invalid file type')
                return redirect(request.url)
        else:
            image_path_relative = None

        steps_str = '\n'.join(steps)

        recipe = Recipe(
            recipe_name=recipe_name,
            description=description,
            ingredients=ingredients,
            steps=steps_str,
            serving_size=serving_size,
            difficulty=difficulty,
            time_required=time_required,
            image_path=image_path_relative,
            user_id=user_id,
            submitted_by=submitted_by, 
            categories=categories
        )

        db.session.add(recipe)
        db.session.commit()

        return redirect(url_for('recipesubmission', user_id=user_id))
    
    user = User.query.get_or_404(user_id)
    categories = Category.query.order_by(Category.name).all()  # Sort categories alphabetically
    # Retrieve all groups and their associated categories
    groups = CategoryGroup.query.order_by(CategoryGroup.name).all()
    for group in groups:
        group.categories = Category.query.filter_by(group_id=group.id).order_by(Category.name).all()
        
    return render_template("RecipeSubmission.html", user=user, categories=categories, groups=groups)

############## Favourited Recipes ################
@app.route("/user/<int:user_id>/favouritedrecipe")
def favouritedrecipe(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    # Fetch favorited recipes for the user
    favourited_recipes = Recipe.query.join(FavouriteRecipe).filter(FavouriteRecipe.user_id == user_id).all()
    # Get the IDs of favourited recipes
    favourited_recipe_ids = [recipe.id for recipe in favourited_recipes]

    return render_template("favourited_recipe.html", user=user, favourited_recipes=favourited_recipes, favourited_recipe_ids=favourited_recipe_ids)

@app.route("/user/<int:user_id>/favorite/<int:recipe_id>", methods=['POST'])
def favorite_recipe(user_id, recipe_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    # Check if the recipe is already favorited
    existing_favorite = FavouriteRecipe.query.filter_by(user_id=user_id, recipe_id=recipe_id).first()


    if existing_favorite:
        # If the recipe is already favorited, unfavorite it
        db.session.delete(existing_favorite)
        db.session.commit()
        flash('Recipe unfavorited successfully!', 'success')
    else:
        if request.method == "POST":
            # Extract pinned_date from the form data
            cook_on_str = request.form.get("cook_on", None)
            cook_on = datetime.strptime(cook_on_str, "%Y-%m-%d").date() if cook_on_str else None
            # If the recipe is not favorited, favorite it
            new_favorite = FavouriteRecipe(user_id=user_id, recipe_id=recipe_id, cook_on=cook_on)
        db.session.add(new_favorite)
        db.session.commit()
        flash('Recipe favorited successfully!', 'success')

    source = request.args.get('source', 'browse_recipe')

    # Redirect back to the recipe page
    return redirect(url_for('recipe', user_id=user_id, recipe_id=recipe_id, source=source))

############ Logout #############
@app.route("/logout")
def logout():
	session.pop("user_id", None)
	return redirect(url_for("login"))


##################################################################### Admin Route #########################################################################

############ Login ###############
@app.route("/adminlogin", methods=["POST", "GET"])
def adminlogin():
    if request.method == "POST":
        session.permanent = True
        email_admin = request.form["email_admin"]
        password_admin_input = request.form["password_admin"]

        # Check if the admin exists in the database
        found_admin = Admin.query.filter_by(email_admin=email_admin).first()

        if found_admin and check_password_hash(found_admin.password_admin, password_admin_input):
            session["admin_id"] = found_admin.id
            return redirect(url_for("pending_submissions", admin_id=found_admin.id))
        else:
            flash("Invalid email or password. Please try again.", "error")
            return redirect(url_for("adminlogin"))
    else:
        if "admin_id" in session:
            return redirect(url_for("pending_submissions", admin_id=session["admin_id"]))

        return render_template("admin_login.html")

########### Pending Submissions ###########
@app.route("/admin/<int:admin_id>/pending_submissions")
def pending_submissions(admin_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))

    admin = Admin.query.get_or_404(admin_id)

    # Query pending recipe submissions
    pending_recipes = Recipe.query.filter_by(approved=False).all()
    
    return render_template("pending_submissions.html", recipes=pending_recipes, admin_id=admin_id, admin=admin)

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
    
    return redirect(url_for("pending_submissions", admin_id=admin_id, admin=admin))

############ Browse Recipes ##############
@app.route("/admin/<int:admin_id>/browse_recipes", methods=["GET"])
def admin_browse_recipes(admin_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))

    admin = Admin.query.get_or_404(admin_id)

    categories = Category.query.order_by(Category.name).all()
    selected_category = request.args.get("category", "All")
    search_query = request.args.get("search_query", "")

    query = Recipe.query.filter_by(approved=True)

    # Retrieve all groups and their associated categories
    groups = CategoryGroup.query.order_by(CategoryGroup.name).all()
    for group in groups:
        group.categories = Category.query.filter_by(group_id=group.id).order_by(Category.name).all()

    if selected_category != "All":
        category = Category.query.filter_by(name=selected_category).first()
        if category:
            query = query.filter(Recipe.categories.contains(category))

    if search_query:
        query = query.filter(Recipe.recipe_name.ilike(f"%{search_query}%"))

    recipes = query.all()

    return render_template("admin_browse_recipes.html", recipes=recipes, groups=groups, categories=categories, selected_category=selected_category, search_query=search_query, admin=admin, admin_id=admin_id)

@app.route("/admin/<int:admin_id>/delete_recipe/<int:recipe_id>", methods=["POST"])
def delete_recipe(admin_id, recipe_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))

    recipe = Recipe.query.get_or_404(recipe_id)

    db.session.delete(recipe)
    db.session.commit()
    # Delete the associated image file
    if recipe.image_path:
        image_path = os.path.join(app.root_path, 'static', recipe.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    flash("Recipe deleted successfully", "success")
    return redirect(url_for("admin_browse_recipes", admin_id=admin_id))

########### In-Depth Recipe ############
@app.route('/admin/<int:admin_id>/recipe/<int:recipe_id>', methods=['GET', 'POST'])
def admin_recipe(admin_id, recipe_id):
    # Fetch the recipe and comments from the database
    admin = Admin.query.get_or_404(admin_id)
    recipe = Recipe.query.get_or_404(recipe_id)
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    

    return render_template('admin_recipe.html',admin=admin, recipe=recipe, comments=comments)


@app.route('/admin/<int:admin_id>/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(admin_id,comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Delete the comment from the database
    db.session.delete(comment)
    db.session.commit()
    # Delete the associated image file
    if comment.image_url:
        image_url = os.path.join(app.root_path, 'static', comment.image_url)
        if os.path.exists(image_url):
            os.remove(image_url)
    flash('Comment deleted successfully', 'success')
    return redirect(url_for('admin_recipe', admin_id=admin_id, recipe_id=comment.recipe_id))

########## Edit Categories Groups #############
@app.route("/admin/<int:admin_id>/edit_category_groups")
def edit_category_groups(admin_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)
    groups = CategoryGroup.query.order_by(CategoryGroup.name).all()

    return render_template("edit_category_groups.html", admin_id=admin_id, admin=admin, groups=groups)

@app.route("/admin/<int:admin_id>/add_category_group", methods=["POST"])
def add_category_group(admin_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)

    if request.method == "POST":
        name = request.form["name"]
        group = CategoryGroup(name=name)
        db.session.add(group)
        db.session.commit()
        flash("Category group added successfully", "success")
        return redirect(url_for("edit_category_groups", admin_id=admin_id))

@app.route("/admin/<int:admin_id>/update_category_group/<int:group_id>", methods=["POST"])
def update_category_group(admin_id, group_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)
    group = CategoryGroup.query.get_or_404(group_id)

    if request.method == "POST":
        new_name = request.form["new_name"]
        group.name = new_name
        db.session.commit()
        flash("Category group updated successfully", "success")
    return redirect(url_for("edit_category_groups", admin_id=admin_id))

@app.route("/admin/<int:admin_id>/delete_category_group/<int:group_id>", methods=["POST"])
def delete_category_group(admin_id, group_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)
    group = CategoryGroup.query.get_or_404(group_id)

    db.session.delete(group)
    db.session.commit()
    flash("Category group deleted successfully", "success")
    return redirect(url_for("edit_category_groups", admin_id=admin_id))

############ Edit Categories #############
@app.route("/admin/<int:admin_id>/edit_categories")
def edit_categories(admin_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    admin = Admin.query.get_or_404(admin_id)

    groups = CategoryGroup.query.order_by(CategoryGroup.name).all()
    selected_group = request.args.get("group", "All")
    search_query = request.args.get("search_query", "")
    query = Category.query

    if selected_group != "All":
        group = CategoryGroup.query.filter_by(name=selected_group).first()
        if group:
            query = query.filter(Category.group_id == group.id)

    if search_query:
        query = query.filter(Category.name.ilike(f"%{search_query}%"))

    categories = Category.query.order_by(Category.name).all()  # Sort categories alphabetically

    return render_template("edit_categories.html", admin_id=admin_id, admin=admin, categories=categories, groups=groups, selected_group=selected_group, search_query=search_query)

    

@app.route("/admin/<int:admin_id>/add_category", methods=["POST"])
def add_category(admin_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)

    if request.method == "POST":
        name = request.form["name"]
        group_id = request.form.get("group_id")
        category = Category(name=name, group_id=group_id)
        db.session.add(category)
        db.session.commit()
        flash("Category added successfully", "success")
        return redirect(url_for("edit_categories",admin=admin, admin_id=admin_id))

@app.route("/admin/<int:admin_id>/delete_category/<int:category_id>", methods=["POST"])
def delete_category(admin_id,category_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)

    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Category deleted successfully", "success")
    return redirect(url_for("edit_categories",admin=admin, admin_id=admin_id))

@app.route("/admin/<int:admin_id>/update_category/<int:category_id>", methods=["GET", "POST"])
def update_category(admin_id, category_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))

    admin = Admin.query.get_or_404(admin_id)
    category = Category.query.get_or_404(category_id)

    if request.method == "POST":
        new_name = request.form["new_name"]
        group_id = request.form.get("group_id")
        category.name = new_name
        category.group_id = group_id
        db.session.commit()
        flash("Category updated successfully", "success")
    return redirect(url_for("edit_categories",admin=admin, admin_id=admin_id))

@app.route("/admin/<int:admin_id>/category_usage/<int:category_id>")
def category_usage(admin_id, category_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))

    category = Category.query.get_or_404(category_id)
    recipe_count = Recipe.query.filter(Recipe.categories.any(id=category_id)).count()
    return jsonify({"recipe_count": recipe_count})

############### Manage Users ################
@app.route("/admin/<int:admin_id>/manage_users")
def manage_users(admin_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)

    search_query = request.args.get('search_query', '').strip()
    
    if search_query:
        users = User.query.filter(User.username.contains(search_query)).all()
    else:
        users = User.query.all()

    return render_template("manage_users.html", admin_id=admin_id, admin=admin, users=users, search_query=search_query)

@app.route("/admin/<int:admin_id>/delete_user/<int:user_id>", methods=["POST"])
def delete_user(admin_id, user_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))

    admin = Admin.query.get_or_404(admin_id)
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully", "success")
    return redirect(url_for("manage_users", admin_id=admin_id))

############### Logout ##################
@app.route("/adminlogout")
def adminlogout():
	session.pop("admin_id", None)
	return redirect(url_for("adminlogin"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)