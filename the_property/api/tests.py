import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import PropertyModel


class PropertyTests(APITestCase):
    def test_create_property(self):
        test_prop = {
            "addres" : "Qwerty 12",
            "area": 123,
            "is_living" : True,
            "owner_uuid" : "123e4567-e89b-12d3-a456-426655440000"
        }
        response = self.client.post('/props/', test_prop, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_unique_property(self):
        test_prop = {
            "addres" : "Qwerty 12",
            "area": 123,
            "is_living" : True,
            "owner_uuid" : "123e4567-e89b-12d3-a456-426655440000"
        }
        response = self.client.post('/props/', test_prop, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post('/props/', test_prop, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_properties(self):
        response = self.client.get('/props/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PropertyAdvTest(APITestCase):
    def setUp(self):
        PropertyModel.objects.create(
            addres="Qwerty 12",
            area=123,
            is_living=True,
            owner_uuid="123e4567-e89b-12d3-a456-426655440000"
        )
        self.test_prop = PropertyModel.objects.get(addres="Qwerty 12")

    def test_get_exist_property(self):
        response = self.client.get(f'/props/{self.test_prop.prop_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_not_exist_property(self):
        response = self.client.get('/props/00000000-0000-0000-0000-000000000001/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_property(self):
        test_another_prop = {
            "addres" : "Qwerty 12",
            "area": 200,
            "is_living" : False,
            "owner_uuid" : "123e4567-e89b-12d3-a456-426655440000"
        }
        response = self.client.put(f'/props/{self.test_prop.prop_uuid}/', data=test_another_prop, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_prop(self):
        response = self.client.delete(f'/props/{self.test_prop.prop_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
