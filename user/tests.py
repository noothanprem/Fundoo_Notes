from django.test import TestCase

# Create your tests here.
import json
#
# import requests
from decouple import config
# from django.test import TestCase
#
# from .models import Label
# with open("test.json") as f:
#     data = json.load(f)
from django.urls import reverse

from .models import img
from django.contrib.auth.models import User
from django.test import Client

header = {
    'HTTP_AUTHORIZATION': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNTc1NjMzMzIyLCJqdGkiOiI2MzE3NTI5Mzk3ZGE0OTMxYjFmYWNlNzRiN2I0YWJmNiIsInVzZXJfaWQiOjN9.g2MxwZtku38dZWL45xWDntim3LQe657U3ABXoXgYzSk'}
# headers = {
#    'Content_Type': "application/json",
#    'Authorization': "TEST_TOKEN"
# }
BASE_URL = config('BASE_URL')
# Create your tests here.
# import requests
# import json
#
# with open("/home/admin1/noothan/project/fundoo_notes/users/test.json") as f:
#     data = json.load(f)
#
# print(data)
#
#
# class Test_Registration:

#     def test_Registration_validinput(self):
#         url = "http://127.0.0.1:8000/accounts/register"
#         user = data['register'][0]
#         Response = requests.post(url, user)
#
#         assert Response.status_code == 200
#
#     def test_Registration_nullinput(self):
#         url = "http://127.0.0.1:8000/accounts/register"
#         user = data['register'][1]
#         Response = requests.post(url, user)
#         assert Response.status_code == 404
#
#
# class Test_Login:
#     def test_Login_validinput(self):
#         url = "http://127.0.0.1:8000/accounts/login"
#         user = data['login'][0]
#         Response = requests.post(url, user)
#         assert Response.status_code == 200
#
#     def test_Login_nullinput(self):
#         url = "http://127.0.0.1:8000/accounts/login"
#         user = data['login'][1]
#         Response = requests.post(url, user)
#         assert Response.status_code == 404
#
#
# class Test_ForgotPassword:
#     def test_ForgotPassword_validinput(self):
#         url = "http://127.0.0.1:8000/accounts/forgotpassword"
#         user = data['forgotpassword'][0]
#         Response = requests.post(url, user)
#         assert Response.status_code == 200
#
#     def test_ForgotPassword_nullinput(self):
#         url = "http://127.0.0.1:8000/accounts/forgotpassword"
#         user = data['forgotpassword'][1]
#         Response = requests.post(url, user)
#         assert Response.status_code == 404
#
#
# if __name__ == "__main__":
#     Test_Registration()

class LoginTest(TestCase):

    fixtures = ['fixtures/db']
    def test_registration1(self):
        url = BASE_URL + reverse('register_view')
        data = {'username':'sarang', 'email':'sarang@gmail.com', 'password':'12345'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,200)
    def test_registration2(self):
        url = BASE_URL + reverse('register_view')
        data = {'username':'', 'email':'sarang@gmail.com', 'password':'12345'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,400)
    def test_registration3(self):
        url = BASE_URL + reverse('register_view')
        data = {'username':'nipun', 'email':'nipun@gmail.com', 'password':'12345'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,400)

    def test_login1(self):
        url = BASE_URL + reverse('login_view')
        data = {'username':'admin','password':'admin'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,200)
    def test_login2(self):
        url = BASE_URL + reverse('login_view')
        data = {'username':'nipun','password':''}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,400)
    def test_login3(self):
        url = BASE_URL + reverse('login_view')
        data = {'username':'','password':'12345'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,400)
    def test_login4(self):
        url = BASE_URL + reverse('login_view')
        data = {'username':'gvsds','password':'12345'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code,400)

    def test_forgot_password1(self):
        url = BASE_URL + reverse('forgotpassword_view')
        data = {'email':'nipun@gmail.com'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,200)
    def test_forgot_password2(self):
        url = BASE_URL + reverse('forgotpassword_view')
        data = {'email':'nipu@gmail.com'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,400)
    def test_forgot_password3(self):
        url = BASE_URL + reverse('forgotpassword_view')
        data = {'email':''}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,400)

    def test_reset_password1(self):
        url = BASE_URL + reverse('resetpassword', args=['admin'])
        data = {'password':'admin'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,400)
    def test_reset_password2(self):
        url = BASE_URL + reverse('resetpassword', args=['eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5pcHVuIiwiZW1haWwiOiJuaXB1bkBnbWFpbC5jb20ifQ.BMAgeSxoLo7P-WwbUBm9uf4dM6DbBUk41Y-MxLwh5Uc'])
        data = {'password':'admin'}
        response = self.client.post(url,data)
        self.assertEqual(response.status_code,200)

