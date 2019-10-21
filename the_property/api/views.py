from django.http import Http404
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import PropertyModel
from api.serializers import PropertySerializer


class PropertyDetail(APIView):
    def get_object(self, prop_uuid):
        try:
            return PropertyModel.objects.get(prop_uuid=prop_uuid)
        except PropertyModel.DoesNotExist:
            raise Http404

    def get(self, request, prop_uuid):
        prop = self.get_object(prop_uuid)
        serializer = PropertySerializer(prop)
        return Response(serializer.data)

    def put(self, request, prop_uuid):
        prop = self.get_object(prop_uuid)
        serializer = PropertySerializer(prop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, prop_uuid):
        prop = self.get_object(prop_uuid)
        prop.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PropertyOper(APIView):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 100

    def get(self, request):
        props = PropertyModel.objects.all()
        serializer = PropertySerializer(self.paginator.paginate_queryset(props, request), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
