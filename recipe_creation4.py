import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import db, User, Recipe, Category

UPLOAD_FOLDER = 'uploads'  # Directory to store uploaded images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder="templates")
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db.init_app(app)

# Setup the database engine and session
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
session = Session()

def add_recipes():
    # Assuming the user with ID 4 exists
    user = session.query(User).filter_by(id=4).first()
    
    if not user:
        print("User with ID 4 does not exist. Please create the user first.")
        return

    # List of recipes to add
    recipes_to_add = [
        {
            "recipe_name": "Keto Chicken Wrap",
            "description": "Low-carb chicken wrap perfect for a keto diet.",
            "ingredients": "Chicken Breast, Lettuce, Cheese, Avocado, Mayo",
            "steps": "1. Cook the chicken\n2. Assemble the wrap with lettuce, cheese, avocado, and mayo\n3. Serve",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 1,
            "image_path": "uploads/keto-chicken-wrap.jpeg",
            "categories": ["Lunch", "Keto", "Wraps", "Low-Carb"]
        },
        {
            "recipe_name": "Soy-Free Tofu Stir-Fry",
            "description": "Delicious tofu stir-fry without soy sauce.",
            "ingredients": "Tofu, Bell Peppers, Broccoli, Garlic, Olive Oil",
            "steps": "1. Heat oil in a pan\n2. Add garlic and tofu, stir-fry\n3. Add vegetables and cook until tender",
            "difficulty": 2,
            "time_required": 1,
            "serving_size": 2,
            "image_path": "uploads/soy-free-tofu-stir-fry.jpg",
            "categories": ["Dinner", "Vegetarian", "Soy-Free", "Low-Sodium"]
        },
        {
            "recipe_name": "Keto Beef Stew",
            "description": "Hearty beef stew with low-carb vegetables.",
            "ingredients": "Beef, Celery, Carrots, Beef Broth, Olive Oil",
            "steps": "1. Brown the beef\n2. Add vegetables and broth\n3. Simmer until tender",
            "difficulty": 3,
            "time_required": 6,
            "serving_size": 4,
            "image_path": "uploads/keto-beef-stew.jpg",
            "categories": ["Main Course", "Stew", "Low-Carb", "High-Protein"]
        },
        {
            "recipe_name": "Sugar-Free Banana Bread",
            "description": "Healthy banana bread with no added sugar.",
            "ingredients": "Bananas, Almond Flour, Eggs, Baking Soda, Vanilla Extract",
            "steps": "1. Mash bananas\n2. Mix all ingredients\n3. Bake at 350°F for 45 minutes",
            "difficulty": 2,
            "time_required": 6,
            "serving_size": 6,
            "image_path": "uploads/sugar-free-banana-bread.jpeg",
            "categories": ["Breakfast", "Sugar-Free", "Low-Fat", "Baked"]
        },
        {
            "recipe_name": "Vegan Buddha Bowl",
            "description": "Colorful and nutritious vegan Buddha bowl.",
            "ingredients": "Quinoa, Chickpeas, Avocado, Spinach, Tahini",
            "steps": "1. Cook quinoa\n2. Arrange all ingredients in a bowl\n3. Drizzle with tahini",
            "difficulty": 1,
            "time_required": 2,
            "serving_size": 1,
            "image_path": "uploads/vegan-buddha-bowl.jpg",
            "categories": ["Lunch", "Vegan", "High-Protein", "Salads"]
        },
        {
            "recipe_name": "French Onion Soup",
            "description": "Classic French onion soup with a rich flavor.",
            "ingredients": "Onions, Beef Broth, Butter, Baguette, Gruyere Cheese",
            "steps": "1. Caramelize onions in butter\n2. Add broth and simmer\n3. Top with baguette and cheese, then broil",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 2,
            "image_path": "uploads/french-onion-soup.jpg",
            "categories": ["Main Course", "French", "Soups", "Luxury"]
        },
        {
            "recipe_name": "Pressure-Cooked Pulled Pork",
            "description": "Tender pulled pork made in a pressure cooker.",
            "ingredients": "Pork Shoulder, BBQ Sauce, Onion, Garlic, Spices",
            "steps": "1. Season pork\n2. Pressure cook with onions and garlic\n3. Shred and mix with BBQ sauce",
            "difficulty": 3,
            "time_required": 5,
            "serving_size": 4,
            "image_path": "uploads/pressure-cooked-pulled-pork.jpg",
            "categories": ["Main Course", "American", "Pressure-Cooked", "Low-Sodium", "Non-Halal"]
        },
        {
            "recipe_name": "Gluten-Free Pizza",
            "description": "Delicious pizza with a gluten-free crust.",
            "ingredients": "Gluten-Free Flour, Yeast, Olive Oil, Tomato Sauce, Cheese",
            "steps": "1. Prepare the dough\n2. Top with sauce and cheese\n3. Bake at 450°F for 15 minutes",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 4,
            "image_path": "uploads/gluten-free-pizza.jpg",
            "categories": ["Dinner", "Gluten-Free", "Pizzas", "Non-Alcoholic"]
        },
        {
            "recipe_name": "Hanukkah Latkes",
            "description": "Crispy potato pancakes for Hanukkah.",
            "ingredients": "Potatoes, Onions, Eggs, Matzo Meal, Oil",
            "steps": "1. Grate potatoes and onions\n2. Mix with eggs and matzo meal\n3. Fry in oil until golden brown",
            "difficulty": 2,
            "time_required": 3,
            "serving_size": 4,
            "image_path": "uploads/hanukkah-latkes.jpg",
            "categories": ["Appetizer", "Fried", "Hanukkah"]
        },
        {
            "recipe_name": "Chinese New Year Dumplings",
            "description": "Traditional dumplings for Chinese New Year.",
            "ingredients": "Ground Pork, Cabbage, Ginger, Dumpling Wrappers, Soy Sauce",
            "steps": "1. Mix filling ingredients\n2. Wrap in dumpling wrappers\n3. Steam or boil until cooked",
            "difficulty": 4,
            "time_required": 4,
            "serving_size": 4,
            "image_path": "uploads/chinese-new-year-dumplings.jpg",
            "categories": ["Appetizer", "Chinese", "Steamed", "Chinese New Year"]
        }
    ]

        # Loop through each recipe and add it to the database
    for recipe_data in recipes_to_add:
        new_recipe = Recipe(
            recipe_name=recipe_data["recipe_name"],
            description=recipe_data["description"],
            ingredients=recipe_data["ingredients"],
            steps=recipe_data["steps"],
            difficulty=recipe_data["difficulty"],
            time_required=recipe_data["time_required"],
            serving_size=recipe_data["serving_size"],
            approved=True,
            user_id=user.id,
            submitted_by=f"{user.username} (ID: {user.id})",
            image_path=recipe_data["image_path"]
        )

        # Add categories to the recipe
        for category_name in recipe_data["categories"]:
            category = session.query(Category).filter_by(name=category_name).first()
            if category:
                new_recipe.categories.append(category)

        # Add the new recipe to the session
        session.add(new_recipe)

    # Commit the session to save all new recipes to the database
    session.commit()
    print(f'{len(recipes_to_add)} recipes added.')

# Example of how to use this function in the Flask app context
with app.app_context():
    add_recipes()

# Close the session
session.close()