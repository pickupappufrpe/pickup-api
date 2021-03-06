from unittest import TestCase
from flask import url_for
from app import app
import jwt
import string
import random
import base64


class RootTests(TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.username = "test_user"
        self.password = "1234567890"
        self.token = jwt.encode({}, app.config['SECRET_KEY'], algorithm='HS256')

    def test_root_must_return_hello_world(self):
        request = self.client.get(url_for('hello_world'))
        self.assertEqual('Hello, World!', request.data.decode())

    def test_root__must_code_200(self):
        request = self.client.get(url_for('hello_world'))
        self.assertEqual(200, request.status_code)

    def test_a_registration(self):
        expected = 200
        request = self.client.post(url_for('create_user'),
                                   json={"username": self.username, "password": self.password},
                                   headers={'x-access-token': self.token},
                                   content_type='application/json'
                                   )
        self.assertEqual(expected, request.status_code)

    def test_b_login(self):
        expected = 200
        data = self.username + ":" + self.password
        base = base64.urlsafe_b64encode(data.encode('UTF-8')).decode('ascii')
        request = self.client.get(url_for('login'),
                                  json={},
                                  headers={'x-access-token': self.token,
                                           'Authorization': 'Basic ' + base},
                                  content_type='application/json'
                                  )
        self.token = request.data.decode('UTF-8')[10:-3]
        self.assertEqual(expected, request.status_code)

    def test_create_person(self):
        expected = 200
        token = jwt.encode({}, app.config['SECRET_KEY'], algorithm='HS256')
        request = self.client.post(url_for('create_person'),
                                   json={"name": "Chandler",
                                         "surname": "Bing"},
                                   headers={'x-access-token': token},
                                   content_type='application/json'
                                   )
        self.assertEqual(expected, request.status_code)
