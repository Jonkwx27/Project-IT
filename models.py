from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    steps = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.String(255), nullable=False)
    taste = db.Column(db.Integer, nullable=False) 
    time_required = db.Column(db.Integer, nullable=False) 
    difficulty = db.Column(db.Integer, nullable=False) 
    comments = db.relationship('Comment', backref='recipe', lazy=True)

    def __repr__(self):
        return f"Recipe('{self.title}')"
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255))
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)

    def __repr__(self):
        return f"Comment('{self.name}', '{self.comment}', '{self.rating}')"
    