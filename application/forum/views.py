from sqlalchemy.exc import SQLAlchemyError as sql_exc
from flask import Blueprint, redirect, render_template, url_for
from flask.ext.security import current_user, login_required

from application import db
from application.models import Board, Thread, Post
import forms

GET_POST = ['GET', 'POST']

bp = Blueprint('forum', __name__)


@bp.route('/')
def index():
    boards = Board.query.all()
    return render_template('forum/index.html', boards=boards)


@bp.route('/<slug>/')
def board(slug):
    try:
        board = Board.query.filter(Board.slug == slug).one()
    except sql_exc:
        return redirect(url_for('.index'))

    threads = Thread.query.all()
    return render_template('forum/board.html', board=board,
                           threads=threads)


@bp.route('/<slug>/<int:id>')
@bp.route('/<slug>/<int:id>-<title>')
def thread(slug, id, title=None):
    try:
        board = Board.query.filter(Board.slug == slug).one()
    except sql_exc:
        return redirect(url_for('.index'))
    try:
        thread = Thread.query.filter(Thread.id == id).one()
    except sql_exc:
        return redirect(url_for('.board', slug=slug))

    posts = thread.posts
    return render_template('forum/thread.html', board=board,
                           thread=thread, posts=posts)


@bp.route('/<slug>/create/', methods=GET_POST)
@login_required
def create_thread(slug):
    try:
        board = Board.query.filter(Board.slug == slug).one()
    except sql_exc:
        return redirect(url_for('.index'))

    form = forms.CreateThreadForm()
    if form.validate_on_submit():
        t = Thread(name=form.name.data,
                   board=board,
                   author=current_user)
        db.session.add(t)
        db.session.flush()
        p = Post(content=form.content.data,
                 author=current_user)
        t.posts.append(p)
        db.session.commit()

        return redirect(url_for('.board', slug=slug))

    return render_template('forum/create_thread.html',
                           board=board,
                           form=form)


@bp.route('/<slug>/<int:id>/create', methods=GET_POST)
@login_required
def create_post(slug, id):
    try:
        board = Board.query.filter(Board.slug == slug).one()
    except sql_exc:
        return redirect(url_for('.index'))
    try:
        thread = Thread.query.filter(Thread.id == id).one()
    except sql_exc:
        return redirect(url_for('.board', slug=slug))

    form = forms.CreatePostForm()
    if form.validate_on_submit():
        p = Post(content=form.content.data,
                 author=current_user)
        thread.posts.append(p)
        thread.last_updated = p.created
        db.session.commit()

        return redirect(url_for('.thread', slug=slug, id=id))

    return render_template('forum/create_post.html',
                           board=board,
                           thread=thread,
                           form=form)
