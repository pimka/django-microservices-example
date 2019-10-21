from django.http import Http404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from api.models import User
from api.serializers import UserSerializer


class UserOper(APIView):
    paginator = LimitOffsetPagination()
    paginator.default_limit = 100

    def get(self, request):
        users = User.objects.all()
        result = self.paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAdvOper(APIView):
    def get(self, request, user_id):
        try:
            user = User.objects.get(owner_uuid=user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            raise Http404


class UserExist(APIView):
    permissions = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        if request.user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
