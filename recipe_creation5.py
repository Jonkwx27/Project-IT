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
    # Assuming the user with ID 5 exists
    user = session.query(User).filter_by(id=5).first()
    
    if not user:
        print("User with ID 5 does not exist. Please create the user first.")
        return

    # List of recipes to add
    recipes_to_add = [
        {
            "recipe_name": "Non-Alcoholic Mojito",
            "description": "A refreshing non-alcoholic mojito.",
            "ingredients": "Mint Leaves, Lime, Sugar, Soda Water, Ice",
            "steps": "1. Muddle mint leaves and lime\n2. Add sugar and ice\n3. Top with soda water and stir",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/non-alcoholic-mojito.jpg",
            "categories": ["Beverages", "Non-Alcoholic", "Mojito"]
        },
        {
            "recipe_name": "Deepavali Murukku",
            "description": "Crispy and savory Indian snack for Deepavali.",
            "ingredients": "Rice Flour, Urad Dal Flour, Butter, Cumin Seeds, Salt",
            "steps": "1. Mix all ingredients\n2. Shape into spirals\n3. Fry until golden brown",
            "difficulty": 3,
            "time_required": 4,
            "serving_size": 6,
            "image_path": "uploads/deepavali-murukku.jpeg",
            "categories": ["Snack", "Indian", "Deepavali", "Fried"]
        },
        {
            "recipe_name": "Hanukkah Sufganiyot",
            "description": "Traditional jelly-filled doughnuts for Hanukkah.",
            "ingredients": "Flour, Yeast, Sugar, Milk, Jelly, Oil",
            "steps": "1. Prepare the dough\n2. Fry doughnuts\n3. Fill with jelly and sprinkle with sugar",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 8,
            "image_path": "uploads/hanukkah-sufganiyot.jpg",
            "categories": ["Dessert", "Jewish", "Hanukkah", "Doughnuts and Fritters"]
        },
        {
            "recipe_name": "Eid Baklava",
            "description": "Sweet and flaky baklava for Eid celebrations.",
            "ingredients": "Phyllo Dough, Nuts, Honey, Butter, Sugar",
            "steps": "1. Layer phyllo dough with nuts and butter\n2. Bake until golden\n3. Drizzle with honey",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 8,
            "image_path": "uploads/eid-baklava.jpeg",
            "categories": ["Dessert", "Middle Eastern", "Eid", "Luxury"]
        },
        {
            "recipe_name": "Turkey Stuffing",
            "description": "Traditional stuffing for a Thanksgiving turkey.",
            "ingredients": "Bread, Onion, Celery, Butter, Herbs",
            "steps": "1. Sauté onions and celery\n2. Mix with bread and herbs\n3. Bake until golden",
            "difficulty": 2,
            "time_required": 4,
            "serving_size": 6,
            "image_path": "uploads/turkey-stuffing.jpg",
            "categories": ["Side Dish", "American", "Turkey", "Thanksgiving"]
        },
        {
            "recipe_name": "Non-Halal Spaghetti Carbonara",
            "description": "Classic Italian pasta with pancetta.",
            "ingredients": "Spaghetti, Eggs, Parmesan Cheese, Pancetta, Black Pepper",
            "steps": "1. Cook spaghetti\n2. Fry pancetta\n3. Mix eggs and cheese, combine with pasta and pancetta",
            "difficulty": 3,
            "time_required": 2,
            "serving_size": 2,
            "image_path": "uploads/non-halal-carbonara.jpg",
            "categories": ["Main Course", "Italian", "Pasta", "Non-Halal"]
        },
        {
            "recipe_name": "Vegan Chocolate Cake",
            "description": "Rich and moist vegan chocolate cake.",
            "ingredients": "Flour, Cocoa Powder, Sugar, Baking Soda, Vinegar, Coconut Oil",
            "steps": "1. Mix dry ingredients\n2. Add wet ingredients and stir\n3. Bake at 350°F for 30 minutes",
            "difficulty": 3,
            "time_required": 4,
            "serving_size": 8,
            "image_path": "uploads/vegan-chocolate-cake.jpg",
            "categories": ["Dessert", "Vegan", "Cakes", "Non-Alcoholic"]
        },
        {
            "recipe_name": "Soy-Free Chicken Teriyaki",
            "description": "A delicious soy-free version of chicken teriyaki.",
            "ingredients": "Chicken, Coconut Aminos, Honey, Garlic, Ginger",
            "steps": "1. Cook chicken\n2. Mix coconut aminos, honey, garlic, and ginger\n3. Combine and simmer",
            "difficulty": 2,
            "time_required": 3,
            "serving_size": 4,
            "image_path": "uploads/soy-free-chicken-teriyaki.jpg",
            "categories": ["Main Course", "Asian", "Soy-Free", "High-Protein"]
        },
        {
            "recipe_name": "Pakistani Nihari",
            "description": "Spicy slow-cooked beef stew.",
            "ingredients": "Beef Shank, Ghee, Flour, Ginger, Garlic, Spices",
            "steps": "1. Cook beef with spices\n2. Thicken with flour and ghee\n3. Simmer until tender",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 6,
            "image_path": "uploads/pakistani-nihari.jpeg",
            "categories": ["Main Course", "Pakistani", "Slow-Cooked", "Stew"]
        },
        {
            "recipe_name": "Christmas Gingerbread Cookies",
            "description": "Festive gingerbread cookies for Christmas.",
            "ingredients": "Flour, Ginger, Cinnamon, Molasses, Butter, Sugar",
            "steps": "1. Mix dry ingredients\n2. Add wet ingredients and stir\n3. Roll out dough, cut shapes, and bake",
            "difficulty": 3,
            "time_required": 5,
            "serving_size": 10,
            "image_path": "uploads/christmas-gingerbread-cookies.jpg",
            "categories": ["Dessert", "Christmas", "Cookies", "Non-Alcoholic"]
        },
        {
            "recipe_name": "Malaysian Nasi Lemak",
            "description": "Traditional Malaysian coconut rice served with various accompaniments.",
            "ingredients": "Rice, Coconut Milk, Anchovies, Peanuts, Cucumber, Egg, Sambal",
            "steps": "1. Cook rice with coconut milk\n2. Fry anchovies and peanuts\n3. Serve with cucumber, egg, and sambal",
            "difficulty": 3,
            "time_required": 4,
            "serving_size": 4,
            "image_path": "uploads/nasi-lemak.jpeg",
            "categories": ["Main Course", "Malaysian", "Rice"]
        },
        {
            "recipe_name": "Spanish Paella",
            "description": "Classic Spanish rice dish with seafood.",
            "ingredients": "Rice, Saffron, Shrimp, Mussels, Chicken, Bell Peppers, Peas",
            "steps": "1. Sauté chicken and peppers\n2. Add rice and saffron\n3. Add seafood and peas, simmer until cooked",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 6,
            "image_path": "uploads/spanish-paella.jpg",
            "categories": ["Main Course", "Spanish", "Seafood"]
        },
        {
            "recipe_name": "Japanese Ramen",
            "description": "Authentic Japanese ramen with pork and soft-boiled eggs.",
            "ingredients": "Ramen Noodles, Pork Belly, Soy Sauce, Mirin, Eggs, Green Onions, Nori",
            "steps": "1. Cook pork belly in soy sauce and mirin\n2. Boil ramen noodles\n3. Serve with soft-boiled eggs, green onions, and nori",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 4,
            "image_path": "uploads/japanese-ramen.jpg",
            "categories": ["Main Course", "Japanese", "Noodles", "Non-Halal"]
        },
        {
            "recipe_name": "Thai Green Curry",
            "description": "Spicy and fragrant green curry from Thailand.",
            "ingredients": "Chicken, Green Curry Paste, Coconut Milk, Bamboo Shoots, Basil, Eggplant",
            "steps": "1. Cook curry paste in coconut milk\n2. Add chicken and vegetables\n3. Simmer until cooked",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 4,
            "image_path": "uploads/thai-green-curry.jpg",
            "categories": ["Main Course", "Thai", "High-Protein", "Non-Halal"]
        },
        {
            "recipe_name": "American Pancakes",
            "description": "Fluffy American-style pancakes perfect for breakfast.",
            "ingredients": "Flour, Baking Powder, Milk, Eggs, Sugar, Butter",
            "steps": "1. Mix dry ingredients\n2. Add wet ingredients and stir\n3. Cook on a griddle until golden brown",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 4,
            "image_path": "uploads/american-pancakes.jpg",
            "categories": ["Breakfast", "American", "Pancakes and Waffles", "Non-Alcoholic"]
        },
        {
            "recipe_name": "Middle Eastern Falafel",
            "description": "Crispy fried falafel served with tahini sauce.",
            "ingredients": "Chickpeas, Onion, Garlic, Parsley, Cumin, Coriander",
            "steps": "1. Blend ingredients into a paste\n2. Shape into balls and fry\n3. Serve with tahini sauce",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 4,
            "image_path": "uploads/falafel.jpg",
            "categories": ["Appetizer", "Middle Eastern", "Vegan", "High-Protein"]
        },
        {
            "recipe_name": "French Macarons",
            "description": "Delicate and colorful French macarons.",
            "ingredients": "Almond Flour, Egg Whites, Sugar, Food Coloring, Buttercream",
            "steps": "1. Whip egg whites and sugar\n2. Fold in almond flour and food coloring\n3. Pipe and bake, fill with buttercream",
            "difficulty": 5,
            "time_required": 5,
            "serving_size": 8,
            "image_path": "uploads/french-macarons.jpg",
            "categories": ["Dessert", "French", "Macarons and Madeleines", "Luxury"]
        },
        {
            "recipe_name": "Italian Tiramisu",
            "description": "Classic Italian dessert with layers of coffee-soaked ladyfingers and mascarpone.",
            "ingredients": "Ladyfingers, Coffee, Mascarpone, Eggs, Sugar, Cocoa Powder",
            "steps": "1. Soak ladyfingers in coffee\n2. Layer with mascarpone mixture\n3. Dust with cocoa powder",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 6,
            "image_path": "uploads/tiramisu.jpg",
            "categories": ["Dessert", "Italian", "Tiramisu and Parfaits", "Luxury"]
        },
        {
            "recipe_name": "Pakistani Biryani",
            "description": "Flavorful and spicy Pakistani biryani with chicken.",
            "ingredients": "Basmati Rice, Chicken, Yogurt, Onions, Tomatoes, Spices",
            "steps": "1. Marinate chicken in yogurt and spices\n2. Cook with onions and tomatoes\n3. Layer with rice and simmer",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 6,
            "image_path": "uploads/pakistani-biryani.jpeg",
            "categories": ["Main Course", "Pakistani", "Rice"]
        },
        {
            "recipe_name": "Mexican Tacos",
            "description": "Traditional Mexican tacos with beef and fresh toppings.",
            "ingredients": "Ground Beef, Tortillas, Lettuce, Tomatoes, Cheese, Sour Cream",
            "steps": "1. Cook ground beef with spices\n2. Assemble tacos with beef and toppings\n3. Serve with sour cream",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 4,
            "image_path": "uploads/mexican-tacos.jpg",
            "categories": ["Main Course", "Mexican", "Tacos"]
        },
        {
            "recipe_name": "French Baguette",
            "description": "Classic French baguette with a crispy crust.",
            "ingredients": "Flour, Water, Yeast, Salt",
            "steps": "1. Mix ingredients and knead dough\n2. Let rise and shape into baguettes\n3. Bake at 450°F until golden",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 6,
            "image_path": "uploads/french-baguette.jpg",
            "categories": ["Bread", "French", "Non-Alcoholic"]
        },
        {
            "recipe_name": "Deepavali Gulab Jamun",
            "description": "Sweet and syrupy Indian dessert for Deepavali.",
            "ingredients": "Milk Powder, Flour, Baking Powder, Sugar, Cardamom, Rose Water",
            "steps": "1. Mix dry ingredients\n2. Form balls and fry\n3. Soak in sugar syrup with cardamom and rose water",
            "difficulty": 3,
            "time_required": 5,
            "serving_size": 8,
            "image_path": "uploads/deepavali-gulab-jamun.jpg",
            "categories": ["Dessert", "Indian", "Deepavali", "Non-Halal"]
        },
        {
            "recipe_name": "Turkish Delight",
            "description": "Sweet and chewy Turkish delight with powdered sugar.",
            "ingredients": "Sugar, Cornstarch, Water, Lemon Juice, Food Coloring, Powdered Sugar",
            "steps": "1. Boil sugar and water\n2. Add cornstarch and lemon juice\n3. Pour into a mold and cool, then cut and coat with powdered sugar",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 10,
            "image_path": "uploads/turkish-delight.jpg",
            "categories": ["Dessert", "Turkey", "Luxury"]
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