from flask import Flask, render_template
from flask.ext.assets import Bundle, Environment
from flask.ext.markdown import Markdown
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')


# Assets
assets = Environment(app)
assets.url = '/static'
assets.directory = app.config['ASSETS_DEST']

less = Bundle('less/style.less', filters='less', output='gen/style.css')
assets.register('all-css', less)


# Database
db = SQLAlchemy(app)
import models


# Admin
import admin


# Markdown
Markdown(app, safe_mode='escape')


# Security
datastore = SQLAlchemyUserDatastore(db, models.User, models.Role)
security = Security(app, datastore)


# Endpoints
@app.route('/')
def index():
    return render_template('index.html')


import forum.views as forum
app.register_blueprint(forum.bp, url_prefix='/forum')
