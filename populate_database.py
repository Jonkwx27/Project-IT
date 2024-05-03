from datetime import datetime
from main import db, Recipe, create_app, Comment

def populate_database():
    app = create_app()
    with app.app_context():
        date_obj = datetime.strptime('2/4/24', '%d/%m/%y').date()

        recipe = Recipe(
            title='Spaghetti Bolognese',
            description='A classic Italian pasta dish with meat sauce.',
            ingredients='Spaghetti, ground beef, tomatoes, onion, garlic, olive oil, salt, pepper, Parmesan cheese',
            photo_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-6sTwopNQNhq2yuW8gitQ2oAzPEbEjRccdN0w_c2qKw&s',
        )

        steps = [
            "Cook spaghetti according to package instructions.",
            "In a large skillet, heat olive oil over medium heat.",
            "Add chopped onion and minced garlic, cook until softened.",
            "Add ground beef, cook until browned.",
            "Add diced tomatoes, salt, and pepper, simmer for 20 minutes.",
            "Serve over cooked spaghetti, garnish with Parmesan cheese."
        ]

        recipe.steps = '\n'.join(steps)

        try:
            db.session.add(recipe)
            db.session.commit()
            print("Recipe added successfully!")
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            db.session.rollback()

        comments = [
            {'name': 'Jonathan', 'comment': 'This spaghetti is so nice', 'rating': 1, 'recipe_id': recipe.id},
            {'name': 'Meor', 'comment': 'This spaghetti is so bad', 'rating': 5, 'recipe_id': recipe.id},
        ]
        
        for comment_data in comments:
            new_comment = Comment(name=comment_data['name'], comment=comment_data['comment'], rating=comment_data['rating'], recipe_id=comment_data['recipe_id'])
            db.session.add(new_comment)

        try:
            db.session.commit()
            print("Comments added successfully!")
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            db.session.rollback()
            
if __name__ == "__main__":
    populate_database()
