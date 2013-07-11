from datetime import datetime

from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy.ext.declarative import declared_attr

from application import db


class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class UserRoleAssoc(db.Model):
    __tablename__ = 'user_role_assoc'
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.ForeignKey('role.id'), primary_key=True)


class User(Base, UserMixin):
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    roles = db.relationship('Role', secondary='user_role_assoc',
                            backref='users')

    def __repr__(self):
        return '<User(%s, %s)>' % (self.id, self.email)


class Role(Base, RoleMixin):
    name = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return '<Role(%s, %s)>' % (self.id, self.name)
