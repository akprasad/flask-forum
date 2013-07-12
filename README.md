# flask-forum

A forum app with some basic forum stuff:

- Authentication and session management
- Create boards, threads, and posts
- Write and edit posts in Markdown

Most of the forum code is contained in its own folder, and it's pretty easy to
move it to other projects and use it as a blueprint or whatever else you have
in mind. If you're new to Flask, this project is also a pretty good illustration
of how to use a variety of common and especially useful extensions.

## Extensions used

- [Flask-Admin](http://flask-admin.readthedocs.org/en/latest/) for database management
- [Flask-Assets](http://elsdoerfer.name/docs/flask-assets/) for asset management
- [Flask-Markdown](http://pythonhosted.org/Flask-Markdown/) for forum posts
- [Flask-Security](http://pythonhosted.org/Flask-Security/) for authentication
- [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/) for database queries
- [Flask-WTF](http://pythonhosted.org/Flask-WTF/) for forms

## Setup

```
pip install -r requirements.txt
python manage.py create_user -e <email> -p <password>
python manage.py create_role -n admin
python manage.py add_role -u <email> -r admin
python runserver.py
```

Then open up a browser and go to `localhost:5000`.