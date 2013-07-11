from flask import Flask, render_template
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)


# Endpoints
@app.route('/')
def index():
    return render_template('index.html')


import forum.views as forum
app.register_blueprint(forum.bp, url_prefix='/forum')


if __name__ == '__main__':
    db.create_all()
    app.run()
