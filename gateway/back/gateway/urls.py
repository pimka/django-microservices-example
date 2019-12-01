"""gateway URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api.views.Order import OrderAdvOperView, OrderBaseOperView
from api.views.User import UserAdvOperView, UserAuthView, UserBaseOperView
from api.views.Prop import PropertyBaseOperView, PropertyAdvOperView
from api.views.Advanced import UsersOrdersView, UserOrdersAdvView, UserPropertyView, UserPropertyAdvView

urlpatterns = [
    path('auth/', UserAuthView.as_view(), name='auth'),
    path('user/', UserBaseOperView.as_view(), name='user'),
    path('user/<uuid:user_id>/', UserAdvOperView.as_view()),

    path('orders/', OrderBaseOperView.as_view(), name='orders'),
    path('orders/<uuid:ord_id>/', OrderAdvOperView.as_view()),

    path('props/', PropertyBaseOperView.as_view(), name='props'),
    path('props/<uuid:prop_id>/', PropertyAdvOperView.as_view()),

    path('user/<uuid:user_id>/orders/', UsersOrdersView.as_view()),
    path('user/<uuid:user_id>/orders/<uuid:ord_id>/', UserOrdersAdvView.as_view()),
    
    path('user/<uuid:user_id>/props/<uuid:prop_id>/', UserPropertyAdvView.as_view()),
    path('user/<uuid:user_id>/props/', UserPropertyView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)