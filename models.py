from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
db = SQLAlchemy()
from datetime import datetime

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
    serving_size = db.Column(db.Integer, nullable=False)
    submitted_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    approved = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('recipe_submissions', lazy=True))
    image_path = db.Column(db.String(255))  # Path to the image file
    submitted_by = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    comments = db.relationship('Comment', backref=db.backref('recipe'), lazy=True)
    favourite_recipe = db.relationship('FavouriteRecipe', uselist=False, backref='recipe')


    def __repr__(self):
        return f'<RecipeSubmission {self.recipe_name}>'
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    submitted_by = db.Column(db.String(100), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('recipe', lazy=True))

    def __repr__(self):
        return f"Comment('{self.comment}', '{self.rating}')"
    
class FavouriteRecipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)
    pinned_date = db.Column(db.Date, nullable=True)

    user = db.relationship('User', backref=db.backref('favourite_recipes', lazy=True))
    recipe = db.relationship('Recipe', backref=db.backref('favourited_by', lazy=True))
    recipe = db.relationship('Recipe', backref='favourite_recipe')
