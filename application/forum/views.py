from sqlalchemy.exc import SQLAlchemyError as sql_exc
from flask import Blueprint, redirect, render_template, url_for

from application.models import Board, Thread, Post

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

    return render_template('forum/thread.html', board=board,
                           thread=thread, posts=posts)
