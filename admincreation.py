import os
from flask import Flask
from flask_bcrypt import Bcrypt
from models import db, Admin  # Adjust the import according to your actual structure

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, template_folder="templates")
app.secret_key = "hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt = Bcrypt(app)

def create_admin(email, password):
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_admin = Admin(email_admin=email, password_admin=hashed_password)
        db.session.add(new_admin)
        db.session.commit()
        print(f"Admin user created with email: {email}")

if __name__ == "__main__":
    create_admin('jonk27@gmail.com', '123')
