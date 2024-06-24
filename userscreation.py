import os
from flask import Flask
from models import db, User  # Adjust the import according to your actual structure
from flask_bcrypt import Bcrypt
from datetime import datetime
from pytz import timezone

app = Flask(__name__, template_folder="templates")
app.secret_key = "hello"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
bcrypt = Bcrypt(app)

def create_users(users_data):
    with app.app_context():
        for user_data in users_data:
            hashed_password = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
            new_user = User(
                name=user_data['name'],
                email=user_data['email'],
                username=user_data['username'],
                age=user_data.get('age'),
                password=hashed_password
            )
            db.session.add(new_user)
        db.session.commit()
        print("Users created successfully")

if __name__ == "__main__":
    # Example data for creating multiple users
    users_data = [
        {
            'name': 'John Doe',
            'email': 'john@gmail.com',
            'username': 'john_doe',
            'age': 30,
            'password': '123'
        },
        {
            'name': 'Jane Doe',
            'email': 'jane@gmail.com',
            'username': 'jane_doe',
            'age': 26,
            'password': '123'
        },
        {
            'name': 'Mail Bin Ismail',
            'email': 'mailismail@gmail.com',
            'username': 'mail_ismail',
            'age': 40,
            'password': '123'
        },
        {
            'name': 'Raju Patel',
            'email': 'rajupatel@gmail.com',
            'username': 'raju_patel',
            'age': 20,
            'password': '123'
        },
        {
            'name': 'Mei Mei',
            'email': 'meimei@gmail.com',
            'username': 'mei_mei',
            'age': 17,
            'password': '123'
        },
        {
            'name': 'Susanti',
            'email': 'susanti@gmail.com',
            'username': 'susanti',
            'age': 27,
            'password': '123'
        },
        {
            'name': 'Fizi',
            'email': 'fizi@gmail.com',
            'username': 'fizi',
            'age': 24,
            'password': '123'
        },
        {
            'name': 'Adam Bin Ali',
            'email': 'adamali@gmail.com',
            'username': 'adam_ali',
            'age': 49,
            'password': '123'
        },
        {
            'name': 'Devi',
            'email': 'devi@gmail.com',
            'username': 'devi',
            'age': 23,
            'password': '123'
        },
        {
            'name': 'Jarjit Singh',
            'email': 'jarjitsingh@gmail.com',
            'username': 'jarjit_singh',
            'age': 15,
            'password': '123'
        },
    ]
    
    create_users(users_data)
