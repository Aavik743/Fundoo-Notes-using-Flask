# import unittest
# from main import app
#
#
# class MyTestCase(unittest.TestCase):
#     # def test_something(self):
#     #     self.assertEqual(True, False)  # add assertion here
#
#     def test_Register_API(self):
#         tester = app.test_client(self)
#         response = tester.get("/register")
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 200)
#
#
# if __name__ == '__main__':
#     unittest.main()


# import pytest
#
#
# def test_user_registration_pass(client):
#     url = '/register'
#     expected_cred = [
#         {'name': 'name'}, {'username': 'username'}, {'email_id': 'email@hotmail.com'}, {'password': '12345'}
#     ]
#
#     response = client.get(url)
#     assert response.json == expected_cred

# import requests
#
# # API route
# url = 'http://127.0.0.1:5000/activate'
#
# # Send get request
# response = requests.get(url)
#
# print(response.content)





# import requests
# from unittest import TestCase
#
#
# class MyTestCase(TestCase):
#     # API route
#     url = 'http://127.0.0.1:5000/activate'
#
#     def activate_account_fail(self, url):
#         # Send get request
#         response = requests.get(url)
#         print(response.content)
#         statuscode = response.status_code
#         self.assertEqual(statuscode, 401)
#
#
# if __name__ == '__main__':
#     MyTestCase.activate_account_fail()
