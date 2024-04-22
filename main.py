from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)