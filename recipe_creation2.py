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
    user = session.query(User).filter_by(id=2).first()
    
    if not user:
        print("User with ID 2 does not exist. Please create the user first.")
        return

    recipes_to_add = [
        {
            "recipe_name": "Cheeseburger",
            "description": "A juicy beef burger topped with cheese, lettuce, tomato, and onions.",
            "ingredients": "Ground Beef, Salt, Pepper, Cheese Slices, Burger Buns, Lettuce, Tomato, Onion, Ketchup, Mustard",
            "steps": "1. Season ground beef with salt and pepper, form into patties\n2. Grill or pan-fry patties to desired doneness\n3. Place cheese slice on top of each patty, let it melt\n4. Toast burger buns\n5. Assemble burgers with lettuce, tomato, onion, and desired condiments",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 4,
            "image_path": "uploads/cheeseburger.jpg",
            "categories": ["Burger", "Dinner", "Lunch"]
        },
        {
            "recipe_name": "Margherita Pizza",
            "description": "A simple and classic pizza with fresh tomatoes, mozzarella, and basil.",
            "ingredients": "Pizza Dough, Tomato Sauce, Fresh Mozzarella Cheese, Fresh Basil Leaves, Olive Oil, Salt",
            "steps": "1. Preheat oven to 475°F (245°C)\n2. Roll out pizza dough on a floured surface\n3. Spread tomato sauce over the dough\n4. Top with sliced fresh mozzarella\n5. Bake in preheated oven until crust is golden and cheese is bubbly\n6. Remove from oven, top with fresh basil leaves and a drizzle of olive oil",
            "difficulty": 3,
            "time_required": 3,
            "serving_size": 2,
            "image_path": "uploads/margherita-pizza.jpg",
            "categories": ["Pizza", "Dinner", "Lunch"]
        },
        {
            "recipe_name": "Chocolate Chip Cookies",
            "description": "Classic chewy and delicious chocolate chip cookies.",
            "ingredients": "Flour, Baking Soda, Salt, Butter, White Sugar, Brown Sugar, Vanilla Extract, Eggs, Chocolate Chips",
            "steps": "1. Preheat oven to 350°F (175°C)\n2. In a bowl, mix flour, baking soda, and salt\n3. In another bowl, beat butter, white sugar, and brown sugar until creamy\n4. Add vanilla extract and eggs, beat well\n5. Gradually add dry ingredients to the wet mixture\n6. Stir in chocolate chips\n7. Drop by rounded spoonfuls onto ungreased cookie sheets\n8. Bake for 8-10 minutes or until edges are lightly browned",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 9,
            "image_path": "uploads/chocolate-chip-cookies.jpg",
            "categories": ["Dessert"]
        },
        {
            "recipe_name": "Vanilla Panna Cotta",
            "description": "A creamy and smooth Italian dessert made with vanilla and cream.",
            "ingredients": "Heavy Cream, Milk, Sugar, Vanilla Extract, Gelatin, Fresh Berries (for garnish)",
            "steps": "1. In a saucepan, heat heavy cream, milk, and sugar until sugar dissolves\n2. Remove from heat, stir in vanilla extract\n3. Sprinkle gelatin over cold water, let it soften for a few minutes\n4. Stir gelatin mixture into warm cream until dissolved\n5. Pour into molds or ramekins\n6. Refrigerate for at least 4 hours or until set\n7. Serve with fresh berries",
            "difficulty": 2,
            "time_required": 2,
            "serving_size": 4,
            "image_path": "uploads/vanilla-panna-cotta.jpeg",
            "categories": ["Dessert"]
        },
        {
            "recipe_name": "Refreshing Lemonade",
            "description": "A classic and refreshing homemade lemonade.",
            "ingredients": "Lemons, Water, Sugar, Ice",
            "steps": "1. Juice the lemons to make about 1 cup of lemon juice\n2. In a pitcher, combine lemon juice, water, and sugar\n3. Stir until the sugar is dissolved\n4. Add ice and serve chilled",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 4,
            "image_path": "uploads/lemonade.jpg",
            "categories": ["Beverage", "Non-Alcoholic"]
        },
        {
            "recipe_name": "Classic Iced Coffee",
            "description": "A simple and delicious iced coffee to cool you down.",
            "ingredients": "Brewed Coffee, Ice, Milk (optional), Sugar (optional)",
            "steps": "1. Brew a strong cup of coffee and let it cool\n2. Fill a glass with ice cubes\n3. Pour the cooled coffee over the ice\n4. Add milk and sugar to taste, if desired",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/iced-coffee.jpg",
            "categories": ["Beverage", "Coffee", "Non-Alcoholic"]
        },
        {
            "recipe_name": "Berry Banana Smoothie",
            "description": "A healthy and delicious smoothie packed with berries and banana.",
            "ingredients": "Banana, Mixed Berries (strawberries, blueberries, raspberries), Greek Yogurt, Milk, Honey (optional)",
            "steps": "1. Combine banana, mixed berries, Greek yogurt, and milk in a blender\n2. Blend until smooth\n3. Add honey for extra sweetness, if desired\n4. Pour into a glass and serve immediately",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 2,
            "image_path": "uploads/berry-banana-smoothie.jpg",
            "categories": ["Beverage", "Healthy", "Non-Alcoholic"]
        },
        {
            "recipe_name": "Classic Hot Chocolate",
            "description": "A warm and comforting hot chocolate made from scratch.",
            "ingredients": "Milk, Cocoa Powder, Sugar, Vanilla Extract, Whipped Cream (optional), Chocolate Shavings (optional)",
            "steps": "1. In a saucepan, heat milk over medium heat until warm\n2. Whisk in cocoa powder and sugar until dissolved\n3. Continue to heat until hot, but not boiling\n4. Stir in vanilla extract\n5. Pour into a mug, top with whipped cream and chocolate shavings, if desired",
            "difficulty": 1,
            "time_required": 1,
            "serving_size": 1,
            "image_path": "uploads/hot-chocolate.jpg",
            "categories": ["Beverage",  "Non-Alcoholic"]
        },
        {
            "recipe_name": "Lamb Biryani",
            "description": "A fragrant and flavorful rice dish made with tender lamb and aromatic spices.",
            "ingredients": "Basmati Rice, Lamb, Yogurt, Onion, Garlic, Ginger, Tomatoes, Green Chilies, Biryani Masala, Cinnamon, Cloves, Bay Leaves, Cardamom, Saffron, Milk, Ghee, Fresh Coriander, Fresh Mint, Fried Onions",
            "steps": "1. Marinate lamb in yogurt, garlic, ginger, and biryani masala for at least 1 hour\n2. Cook basmati rice with cinnamon, cloves, bay leaves, and cardamom until half done\n3. In a large pot, heat ghee and fry onions until golden brown\n4. Add marinated lamb and cook until tender\n5. Layer partially cooked rice over the lamb\n6. Dissolve saffron in warm milk and drizzle over rice\n7. Top with fresh coriander, mint, and fried onions\n8. Cover pot with a tight lid and cook on low heat until rice is fully cooked\n9. Serve hot with raita or salad",
            "difficulty": 3,
            "time_required": 5,
            "serving_size": 6,
            "image_path": "uploads/lamb-biryani.jpg",
            "categories": ["Eid", "Indian", "Pakistani"]
        },
        {
            "recipe_name": "Baklava",
            "description": "A rich and sweet pastry made with layers of phyllo dough, nuts, and honey syrup.",
            "ingredients": "Phyllo Dough, Walnuts, Pistachios, Almonds, Butter, Cinnamon, Sugar, Water, Honey, Lemon Juice, Vanilla Extract",
            "steps": "1. Preheat oven to 350°F (175°C)\n2. Chop nuts and mix with cinnamon\n3. Layer phyllo dough in a baking dish, brushing each layer with melted butter\n4. Sprinkle nut mixture over the phyllo dough\n5. Repeat layers until all ingredients are used\n6. Cut into diamond shapes\n7. Bake for 45-50 minutes or until golden brown\n8. In a saucepan, combine sugar, water, honey, lemon juice, and vanilla extract; bring to a boil and simmer for 10 minutes\n9. Pour hot syrup over baked baklava\n10. Allow to cool completely before serving",
            "difficulty": 3,
            "time_required": 5,
            "serving_size": 10,
            "image_path": "uploads/baklava.jpg",
            "categories": ["Dessert", "Eid", "Middle Eastern"]
        },
        {
            "recipe_name": "Chinese Dumplings",
            "description": "Traditional Chinese dumplings filled with ground pork and vegetables.",
            "ingredients": "Ground Pork, Napa Cabbage, Green Onions, Ginger, Garlic, Soy Sauce, Sesame Oil, Dumpling Wrappers",
            "steps": "1. In a bowl, combine ground pork, finely chopped napa cabbage, green onions, grated ginger, minced garlic, soy sauce, and sesame oil\n2. Place a spoonful of filling in the center of each dumpling wrapper\n3. Fold the wrapper and seal the edges\n4. Boil or steam the dumplings until cooked through\n5. Serve with soy sauce or your favorite dipping sauce",
            "difficulty": 2,
            "time_required": 4,
            "serving_size": 4,
            "image_path": "uploads/chinese-dumplings.jpeg",
            "categories": ["Appetizer", "Chinese New Year", "Chinese"]
        },
        {
            "recipe_name": "Sweet and Sour Pork",
            "description": "A popular Chinese dish featuring crispy pork in a tangy sweet and sour sauce.",
            "ingredients": "Pork Tenderloin, Cornstarch, Egg, Green Bell Pepper, Pineapple, Onion, Ketchup, Rice Vinegar, Sugar, Soy Sauce, Garlic, Ginger",
            "steps": "1. Cut pork tenderloin into bite-sized pieces\n2. In a bowl, coat pork pieces with beaten egg and cornstarch\n3. Deep fry pork until golden and crispy\n4. In a pan, stir-fry chopped green bell pepper, pineapple, and onion\n5. Add garlic and ginger, cook until fragrant\n6. Mix ketchup, rice vinegar, sugar, and soy sauce to create the sweet and sour sauce\n7. Add fried pork to the pan and pour the sauce over\n8. Stir until everything is well coated and heated through\n9. Serve hot with steamed rice",
            "difficulty": 3,
            "time_required": 4,
            "serving_size": 4,
            "image_path": "uploads/sweet-and-sour-pork.jpg",
            "categories": ["Non-Halal", "Chinese New Year", "Chinese"]
        },
        {
            "recipe_name": "Samosas",
            "description": "Crispy and savory pastry filled with spiced potatoes and peas.",
            "ingredients": "Potatoes, Green Peas, Onion, Green Chilies, Ginger, Garlic, Cumin Seeds, Coriander Powder, Garam Masala, Turmeric, Red Chili Powder, Salt, All-Purpose Flour, Water, Oil",
            "steps": "1. Boil and mash potatoes\n2. In a pan, heat oil and add cumin seeds\n3. Add chopped onions, green chilies, ginger, and garlic; sauté until golden brown\n4. Add green peas, mashed potatoes, coriander powder, garam masala, turmeric, red chili powder, and salt; mix well\n5. Let the filling cool\n6. Prepare dough with all-purpose flour, water, and a pinch of salt\n7. Roll the dough into small circles, cut in half, and shape into cones\n8. Fill the cones with the potato mixture and seal the edges\n9. Deep fry until golden brown and crispy\n10. Serve hot with mint chutney or tamarind sauce",
            "difficulty": 2,
            "time_required": 5,
            "serving_size": 4,
            "image_path": "uploads/samosas.jpg",
            "categories": ["Appetizer", "Deepavali", "Indian"]
        },
        {
            "recipe_name": "Gulab Jamun",
            "description": "Soft and spongy milk-based sweets soaked in rose-flavored sugar syrup.",
            "ingredients": "Milk Powder, All-Purpose Flour, Baking Soda, Ghee, Milk, Sugar, Water, Cardamom Pods, Rose Water",
            "steps": "1. In a bowl, mix milk powder, all-purpose flour, and baking soda\n2. Add melted ghee and milk to form a soft dough\n3. Divide the dough into small balls\n4. In a deep pan, heat oil or ghee and fry the balls until golden brown\n5. In another pot, prepare sugar syrup with sugar, water, and cardamom pods; bring to a boil and simmer\n6. Add rose water to the syrup\n7. Soak the fried balls in the hot syrup for at least 2 hours\n8. Serve warm or at room temperature",
            "difficulty": 3,
            "time_required": 5,
            "serving_size": 6,
            "image_path": "uploads/gulab-jamun.jpg",
            "categories": ["Dessert", "Deepavali", "Indian"]
        },
        {
            "recipe_name": "Roast Turkey",
            "description": "A juicy and flavorful roast turkey perfect for a Christmas feast.",
            "ingredients": "Whole Turkey, Butter, Garlic, Fresh Herbs (thyme, rosemary, sage), Lemon, Salt, Black Pepper, Olive Oil, Carrots, Celery, Onion, Chicken Broth",
            "steps": "1. Preheat the oven to 325°F (165°C)\n2. Clean the turkey and pat it dry\n3. Rub the turkey with a mixture of softened butter, minced garlic, chopped fresh herbs, salt, and black pepper\n4. Stuff the cavity with lemon halves, fresh herb sprigs, and onion chunks\n5. Tie the legs together and tuck the wings under the bird\n6. Place the turkey on a roasting rack in a large roasting pan\n7. Add carrots, celery, and onion chunks to the bottom of the pan\n8. Pour chicken broth into the pan\n9. Roast the turkey, basting occasionally with pan juices, until the internal temperature reaches 165°F (74°C)\n10. Let the turkey rest before carving\n11. Serve with your favorite sides and gravy",
            "difficulty": 4,
            "time_required": 5,
            "serving_size": 10,
            "image_path": "uploads/roast-turkey.jpg",
            "categories": ["Main Course", "Christmas", "Holiday"]
        },
        {
            "recipe_name": "Gingerbread Cookies",
            "description": "Classic spiced gingerbread cookies perfect for decorating during the holidays.",
            "ingredients": "All-Purpose Flour, Baking Soda, Ground Ginger, Ground Cinnamon, Ground Cloves, Salt, Unsalted Butter, Brown Sugar, Egg, Molasses, Vanilla Extract, Powdered Sugar (for icing), Food Coloring (optional)",
            "steps": "1. In a bowl, whisk together flour, baking soda, ground ginger, ground cinnamon, ground cloves, and salt\n2. In a separate bowl, beat softened butter and brown sugar until creamy\n3. Add egg, molasses, and vanilla extract; mix well\n4. Gradually add the dry ingredients to the wet mixture, mixing until a dough forms\n5. Divide the dough in half, flatten into disks, and wrap in plastic wrap\n6. Chill the dough in the refrigerator for at least 1 hour\n7. Preheat the oven to 350°F (175°C)\n8. Roll out the dough on a floured surface to about 1/4 inch thickness\n9. Cut out shapes with cookie cutters and place on a baking sheet lined with parchment paper\n10. Bake for 8-10 minutes or until the edges are firm\n11. Let cookies cool completely before decorating with icing made from powdered sugar and a small amount of water or milk\n12. Add food coloring to the icing if desired and decorate as desired",
            "difficulty": 2,
            "time_required": 5,
            "serving_size": 10,
            "image_path": "uploads/gingerbread-cookies.jpg",
            "categories": ["Dessert", "Christmas", "Holiday"]
        }
    ]

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

        for category_name in recipe_data["categories"]:
            category = session.query(Category).filter_by(name=category_name).first()
            if category:
                new_recipe.categories.append(category)

        session.add(new_recipe)

    session.commit()
    print(f'{len(recipes_to_add)} recipes added.')

with app.app_context():
    add_recipes()

session.close()
