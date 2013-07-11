from flask import Flask, render_template
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')


# Database
db = SQLAlchemy(app)
import models


# Security
datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, datastore)


# Endpoints
@app.route('/')
def index():
    return render_template('index.html')


import forum.views as forum
app.register_blueprint(forum.bp, url_prefix='/forum')
