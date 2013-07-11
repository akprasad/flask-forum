DEBUG = True
SECRET_KEY = 'secret'

# flask-assets
# ------------
ASSETS_DEST = 'application/static'

# flask-security
# --------------
SECURITY_PASSWORD_HASH = 'bcrypt'
SECURITY_PASSWORD_SALT = '$2a$10$WyxRXkzAICMHgmqhMGTlJu'
SECURITY_REGISTERABLE = True

# flask-sqlalchemy
# ----------------
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.sql'
