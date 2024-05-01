from flask import Flask, render_template, request, redirect, url_for
from models import Recipe, db, Comment

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()

    return app

app = create_app()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/signup')
def signup():
    return 'Sign Up'

@app.route('/login')
def login():
    return 'Log In'

@app.route('/recipes')
def recipe_details():
    recipe = Recipe.query.first()
    comments = Comment.query.all()  
    return render_template('in-depth.html', recipe=recipe, comments=comments)

@app.route('/submit_comment', methods=['POST'])
def submit_comment():
    if request.method == 'POST':
        name = request.form['name']
        comment_text = request.form['comment']
        rating = request.form['rating']
        recipe_id = request.form['recipe_id']  
        comment = Comment(name=name, comment=comment_text, rating=rating, recipe_id=recipe_id)
        
        try:
            db.session.add(comment)
            db.session.commit()
            return redirect(url_for('recipe_details'))
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            db.session.rollback()
            return "Error occurred while submitting the comment"

if __name__ == '__main__':
    app.run(debug=True)
