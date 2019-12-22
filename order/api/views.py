from django.http import Http404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.auth import TokenAuth
from api.models import CustomToken, OrderModel
from api.serializers import AppSerializer, OrderSerializer


class OrderOper(APIView):
    pagination = LimitOffsetPagination()
    pagination.default_limit = 100
    authentication_classes = [TokenAuth, ]


    def get(self, request):
        orders = OrderModel.objects.all()
        serializer = OrderSerializer(self.pagination.paginate_queryset(orders, request), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrderDetail(APIView):
    authentication_classes = [TokenAuth, ]

    def get_object(self, ord_uuid):
        try:
            return OrderModel.objects.get(order_uuid=ord_uuid)
        except OrderModel.DoesNotExist:
            raise Http404

    def get(self, request, ord_uuid):
        order = self.get_object(ord_uuid)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, ord_uuid):
        order = self.get_object(ord_uuid)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ord_uuid):
        order = self.get_object(ord_uuid)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ServiceAuth(ObtainAuthToken):
    authentication_classes = [TokenAuth, ]
    serializer_class = AppSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context = {'request': request})
        serializer.is_valid(raise_exception=True)
        token = CustomToken.objects.create()

        return Response({ 'token': token.token }, status.HTTP_200_OK)
