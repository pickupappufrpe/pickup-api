from unittest import TestCase
from flask import url_for
from core import app
import jwt
import string
import random


class RootTests(TestCase):
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()

    def test_root_deve_retornar_hello_world(self):
        request = self.client.get(url_for('hello_world'))
        self.assertEqual('Hello, World!', request.data.decode())

    def test_root_deve_retornar_status_code_200(self):
        request = self.client.get(url_for('hello_world'))
        self.assertEqual(200, request.status_code)

    def test_registration(self):
        expected = 200
        login = "test_user_" + ''.join(random.choice(string.ascii_letters) for i in range(5))
        token = jwt.encode({}, app.config['SECRET_KEY'], algorithm='HS256')
        request = self.client.post(url_for('create_user'),
                                   json={"login": login, "password": "1234"},
                                   headers={'x-access-token': token},
                                   content_type='application/json'
                                   )
        # print(request.data.decode())
        # self.assertIn("id", request.data.decode())
        self.assertEqual(expected, request.status_code)
