from unittest import TestCase
from flask import url_for
from core import app
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
        # self.username = "test_user_" + ''.join(random.choice(string.ascii_letters) for i in range(5))
        self.username = "abacate"
        self.password = "1234567890"
        self.token = jwt.encode({}, app.config['SECRET_KEY'], algorithm='HS256')

    def test_root_deve_retornar_hello_world(self):
        request = self.client.get(url_for('hello_world'))
        self.assertEqual('Hello, World!', request.data.decode())

    def test_root_deve_retornar_status_code_200(self):
        request = self.client.get(url_for('hello_world'))
        self.assertEqual(200, request.status_code)

    def test_registration(self):
        expected = 200
        request = self.client.post(url_for('create_user'),
                                   json={"username": self.username, "password": self.password},
                                   headers={'x-access-token': self.token},
                                   content_type='application/json'
                                  )
        # print(request.data.decode())
        # self.assertIn("id", request.data.decode())
        self.assertEqual(expected, request.status_code)

    def test_login(self):
        expected = 200
        data = self.username + ":" + self.password
        base = base64.urlsafe_b64encode(data.encode('UTF-8')).decode('ascii')
        # print('Base: ', base)
        request = self.client.get(url_for('login'),
                                  json={},
                                  headers={'x-access-token': self.token, 'Authorization': 'Basic ' + base},
                                  content_type='application/json'
                                  )
        self.token = request.data.decode('UTF-8')[10:-3]
        self.assertEqual(200, request.status_code)
