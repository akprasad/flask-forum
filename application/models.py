from datetime import datetime

from flask.ext.security import UserMixin, RoleMixin
from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.orderinglist import ordering_list

from application import db


class Base(db.Model):

    """A base class that automatically creates the table name and
    primary key.
    """

    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class TimestampMixin(object):
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def readable_date(self, date, format='%H:%M on %-d %B'):
        """Format the given date using the given format."""
        return date.strftime(format)


# Authentication
# ~~~~~~~~~~~~~~
class UserRoleAssoc(db.Model):

    """Associates a user with a role."""

    __tablename__ = 'user_role_assoc'
    user_id = db.Column(db.ForeignKey('user.id'), primary_key=True)
    role_id = db.Column(db.ForeignKey('role.id'), primary_key=True)


class User(Base, UserMixin):

    """
    A forum user. `UserMixin` provides the following methods:

        `is_active(self)`
            Returns ``True`` if the user is active.

        `is_authenticated(self)`
            Always returns ``True``.

        `is_anonymous(self)`
            Always returns ``False``.

        `get_auth_token(self)`
            Returns the user's authentication token.

        `has_role(self, role)`
            Returns ``True`` if the user identifies with the specified role.

        `get_id(self)`
            Returns ``self.id``.

        `__eq__(self, other)`
            Returns ``True`` if the two users have the same id.

        `__ne__(self, other)`
            Returns the opposite of `__eq__`.
    """

    email = db.Column(db.String, unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    roles = db.relationship('Role', secondary='user_role_assoc',
                            backref='users')

    def __repr__(self):
        return '<User(%s, %s)>' % (self.id, self.email)

    def __unicode__(self):
        return self.email


class Role(Base, RoleMixin):

    """
    A specific role. `RoleMixin` provides the following methods:

        `__eq__(self, other)`
            Returns ``True`` if the `name` attributes are the same. If
            `other` is a string, returns `self.name == other`.

        `__ne__(self, other)`
    """

    name = db.Column(db.String)
    description = db.Column(db.String)

    def __repr__(self):
        return '<Role(%s, %s)>' % (self.id, self.name)


# Forum
# ~~~~~
class Board(Base):

    #: The human-readable name, e.g. "Python 3"
    name = db.Column(db.String)

    #: The URL-encoded name, e.g. "python-3"
    slug = db.Column(db.String, unique=True)

    #: A short description of what the board contains.
    description = db.Column(db.Text)

    #: The threads associated with this board.
    threads = db.relationship('Thread', cascade='all,delete', backref='board')

    def __unicode__(self):
        return self.name


class Thread(Base, TimestampMixin):
    name = db.Column(db.String(80))

    #: The original author of the thread.
    author_id = db.Column(db.ForeignKey('user.id'), index=True)
    author = db.relationship('User', backref='threads')

    #: The parent board.
    board_id = db.Column(db.ForeignKey('board.id'), index=True)

    #: An ordered collection of posts
    posts = db.relationship('Post', backref='thread',
                            cascade='all,delete',
                            order_by='Post.index',
                            collection_class=ordering_list('index'))

    #: Length of the threads
    length = db.Column(db.Integer, default=0)

    def __unicode__(self):
        return self.name


class Post(Base, TimestampMixin):
    #: Used to order the post within its :class:`Thread`
    index = db.Column(db.Integer, default=0, index=True)

    #: The post content. The site views expect Markdown by default, but
    #: you can store anything here.
    content = db.Column(db.Text)

    #: The original author of the post.
    author_id = db.Column(db.ForeignKey('user.id'), index=True)
    author = db.relationship('User', backref='posts')

    #: The parent thread.
    thread_id = db.Column(db.ForeignKey('thread.id'), index=True)


    def __repr__(self):
        return '<Post(%s)>' % self.id


def thread_posts_append(thread, post, initiator):
    """Update some thread values when `Thread.posts.append` is called."""
    thread.length += 1
    thread.updated = datetime.utcnow()

event.listen(Thread.posts, 'append', thread_posts_append)
