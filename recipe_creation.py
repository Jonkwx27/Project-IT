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
    # Assuming the user with ID 1 exists
    user = session.query(User).filter_by(id=1).first()
    
    if not user:
        print("User with ID 1 does not exist. Please create the user first.")
        return

    # List of recipes to add
    recipes_to_add = [
        {
            "recipe_name": "Grilled Cheese",
            "description": "A tasty grilled cheese sandwich.",
            "ingredients": "Bread, Cheese, Butter",
            "steps": "1. Butter the bread\n2. Add cheese\n3. Grill until golden brown",
            "difficulty": 2,
            "time_required": 3,
            "serving_size": 1,
            "image_path": "uploads/grilled-cheese.jpg",
            "categories": ["Lunch"]
        },
        {
            "recipe_name": "Tomato Soup",
            "description": "Delicious and warm tomato soup.",
            "ingredients": "Tomatoes, Onion, Garlic, Salt, Pepper",
            "steps": "1. Cook the onions and garlic\n2. Add tomatoes and cook\n3. Blend until smooth",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 2,
            "image_path": "uploads/tomato-soup.jpg",
            "categories": ["Dinner"]
        },
        {
            "recipe_name": "Grilled Chicken Salad",
            "description": "A fresh and healthy grilled chicken salad is perfect for a light lunch or dinner. This salad features tender grilled chicken breast on a bed of mixed greens, with a variety of colorful vegetables and a simple vinaigrette.",
            "ingredients": "2 boneless, skinless chicken breasts, Salt and pepper, to taste, 1 tablespoon olive oil, 6 cups mixed salad greens, 1 cup cherry tomatoes, halved, 1 cucumber, sliced, 1/4 red onion, thinly sliced, 1/4 cup crumbled feta cheese (optional), 1/4 cup balsamic vinaigrette (store-bought or homemade)",
            "steps": "1. Season the chicken breasts with salt and pepper.\n2. Heat the olive oil in a grill pan or skillet over medium-high heat.\n3. Grill the chicken for about 6-7 minutes per side, or until fully cooked (internal temperature of 165°F or 74°C).\n4. Remove from the grill and let rest for a few minutes, then slice into strips.\n5. In a large bowl, combine the mixed salad greens, cherry tomatoes, cucumber, and red onion.\n6. Top the salad with the grilled chicken strips.\n7. Sprinkle with crumbled feta cheese, if using.\n8. Drizzle with balsamic vinaigrette and toss gently to combine.\n9. Serve immediately and enjoy!",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 4,
            "image_path": "uploads/grilled-chicken-salad.jpg",
            "categories": ["Dinner"]
        },
        {
            "recipe_name": "Avocado Toast",
            "description": "Avocado toast is a quick, nutritious, and delicious breakfast or snack option. It's made with ripe avocados spread over toasted bread, often topped with a variety of additional ingredients for extra flavor and nutrition.",
            "ingredients": "2 slices of whole-grain bread, 1 ripe avocado, Salt and pepper, to taste, Optional toppings: cherry tomatoes, red pepper flakes, a squeeze of lemon juice, olive oil, microgreens, poached egg",
            "steps": "1. Toast the bread slices until golden and crisp.\n2. Cut the avocado in half, remove the pit, and scoop out the flesh into a bowl.\n3. Mash the avocado with a fork until it reaches your desired consistency (smooth or slightly chunky).\n4. Season with salt and pepper to taste.\n5. Spread the mashed avocado evenly over the toasted bread slices.\n6. Add any optional toppings such as cherry tomatoes, red pepper flakes, a squeeze of lemon juice, a drizzle of olive oil, microgreens, or a poached egg.\n7. Serve immediately and enjoy!",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 1,
            "image_path": "uploads/avocado-toast.jpg",
            "categories": ["Breakfast","Brunch"]
        },
        {
            "recipe_name": "Beef Wellington",
            "description": "Beef Wellington is a classic British dish that consists of a tender beef fillet coated with a layer of pâté (often pâté de foie gras) and duxelles (a finely chopped mixture of mushrooms, shallots, and herbs), then wrapped in puff pastry and baked to a golden perfection. This elegant dish is perfect for special occasions and is sure to impress your guests.",
            "ingredients": "1 center-cut beef tenderloin (about 2 pounds), Salt and freshly ground black pepper, to taste, 2 tablespoons olive oil, 2 tablespoons Dijon mustard, 1 pound mushrooms (button or cremini), finely chopped, 2 shallots, finely chopped,  2 cloves garlic, minced, 2 tablespoons unsalted butter, 1 tablespoon fresh thyme leaves, chopped, 4 ounces pâté de foie gras or mushroom pâté (optional), 6 to 8 thin slices of prosciutto, 1 package puff pastry (thawed if frozen), 1 egg, beaten (for egg wash)",
            "steps": "1. Preheat the oven to 400°F (200°C).\n2. Season the beef tenderloin generously with salt and pepper.\n3. Heat the olive oil in a large skillet over medium-high heat.\n4. Sear the beef on all sides until browned, about 2-3 minutes per side. Remove from heat and let cool.\n5. Brush the beef with Dijon mustard and let it rest.\n6. In a food processor, pulse the mushrooms until finely chopped.\n7. In the same skillet used for searing the beef, melt the butter over medium heat.\n8. Add the shallots and garlic, sauté until translucent, about 2 minutes.\n9. Add the chopped mushrooms and cook until all the moisture has evaporated, about 10 minutes.\n10. Stir in the thyme leaves, season with salt and pepper, and set aside to cool.\n11. Lay out a large piece of plastic wrap on a work surface.\n12. Arrange the prosciutto slices on the plastic wrap, slightly overlapping, to form a rectangle large enough to wrap around the beef.\n13. Spread the duxelles evenly over the prosciutto.\n14. Place the beef tenderloin on top of the duxelles.\n15. If using, spread the pâté over the beef.\n16. Using the plastic wrap, roll the prosciutto and duxelles around the beef, wrapping tightly. Twist the ends of the plastic wrap to secure and refrigerate for 15-20 minutes.\n17. Preheat the oven to 425°F (220°C).\n18. Roll out the puff pastry on a lightly floured surface to a rectangle large enough to envelop the beef.\n19. Unwrap the beef from the plastic wrap and place it in the center of the puff pastry.\n20. Fold the pastry over the beef, trimming any excess and sealing the edges well.\n21. Place the wrapped beef seam-side down on a baking sheet.\n22. Brush the pastry with the beaten egg to create an egg wash.\n23. Score the top of the pastry with a sharp knife (optional for decoration).\n24. Bake in the preheated oven until the pastry is golden brown and the beef reaches your desired doneness (about 25-30 minutes for medium-rare).\n25. Use a meat thermometer to check the internal temperature: 125°F (51°C) for medium-rare, 135°F (57°C) for medium.\n26. Let the Beef Wellington rest for 10 minutes before slicing.\n27. Slice and serve immediately, preferably with a side of roasted vegetables or a green salad.",
            "difficulty": 5,
            "time_required": 5,
            "serving_size": 10,
            "image_path": "uploads/beef-wellington.jpg",
            "categories": ["Dinner","Luxury"]
        },
        {
            "recipe_name": "Spaghetti Aglio e Olio",
            "description": "Spaghetti Aglio e Olio is a classic Italian pasta dish that's incredibly simple yet full of flavor. Made with garlic, olive oil, and red pepper flakes, it’s perfect for a quick and satisfying dinner.",
            "ingredients": "12 ounces spaghetti, 1/2 cup extra-virgin olive oil, 6 cloves garlic, thinly sliced, 1/4 teaspoon red pepper flakes (adjust to taste), Salt and freshly ground black pepper, to taste, 1/4 cup chopped fresh parsley, Freshly grated Parmesan cheese (optional)",
            "steps": "1. Bring a large pot of salted water to a boil.\n2. Cook the spaghetti according to the package instructions until al dente./n3. Reserve 1/2 cup of pasta cooking water, then drain the spaghetti.\n4. While the spaghetti is cooking, heat the olive oil in a large skillet over medium heat.\n5. Add the sliced garlic and cook until it begins to turn golden (about 1-2 minutes). Be careful not to burn it.\n6. Add the red pepper flakes and cook for another 30 seconds.\n7. Add the drained spaghetti to the skillet.\n8. Toss to coat the pasta with the garlic oil, adding a little reserved pasta water if needed to help distribute the sauce.\n9. Season with salt and pepper to taste.\n10. Remove from heat and stir in the chopped parsley.\n11. Serve immediately, with freshly grated Parmesan cheese on top if desired.",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 5,
            "image_path": "uploads/spaghetti-e-olio.jpg",
            "categories": ["Lunch","Pasta"]
        },
        {
            "recipe_name": "Omelette",
            "description": "A simple omelette is a quick and tasty dish made by cooking beaten eggs in a skillet until set, then folding them over any desired fillings.",
            "ingredients": "2 large eggs, Pinch of salt and pepper, 1 tablespoon butter or oil, Optional fillings: cheese, vegetables, meats",
            "steps": "1. Crack eggs into a bowl.\n2. Beat with a fork until mixed.\n3. Add a pinch of salt and pepper.\n4. Heat butter or oil in a skillet over medium heat.\n5. Pour eggs into skillet.\n6. Sprinkle desired fillings on one side of the cooking eggs.\n7. Once eggs are mostly set, fold the unfilled side over the filled side.\n8. Slide onto a plate and serve hot.",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 1,
            "image_path": "uploads/omelette.jpeg",
            "categories": ["Breakfast"]
        },
        {
            "recipe_name": "Scrambled Eggs",
            "description": "Classic scrambled eggs for a quick breakfast.",
            "ingredients": "Eggs, Salt, Pepper, Butter",
            "steps": "1. Crack eggs into a bowl\n2. Whisk with salt and pepper\n3. Melt butter in a pan\n4. Pour eggs into pan\n5. Stir until cooked to desired consistency",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/scrambled-eggs.jpg",
            "categories": ["Breakfast"]
        },
        {
            "recipe_name": "Fruit Salad",
            "description": "A refreshing and healthy fruit salad.",
            "ingredients": "Apple, Banana, Orange, Grapes, Honey",
            "steps": "1. Wash and chop fruits\n2. Combine fruits in a bowl\n3. Drizzle with honey\n4. Toss gently to combine",
            "difficulty": 1,
            "time_required": 2,
            "serving_size": 2,
            "image_path": "uploads/fruit-salad.jpg",
            "categories": ["Snack", "Healthy Food", "Dessert"]
        },
        {
            "recipe_name": "Vegetable Stir-Fry",
            "description": "A simple and delicious vegetable stir-fry.",
            "ingredients": "Broccoli, Bell Pepper, Carrot, Mushroom, Soy Sauce",
            "steps": "1. Chop vegetables into bite-sized pieces\n2. Heat oil in a pan\n3. Add vegetables and stir-fry until tender\n4. Season with soy sauce",
            "difficulty": 2,
            "time_required": 20,
            "serving_size": 2,
            "image_path": "uploads/vegetable-stir-fry.jpg",
            "categories": ["Lunch", "Dinner"]
        },
        {
            "recipe_name": "PB&J Sandwich",
            "description": "A classic peanut butter and jelly sandwich.",
            "ingredients": "Bread, Peanut Butter, Jelly",
            "steps": "1. Spread peanut butter on one slice of bread\n2. Spread jelly on the other slice of bread\n3. Press slices together to form a sandwich",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/pbj-sandwich.jpeg",
            "categories": ["Snack", "Breakfast", "Sandwich"]
        },
        {
            "recipe_name": "Green Salad",
            "description": "A simple and healthy green salad.",
            "ingredients": "Lettuce, Cucumber, Tomato, Olive Oil, Lemon Juice, Salt, Pepper",
            "steps": "1. Wash and chop lettuce, cucumber, and tomato\n2. Combine vegetables in a bowl\n3. Drizzle with olive oil and lemon juice\n4. Season with salt and pepper",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 2,
            "image_path": "uploads/green-salad.jpg",
            "categories": ["Salad", "Appetizer", "Healthy Food"]
        },
        {
            "recipe_name": "Vegetable Noodle Stir-Fry",
            "description": "A colorful and nutritious noodle stir-fry with assorted vegetables.",
            "ingredients": "Noodles (such as rice noodles or soba noodles), Bell Pepper, Carrot, Broccoli, Snap Peas, Soy Sauce, Sesame Oil, Ginger, Garlic, Green Onions",
            "steps": "1. Cook noodles according to package instructions\n2. Heat sesame oil in a pan or wok, add minced garlic and ginger\n3. Stir-fry sliced vegetables until tender-crisp\n4. Add cooked noodles and soy sauce to the pan, toss to combine\n5. Garnish with chopped green onions and serve hot",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 2,
            "image_path": "uploads/vegetable-noodle-stir-fry.jpg",
            "categories": ["Noodles", "Dinner"]
        },
        {
            "recipe_name": "Nasi Lemak",
            "description": "A traditional Malaysian dish featuring coconut rice served with various accompaniments.",
            "ingredients": "Rice, Coconut Milk, Pandan Leaves, Salt, Cucumber, Fried Anchovies, Roasted Peanuts, Hard-Boiled Eggs, Sambal (Chili Paste)",
            "steps": "1. Rinse rice and cook with coconut milk, pandan leaves, and salt until fluffy\n2. Serve with sliced cucumber, fried anchovies, roasted peanuts, hard-boiled eggs, and sambal",
            "difficulty": 2,
            "time_required": 3,
            "serving_size": 2,
            "image_path": "uploads/nasi_lemak.jpg",
            "categories": ["Malaysian", "Breakfast"]
        },
        {
            "recipe_name": "Minestrone Soup",
            "description": "A hearty Italian soup filled with vegetables, beans, pasta, and savory broth.",
            "ingredients": "Onion, Carrot, Celery, Garlic, Tomato, Potato, Zucchini, Green Beans, Cannellini Beans, Pasta (such as small shells or elbow macaroni), Vegetable Broth, Olive Oil, Salt, Pepper, Italian Seasoning, Parmesan Cheese (optional)",
            "steps": "1. Heat olive oil in a large pot, sauté onion, carrot, celery, and garlic until softened\n2. Add diced tomato, potato, zucchini, and green beans to the pot\n3. Pour in vegetable broth and bring to a simmer\n4. Stir in pasta and cannellini beans, cook until pasta is tender\n5. Season with salt, pepper, and Italian seasoning\n6. Serve hot with grated Parmesan cheese if desired",
            "difficulty": 2,
            "time_required": 4,
            "serving_size": 4,
            "image_path": "uploads/minestrone-soup.jpg",
            "categories": ["Soup", "Lunch", "Dinner"]
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
