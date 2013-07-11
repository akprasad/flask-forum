# flask-forum

A forum app made with multiple Flask extensions:

- [Flask-Admin](http://flask-admin.readthedocs.org/en/latest/) for database management
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
