from flask import Blueprint, render_template

bp = Blueprint('forum', __name__)


@bp.route('/')
def index():
    return render_template('forum/index.html')
