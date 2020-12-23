from django.urls import path     
from . import views


urlpatterns = [
    path('', views.index),
    path('userInfo', views.display_user),
    path('admin', views.display_admin),
]

