# -*- coding: utf-8 -*-
"""
    forum_tests.py
    ~~~~~~~~~~~~~~

    Some basic tests on the forum app.

    TODO: test models, authentication

    :license: MIT and BSD
"""

import application
from application.models import *

ADMIN = 'admin@example.com'
USER = 'admin@example.com'


class Test(object):

    def setup(self):
        application.app.config.update({
            'TESTING': True,
            'DEBUG_TB_ENABLED': False,
            'SQLALCHEMY_DATABASE_URI': 'sqlite://'
        })
        self.app = application.app.test_client()
        application.db.create_all()

    def teardown(self):
        pass

    def assert_code(self, path, code):
        response = self.app.get(path)
        assert response.status_code == code

    def assert_redirect(self, path, location=None):
        response = self.app.get(path)
        assert response.status_code == 302
        if location:
            assert response.location == 'http://localhost' + location

    def test_basic_response_codes(self):
        self.assert_code('/', 200)
        self.assert_code('/unknown', 404)

    def test_auth_response_codes(self):
        self.assert_code('/login', 200)
        self.assert_code('/logout', 302)
        self.assert_code('/register', 200)

    def check_admin_endpoints(self, code):
        self.assert_code('/admin/', code)
        for item in ['board', 'thread', 'post', 'user', 'role']:
            url = '/admin/%sview/' % item
            self.assert_code(url, code)
            self.assert_code(url + 'new/', code)

    def test_admin_response_codes(self):
        self.check_admin_endpoints(404)


    def test_forum_response_codes(self):
        self.assert_code('/forum/', 200)
        self.assert_redirect('/forum/board/', '/forum/')
        self.assert_redirect('/forum/board/1', '/forum/')
        self.assert_redirect('/forum/board/1-thread', '/forum/')

        # These redirect to the login page
        self.assert_redirect('/forum/board/1/create')
        self.assert_redirect('/forum/board/1/1/edit')
