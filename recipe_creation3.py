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
    # Assuming the user with ID 3 exists
    user = session.query(User).filter_by(id=3).first()
    
    if not user:
        print("User with ID 3 does not exist. Please create the user first.")
        return

    # List of recipes to add
    recipes_to_add = [
        {
            "recipe_name": "Vegan Pancakes",
            "description": "Fluffy vegan pancakes perfect for breakfast.",
            "ingredients": "Flour, Almond Milk, Baking Powder, Maple Syrup, Salt",
            "steps": "1. Mix dry ingredients\n2. Add almond milk and stir\n3. Cook on a hot griddle until golden",
            "difficulty": 2,
            "time_required": 1,
            "serving_size": 2,
            "image_path": "uploads/vegan-pancakes.jpg",
            "categories": ["Breakfast", "Vegan", "Pancakes and Waffles"]
        },
        {
            "recipe_name": "Gluten-Free Brownies",
            "description": "Rich and chewy gluten-free brownies.",
            "ingredients": "Gluten-Free Flour, Cocoa Powder, Eggs, Butter, Sugar",
            "steps": "1. Mix dry ingredients\n2. Add wet ingredients and stir\n3. Bake at 350°F for 25 minutes",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 4,
            "image_path": "uploads/gluten-free-brownies.jpg",
            "categories": ["Dessert", "Gluten-Free", "Brownies and Bars"]
        },
        {
            "recipe_name": "Chicken Biryani",
            "description": "Aromatic and flavorful chicken biryani.",
            "ingredients": "Chicken, Basmati Rice, Spices, Yogurt, Onions",
            "steps": "1. Marinate chicken\n2. Cook rice and chicken separately\n3. Layer and cook on low heat",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 4,
            "image_path": "uploads/chicken-biryani.jpg",
            "categories": ["Main Course", "Indian", "Rice", "High-Protein"]
        },
        {
            "recipe_name": "Grilled Salmon",
            "description": "Simple and delicious grilled salmon.",
            "ingredients": "Salmon Fillets, Lemon, Olive Oil, Salt, Pepper",
            "steps": "1. Season salmon\n2. Grill on medium heat until cooked through\n3. Serve with lemon wedges",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 2,
            "image_path": "uploads/grilled-salmon.jpg",
            "categories": ["Lunch", "Grilled", "Seafood", "Low-Carb"]
        },
        {
            "recipe_name": "Vegetable Stir-Fry",
            "description": "Quick and healthy vegetable stir-fry.",
            "ingredients": "Mixed Vegetables, Soy Sauce, Garlic, Ginger, Olive Oil",
            "steps": "1. Heat oil in a wok\n2. Add garlic and ginger\n3. Stir-fry vegetables until tender",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 2,
            "image_path": "uploads/vegetable_stir-fry.jpg",
            "categories": ["Dinner", "Vegetarian", "Side Dish", "Soy-Free"]
        },
        {
            "recipe_name": "Spaghetti Carbonara",
            "description": "Classic Italian pasta dish with creamy sauce.",
            "ingredients": "Spaghetti, Eggs, Parmesan Cheese, Pancetta, Black Pepper",
            "steps": "1. Cook spaghetti\n2. Fry pancetta\n3. Mix eggs and cheese, combine with pasta and pancetta",
            "difficulty": 3,
            "time_required": 2,
            "serving_size": 2,
            "image_path": "uploads/spaghetti_carbonara.jpg",
            "categories": ["Main Course", "Italian", "Pasta", "Luxury"]
        },
        {
            "recipe_name": "Keto Avocado Salad",
            "description": "Refreshing salad perfect for a keto diet.",
            "ingredients": "Avocado, Cherry Tomatoes, Cucumber, Olive Oil, Lemon Juice",
            "steps": "1. Chop vegetables\n2. Toss with olive oil and lemon juice\n3. Season to taste",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/keto-avocado-salad.jpg",
            "categories": ["Lunch", "Keto", "Salads"]
        },
        {
            "recipe_name": "BBQ Chicken Wings",
            "description": "Juicy and flavorful BBQ chicken wings.",
            "ingredients": "Chicken Wings, BBQ Sauce, Garlic Powder, Salt, Pepper",
            "steps": "1. Season wings\n2. Grill and baste with BBQ sauce\n3. Serve hot",
            "difficulty": 2,
            "time_required": 3,
            "serving_size": 4,
            "image_path": "uploads/bbq-chicken-wings.jpg",
            "categories": ["Appetizer", "American", "Grilled", "High-Protein"]
        },
        {
            "recipe_name": "Tom Yum Soup",
            "description": "Spicy and sour Thai soup.",
            "ingredients": "Shrimp, Lemongrass, Lime Leaves, Mushrooms, Chili Peppers",
            "steps": "1. Boil water with lemongrass and lime leaves\n2. Add mushrooms and shrimp\n3. Season with fish sauce and lime juice",
            "difficulty": 3,
            "time_required": 2,
            "serving_size": 2,
            "image_path": "uploads/tom-yum-soup.jpg",
            "categories": ["Main Course", "Thai", "Soups", "Dairy-Free"]
        },
        {
            "recipe_name": "Deepavali Ladoo",
            "description": "Traditional Indian sweet for Deepavali.",
            "ingredients": "Chickpea Flour, Ghee, Sugar, Cardamom, Nuts",
            "steps": "1. Roast flour in ghee\n2. Add sugar and cardamom\n3. Shape into balls and garnish with nuts",
            "difficulty": 4,
            "time_required": 4,
            "serving_size": 6,
            "image_path": "uploads/deepavali-ladoo.jpg",
            "categories": ["Dessert", "Indian", "Deepavali", "Gluten-Free"]
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