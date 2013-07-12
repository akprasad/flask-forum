# -*- coding: utf-8 -*-
"""
    seed
    ~~~~

    Add a lot of content to the forum.

    :license: MIT and BSD
"""

import random

from application import db
from application.models import *

NUM_BOARDS = 1
NUM_THREADS = 100
NUM_POSTS = 20


def main():
    users = User.query.all()

    for b in range(NUM_BOARDS):
        board = Board(
            name='Board %s' % b,
            slug='board-%s' % b,
            description='This is board number %s.' % b
        )
        db.session.add(board)
        db.session.flush()
        for t in range(NUM_THREADS):
            author_id = random.choice(users).id
            thread = Thread(
                name='Thread %s' % t,
                author_id=author_id,
                board_id=board.id
            )
            db.session.add(thread)
            db.session.flush()
            for p in range(NUM_POSTS):
                author_id = random.choice(users).id
                post = Post(
                    content='This is post number %s.' % p,
                    author_id=author_id,
                    thread_id=thread.id
                )
                thread.posts.append(post)

        db.session.commit()

if __name__ == '__main__':
    main()
