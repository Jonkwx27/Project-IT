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
    # Assuming the user with ID 6 exists
    user = session.query(User).filter_by(id=6).first()
    
    if not user:
        print("User with ID 6 does not exist. Please create the user first.")
        return

    # List of recipes to add
    recipes_to_add = [
        {
            "recipe_name": "Classic Margarita",
            "description": "A refreshing cocktail with tequila, lime, and triple sec.",
            "ingredients": "Tequila, Lime Juice, Triple Sec, Salt, Ice",
            "steps": "1. Rim glass with salt\n2. Shake tequila, lime juice, and triple sec with ice\n3. Pour into glass and serve",
            "difficulty": 2,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/classic-margarita.jpeg",
            "categories": ["Cocktails"]
        },
        {
            "recipe_name": "Espresso",
            "description": "A strong and rich espresso shot.",
            "ingredients": "Coffee Beans, Water",
            "steps": "1. Grind coffee beans\n2. Brew with an espresso machine\n3. Serve immediately",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/espresso.jpg",
            "categories": ["Coffee"]
        },
        {
            "recipe_name": "Iced Caramel Macchiato",
            "description": "A sweet and creamy iced coffee drink.",
            "ingredients": "Espresso, Milk, Caramel Syrup, Ice",
            "steps": "1. Fill a glass with ice\n2. Add caramel syrup and milk\n3. Pour espresso over the top",
            "difficulty": 2,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/iced-caramel-macchiato.jpg",
            "categories": ["Iced Coffee"]
        },
        {
            "recipe_name": "Peach Iced Tea",
            "description": "A refreshing iced tea with a hint of peach.",
            "ingredients": "Black Tea, Peach Syrup, Ice, Peach Slices",
            "steps": "1. Brew black tea and let cool\n2. Add peach syrup and stir\n3. Serve over ice with peach slices",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 2,
            "image_path": "uploads/peach-iced-tea.jpg",
            "categories": ["Iced Tea"]
        },
        {
            "recipe_name": "Fresh Orange Juice",
            "description": "Simple and fresh homemade orange juice.",
            "ingredients": "Oranges",
            "steps": "1. Squeeze oranges to extract juice\n2. Strain if desired\n3. Serve immediately",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 2,
            "image_path": "uploads/fresh-orange-juice.jpg",
            "categories": ["Juices"]
        },
        {
            "recipe_name": "Mango Lassi",
            "description": "A sweet and creamy mango yogurt drink.",
            "ingredients": "Mango, Yogurt, Sugar, Water, Cardamom",
            "steps": "1. Blend mango, yogurt, sugar, and water\n2. Add cardamom and blend again\n3. Serve chilled",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 2,
            "image_path": "uploads/mango-lassi.jpg",
            "categories": ["Lassi"]
        },
        {
            "recipe_name": "Chocolate Milkshake",
            "description": "A rich and creamy chocolate milkshake.",
            "ingredients": "Ice Cream, Milk, Chocolate Syrup",
            "steps": "1. Blend ice cream, milk, and chocolate syrup\n2. Serve in a tall glass with whipped cream",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/chocolate-milkshake.jpg",
            "categories": ["Milkshakes"]
        },
        {
            "recipe_name": "Virgin Mojito",
            "description": "A refreshing and minty mocktail.",
            "ingredients": "Mint Leaves, Lime, Sugar, Soda Water, Ice",
            "steps": "1. Muddle mint leaves and lime\n2. Add sugar and ice\n3. Top with soda water and stir",
            "difficulty": 1,
            "time_required": 5,
            "serving_size": 1,
            "image_path": "uploads/virgin-mojito.jpeg",
            "categories": ["Mocktails"]
        },
        {
            "recipe_name": "Homemade Lemonade",
            "description": "A simple and refreshing homemade lemonade.",
            "ingredients": "Lemons, Sugar, Water, Ice",
            "steps": "1. Squeeze lemons to extract juice\n2. Mix lemon juice with sugar and water\n3. Serve over ice",
            "difficulty": 1,
            "time_required": 10,
            "serving_size": 4,
            "image_path": "uploads/homemade-lemonade.jpeg",
            "categories": ["Other Beverages"]
        },
        {
            "recipe_name": "Strawberry Banana Smoothie",
            "description": "A healthy and delicious strawberry banana smoothie.",
            "ingredients": "Strawberries, Banana, Yogurt, Milk, Honey",
            "steps": "1. Blend strawberries, banana, yogurt, milk, and honey\n2. Serve immediately",
            "difficulty": 1,
            "time_required": 5,
            "serving_size": 2,
            "image_path": "uploads/strawberry-banana-smoothie.jpg",
            "categories": ["Smoothies"]
        },
        {
            "recipe_name": "Green Tea",
            "description": "Simple and healthy green tea.",
            "ingredients": "Green Tea Leaves, Water",
            "steps": "1. Boil water and let cool slightly\n2. Steep green tea leaves for 2-3 minutes\n3. Serve hot",
            "difficulty": 1,
            "time_required": 5,
            "serving_size": 1,
            "image_path": "uploads/green-tea.jpg",
            "categories": ["Tea"]
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