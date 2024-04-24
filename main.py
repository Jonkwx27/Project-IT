from flask import Flask, render_template
from models import Recipe, db

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
    return render_template('in-depth.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True)