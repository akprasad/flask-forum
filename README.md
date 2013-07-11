# flask-forum

A forum app made with multiple Flask extensions:

- [Flask-Admin](http://flask-admin.readthedocs.org/en/latest/)
- [Flask-Markdown](http://pythonhosted.org/Flask-Markdown/)
- [Flask-Security](http://pythonhosted.org/Flask-Security/)
- [Flask-SQLAlchemy](http://pythonhosted.org/Flask-SQLAlchemy/)
- [Flask-WTF](http://pythonhosted.org/Flask-WTF/)

## Setup

```
pip install -r requirements.txt
python manage.py create_user -e <email> -p <password>
python manage.py create_role -n admin
python manage.py add_role -u <email> -r admin
python runserver.py
```
