from django.http import Http404
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import OrderModel
from api.serializers import OrderSerializer


class OrderOper(APIView):
    pagination = LimitOffsetPagination()
    pagination.default_limit = 100

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
