from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pytz import timezone

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone('Asia/Kuala_Lumpur')))
    recipes = db.relationship('Recipe', backref='author', cascade="all, delete-orphan", lazy=True)
    comments = db.relationship('Comment', backref='commenter', cascade="all, delete-orphan", lazy=True)
    favourite_recipes = db.relationship('FavouriteRecipe', backref='user_fav', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f'<User {self.name}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email_admin = db.Column(db.String(80), unique=True, nullable=False)
    password_admin = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Admin {self.email_admin}>'
    
    def set_password_admin(self, password_admin):
        self.password_admin = generate_password_hash(password_admin)

    def check_password_admin(self, password_admin):
        return check_password_hash(self.password_admin, password_admin)

recipe_category_association = db.Table('recipe_category_association',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.id'), primary_key=True)
)

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    time_required = db.Column(db.Integer, nullable=False)
    serving_size = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone('Asia/Kuala_Lumpur')))
    approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_recipe_user'), nullable=False)
    image_path = db.Column(db.String(255))  # Path to the image file
    submitted_by = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id', name='fk_recipe_admin'))
    comments = db.relationship('Comment', backref='recipe', cascade="all, delete-orphan", lazy=True)
    categories = db.relationship('Category', secondary=recipe_category_association, backref=db.backref('recipes', lazy='dynamic'))

    def __repr__(self):
        return f'<Recipe {self.recipe_name}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    submitted_by = db.Column(db.String(100), nullable=False)
    commented_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(timezone('Asia/Kuala_Lumpur')))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_comment_recipe'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_comment_user'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.comment}', '{self.rating}')"

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    group_id = db.Column(db.Integer, db.ForeignKey('category_group.id', name='fk_category_group'), nullable=True)

    def __repr__(self):
        return f'<Category {self.name}>'

class CategoryGroup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    categories = db.relationship('Category', backref='group', lazy=True)

    def __repr__(self):
        return f'<CategoryGroup {self.name}>'

class FavouriteRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', name='fk_favourite_recipe_user'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id', name='fk_favourite_recipe'), nullable=False)
    cook_on = db.Column(db.Date)

    def __repr__(self):
        return f"FavouriteRecipe('{self.user_id}', '{self.recipe_id}')"
