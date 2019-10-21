import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, force_authenticate

from api.models import User


class RegistrationTests(APITestCase):
    def test_create_user(self):
        test_user = {
            "username" : "test",
            "password" : "test1234"
        }
        response = self.client.post('/user/', test_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    '''def test_create_user_without_password(self):
        test_user = {
            "username" : "test",
            "password": ""
        }
        response = self.client.post('/user/', test_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)'''

    def test_create_unique_user(self):
        test_user = {
            "username" : "test",
            "password" : "test1234"
        }
        response = self.client.post('/user/', test_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/user/', test_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_users(self):
        response = self.client.get('/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LoginTests(APITestCase):
    def setUp(self):
        User.objects.create_user('testlogin', password='testlogin')

    def test_auth_without_password(self):
        response = self.client.post('/auth/', { "username" : "testlogin" }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth_with_incorrect_password(self):
        test_user = {
            "username" : "testlogin",
            "password" : "12345678"
        }
        response = self.client.post('/auth/', test_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_auth(self):
        test_user = {
            "username" : "testlogin",
            "password": "testlogin"
        }
        response = self.client.post('/auth/', test_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)