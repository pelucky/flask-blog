#!/usr/bin/env python
# -*- coding=utf-8 -*-

import unittest
from app import create_app, db
from flask import url_for


class FalskClientTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TEST')
        self.app_content = self.app.app_context()
        self.app_content.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_content.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue('Blog' in response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
