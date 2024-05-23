from models import db, Admin
from werkzeug.security import generate_password_hash

# Manually create an Admin instance
admin = Admin(email_admin='jonk27@gmail.com', password_admin=123)

# Manually generate a hashed password
hashed_password = generate_password_hash('password_admin')

# Set the hashed password to the admin instance
admin.password_admin = hashed_password

# Add the admin instance to the database session and commit
db.session.add(admin)
db.session.commit()

