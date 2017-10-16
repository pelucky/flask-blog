#!/usr/bin/env python
# -*- coding=utf-8 -*-

import unittest
from flask import current_app
from  app import create_app, db


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TEST')
        self.app_content = self.app.app_context()
        self.app_content.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_content.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'])


if __name__ == '__main__':
    unittest.main()
