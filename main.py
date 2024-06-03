import os
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify, request
from datetime import timedelta
from flask_migrate import Migrate
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from models import Recipe, db, User, Admin, Comment, Category, CategoryGroup, FavouriteRecipe, Report, Notification
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
        flash("Account created successfully!", "success")
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
            flash("You have been successfully logged in!", "success")
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
    page = request.args.get("page", 1, type=int)
    per_page = 20

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

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    recipes = pagination.items

    return render_template("browse_recipes.html", recipes=recipes, groups=groups, categories=categories, selected_category=selected_category, search_query=search_query, user=user, user_id=user_id,pagination=pagination)

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

################ Submit Comment #################
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

############## Report Recipes #############
@app.route('/user/<int:user_id>/report_recipe/<int:recipe_id>', methods=['GET', 'POST'])
def report_recipe(user_id,recipe_id):

    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        report_text = request.form.get('report_text')
        report = Report(user_id=user_id, recipe_id=recipe_id, report_text=report_text)
        db.session.add(report)
        db.session.commit()
        flash('Your report has been submitted.', 'success')
        return redirect(url_for('recipe', user_id=user_id, recipe_id=recipe_id))

    return render_template('report_recipe.html', recipe_id=recipe_id, user_id=user_id, user=user)

############# Report Comments ##############
@app.route('/user/<int:user_id>/report_comment/<int:recipe_id>/<int:comment_id>', methods=['GET', 'POST'])
def report_comment(user_id,comment_id, recipe_id):

    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        report_text = request.form.get('report_text')
        report = Report(user_id=user_id, comment_id=comment_id, report_text=report_text, recipe_id=recipe_id)
        db.session.add(report)
        db.session.commit()
        flash('Your report has been submitted.', 'success')
        return redirect(url_for('recipe', recipe_id=recipe_id, user_id=user_id))

    return render_template('report_comment.html', comment_id=comment_id, user_id=user_id, user=user, recipe_id=recipe_id)


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
                flash('No selected file','error')
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
                flash('Invalid file type','error')
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
        flash('Recipe submitted successfully!','success')
        return redirect(url_for('recipesubmission', user_id=user_id))
    
    user = User.query.get_or_404(user_id)
    categories = Category.query.order_by(Category.name).all()  # Sort categories alphabetically
    # Retrieve all groups and their associated categories
    groups = CategoryGroup.query.order_by(CategoryGroup.name).all()
    for group in groups:
        group.categories = Category.query.filter_by(group_id=group.id).order_by(Category.name).all()
        
    return render_template("RecipeSubmission.html", user=user, categories=categories, groups=groups)

################## Submitted Recipes ######################
@app.route("/user/<int:user_id>/submitted_recipes")
def submitted_recipes(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    user = User.query.get_or_404(user_id)
    recipes = Recipe.query.filter_by(user_id=user_id).all()

    return render_template("submitted_recipes.html", user=user, recipes=recipes)

############### Edit Recipes ##################
@app.route("/user/<int:user_id>/edit_recipe/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(user_id, recipe_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    user = User.query.get_or_404(user_id)
    recipe = Recipe.query.get_or_404(recipe_id)
    categories = Category.query.all()

    if request.method == "POST":
        recipe_name = request.form["recipe_name"]
        description = request.form["description"]
        ingredients = request.form["ingredients"]
        steps = request.form.getlist("steps[]")
        serving_size = int(request.form.get("serving_size", 1))
        difficulty = int(request.form.get("rating1", 1))
        time_required = int(request.form.get("rating2", 1))
        categories_selected = request.form.getlist("categories[]")

        recipe.recipe_name = recipe_name
        recipe.description = description
        recipe.ingredients = ingredients
        recipe.steps = '\n'.join(steps)
        recipe.serving_size = serving_size
        recipe.difficulty = difficulty
        recipe.time_required = time_required

        selected_category_ids = set(int(cat_id) for cat_id in categories_selected)
        current_category_ids = set(category.id for category in recipe.categories)

        new_category_ids = selected_category_ids - current_category_ids
        for cat_id in new_category_ids:
            category = Category.query.get_or_404(cat_id)
            recipe.categories.append(category)

        removed_category_ids = current_category_ids - selected_category_ids
        for cat_id in removed_category_ids:
            category = Category.query.get_or_404(cat_id)
            recipe.categories.remove(category)

        if "recipe_image" in request.files:
            recipe_image = request.files["recipe_image"]
            if recipe_image.filename:
                if recipe_image and allowed_file(recipe_image.filename):
                    filename = secure_filename(recipe_image.filename)

                    if recipe.image_path:
                        old_image_path = os.path.join(app.root_path, 'static', recipe.image_path)
                        if os.path.exists(old_image_path):
                            os.remove(old_image_path)

                    image_path = os.path.join(app.root_path, 'static/uploads', filename)
                    recipe_image.save(image_path)

                    recipe.image_path = 'uploads/' + filename

        db.session.commit()

        return redirect(url_for("recipe", user_id=user_id, recipe_id=recipe_id))

    return render_template("edit_recipe.html", user=user, recipe=recipe, categories=categories)

############## Favourited Recipes ################
@app.route("/user/<int:user_id>/favouritedrecipe")
def favouritedrecipe(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)
    
    # Fetch favorited recipes for the user and their cook_on dates
    favourited_recipes_with_cook_on = db.session.query(Recipe, FavouriteRecipe.cook_on)\
        .join(FavouriteRecipe, Recipe.id == FavouriteRecipe.recipe_id)\
        .filter(FavouriteRecipe.user_id == user_id).all()

    # Extracting Recipe objects and cook_on dates from the query result
    favourited_recipes = [recipe_cook_on[0] for recipe_cook_on in favourited_recipes_with_cook_on]
    cook_on_dates = [recipe_cook_on[1] for recipe_cook_on in favourited_recipes_with_cook_on]

    # Get sorting criteria from the request args
    sort_by = request.args.get("sort_by", "none")

    if sort_by == "alphabetical":
        favourited_recipes_with_cook_on = sorted(favourited_recipes_with_cook_on, key=lambda r: r[0].recipe_name)
    elif sort_by == "cook_on":
        favourited_recipes_with_cook_on = sorted(favourited_recipes_with_cook_on, key=lambda r: r[1] if r[1] else datetime.min)


    # Get the IDs of favourited recipes
    favourited_recipe_ids = [recipe.id for recipe in favourited_recipes]

    return render_template("favourited_recipe.html", user=user, favourited_recipes=favourited_recipes_with_cook_on, cook_on_dates=cook_on_dates, favourited_recipe_ids=favourited_recipe_ids, sort_by=sort_by)

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

########### View Notifications ################
@app.route('/user/<int:user_id>/notifications')
def view_notifications(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    user = User.query.get_or_404(user_id)
    unread_notifications = Notification.query.filter_by(user_id=user_id, read=False).order_by(Notification.timestamp.desc()).all()
    read_notifications = Notification.query.filter_by(user_id=user_id, read=True).order_by(Notification.timestamp.desc()).all()

    return render_template('notifications.html', user=user, unread_notifications=unread_notifications, read_notifications=read_notifications)

@app.route('/user/<int:user_id>/notifications/read/<int:notification_id>', methods=['POST'])
def mark_notification_as_read(user_id,notification_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    user = User.query.get_or_404(user_id)
    notification = Notification.query.get_or_404(notification_id)
    notification.read = True
    db.session.commit()
    flash('Notification marked as read.', 'success')
    return redirect(url_for('view_notifications', user_id=user_id, user=user))

@app.route('/user/<int:user_id>/notifications/unread/<int:notification_id>', methods=['POST'])
def mark_notification_as_unread(user_id,notification_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))

    user = User.query.get_or_404(user_id)
    notification = Notification.query.get_or_404(notification_id)
    notification.read = False
    db.session.commit()
    flash('Notification marked as unread.', 'success')
    return redirect(url_for('view_notifications', user_id=user_id, user=user))

############ User Profile ##############
@app.route("/user/<int:user_id>/userprofile")
def user_profile(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect(url_for("login"))
    
    user = User.query.get_or_404(user_id)

    return render_template("user_profile.html", user=user)

############## Edit Profile ################
@app.route("/edit_profile/<int:user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    user = User.query.get_or_404(user_id)
    update_message = None
    password_message = None
    
    if request.method == "POST":
        if request.form.get("action") == "update_profile":
            user.username = request.form.get("username")
            user.email = request.form.get("email")
            user.age = int(request.form.get("age"))
            db.session.commit()
            update_message = "Profile updated successfully!"
        
        elif request.form.get("action") == "change_password":
            old_password = request.form.get("old_password")
            new_password = request.form.get("new_password")
            if user.check_password(old_password):
                user.set_password(new_password)
                db.session.commit()
                password_message = "Password changed successfully!"
            else:
                password_message = "Old password is incorrect!"
    
    return render_template("edit_profile.html", user=user, update_message=update_message, password_message=password_message)

############ Logout #############
@app.route("/logout")
def logout():
    flash('Log out successfully!','success')
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
            flash("You have been successfully logged in!","success")
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
    page = request.args.get("page", 1, type=int)
    per_page = 20

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


    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    recipes = pagination.items

    return render_template("admin_browse_recipes.html", recipes=recipes, groups=groups, categories=categories, selected_category=selected_category, search_query=search_query, admin=admin, admin_id=admin_id, pagination=pagination)

@app.route("/admin/<int:admin_id>/delete_recipe/<int:recipe_id>", methods=["POST"])
def delete_recipe(admin_id, recipe_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))

    recipe = Recipe.query.get_or_404(recipe_id)

    # Create a notification for the user who submitted the recipe
    notification_message = f"Your recipe '{recipe.recipe_name}' has been deleted by the admin."
    notification = Notification(user_id=recipe.user_id, message=notification_message)
    db.session.add(notification)

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
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("admin_login"))
    # Fetch the recipe and comments from the database
    admin = Admin.query.get_or_404(admin_id)
    recipe = Recipe.query.get_or_404(recipe_id)
    comments = Comment.query.filter_by(recipe_id=recipe_id).all()
    source = request.args.get('source', 'admin_browse_recipe')

    return render_template('admin_recipe.html',admin=admin, recipe=recipe, comments=comments, source=source)


@app.route('/admin/<int:admin_id>/delete_comment/<int:comment_id>', methods=['POST'])
def delete_comment(admin_id,comment_id):
    comment = Comment.query.get_or_404(comment_id)

    # Create a notification for the user who submitted the comment
    notification_message = f"Your comment on '{comment.recipe.recipe_name}' has been deleted by the admin."
    notification = Notification(user_id=comment.user_id, message=notification_message)
    db.session.add(notification)

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
    page = request.args.get("page", 1, type=int)
    per_page = 32
    query = Category.query

    if selected_group != "All":
        group = CategoryGroup.query.filter_by(name=selected_group).first()
        if group:
            query = query.filter(Category.group_id == group.id)

    if search_query:
        query = query.filter(Category.name.ilike(f"%{search_query}%"))


    pagination = query.order_by(Category.name).paginate(page=page, per_page=per_page, error_out=False)
    categories = pagination.items


    return render_template("edit_categories.html", admin_id=admin_id, admin=admin, categories=categories, groups=groups, selected_group=selected_group, search_query=search_query, pagination=pagination)

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

@app.route("/admin/<int:admin_id>/warn_user/<int:user_id>", methods=["POST"])
def warn_user(admin_id, user_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("adminlogin"))

    admin = Admin.query.get_or_404(admin_id)
    user = User.query.get_or_404(user_id)

    user.number_of_warnings += 1

    if user.number_of_warnings > 3:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted due to exceeding warnings", "warning")
    else:
        db.session.commit()
        # Create a notification for the user
        warning_message = f"You have received a warning. Total warnings: {user.number_of_warnings}. If you are already at three warnings, your account will be deleted if you receive another warning!"
        notification = Notification(user_id=user.id, message=warning_message)
        db.session.add(notification)
        db.session.commit()
        flash("Warning issued to user", "warning")

    return redirect(url_for("manage_users", admin_id=admin_id))


############### View Reports ###################
@app.route('/admin/<int:admin_id>/view_reports', methods=['GET'])
def view_reports(admin_id):
    if "admin_id" not in session:
        return redirect(url_for("adminlogin"))
    
    admin = Admin.query.get_or_404(admin_id)
    pending_reports = Report.query.filter_by(reviewed=False).order_by(Report.timestamp.desc()).all()
    reviewed_reports = Report.query.filter_by(reviewed=True).order_by(Report.timestamp.desc()).all()

    return render_template('view_reports.html', admin=admin, pending_reports=pending_reports, reviewed_reports=reviewed_reports, Comment=Comment, Recipe=Recipe)

@app.route('/admin/<int:admin_id>/approve_report/<int:report_id>', methods=['POST'])
def approve_report(admin_id, report_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("admin_login"))

    report = Report.query.get_or_404(report_id)
    report.reviewed = True
    report.approved = True
    report.notified = True
    db.session.commit()

    # Fetch related recipe or comment and user details
    if report.comment_id:
        comment = Comment.query.get(report.comment_id)
        related_text = f"Comment: {comment.comment[:50]}..." if comment else "Comment: [Deleted]"
        submitted_by = f"Submitted by: {comment.submitted_by}" if comment else "Submitted by: [Unknown]"
    else:
        recipe = Recipe.query.get(report.recipe_id)
        related_text = f"Recipe: {recipe.recipe_name}" if recipe else "Recipe: [Deleted]"
        submitted_by = f"Submitted by: {recipe.submitted_by}" if recipe else "Submitted by: [Unknown]"

    # Create a notification for the user who submitted the report
    report_timestamp = report.timestamp.strftime('%d-%m-%Y %H:%M:%S')
    notification_message = f"Your report on {related_text} ({submitted_by}) at {report_timestamp} has been reviewed and approved by the admin."
    notification = Notification(user_id=report.user_id, message=notification_message)
    db.session.add(notification)
    db.session.commit()

    flash('Report has been approved and the user has been notified.', 'success')
    return redirect(url_for('view_reports', admin_id=admin_id))

@app.route('/admin/<int:admin_id>/reject_report/<int:report_id>', methods=['POST'])
def reject_report(admin_id, report_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("admin_login"))

    report = Report.query.get_or_404(report_id)
    report.reviewed = True
    report.approved = False
    report.notified = True  # Assuming you want to notify the user even if the report is rejected
    db.session.commit()

    # Fetch related recipe or comment and user details
    if report.comment_id:
        comment = Comment.query.get(report.comment_id)
        related_text = f"Comment: {comment.comment[:50]}..." if comment else "Comment: [Deleted]"
        submitted_by = f"Submitted by: {comment.submitted_by}" if comment else "Submitted by: [Unknown]"
    else:
        recipe = Recipe.query.get(report.recipe_id)
        related_text = f"Recipe: {recipe.recipe_name}" if recipe else "Recipe: [Deleted]"
        submitted_by = f"Submitted by: {recipe.submitted_by}" if recipe else "Submitted by: [Unknown]"

    # Create a notification for the user who submitted the report
    report_timestamp = report.timestamp.strftime('%d-%m-%Y %H:%M:%S')
    notification_message = f"Your report on {related_text} ({submitted_by}) at {report_timestamp} has been reviewed and rejected by the admin."
    notification = Notification(user_id=report.user_id, message=notification_message)
    db.session.add(notification)
    db.session.commit()

    flash('Report has been rejected and the user has been notified.', 'success')
    return redirect(url_for('view_reports', admin_id=admin_id))


############### Logout ##################
@app.route("/adminlogout")
def adminlogout():
    flash("Log out successfully!","success")
	
    session.pop("admin_id", None)
    return redirect(url_for("adminlogin"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)