import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from api.models import OrderModel


class OrderTest(APITestCase):
    def test_create_order(self):
        test_order = {
            "order_type" : "R",
            "prop_uuid" : "123e4567-e89b-12d3-a456-426655440000",
            "customer_uuid" : "123e4567-e89b-12d3-a456-426655440000",
            "price" : 123456789
        }
        response = self.client.post('/orders/', test_order, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_all_orders(self):
        response = self.client.get('/orders/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OrderAdvTest(APITestCase):
    def setUp(self):
        OrderModel.objects.create(
            order_type="R",
            customer_uuid="123e4567-e89b-12d3-a456-426655440000",
            prop_uuid="123e4567-e89b-12d3-a456-426655440000",
            price=987456321
        )
        self.test_order = OrderModel.objects.get(prop_uuid="123e4567-e89b-12d3-a456-426655440000")

    def test_get_not_exist_order(self):
        response = self.client.get('/orders/00000000-0000-0000-0000-000000000001/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_exist_order(self):
        response = self.client.get(f'/orders/{self.test_order.order_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_order(self):
        test_another_order = {
            "order_type" : "S",
            "prop_uuid" : "123e4567-e89b-12d3-a456-426655440000",
            "customer_uuid" : "123e4567-e89b-12d3-a456-426655440000",
            "price" : 123456789
        }
        response = self.client.put(f'/orders/{self.test_order.order_uuid}/', data=test_another_order, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_order(self):
        response = self.client.delete(f'/orders/{self.test_order.order_uuid}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)