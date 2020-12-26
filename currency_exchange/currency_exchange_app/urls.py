from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.index),
    path('admin', views.display_admin),
    path("register", views.register),
    path('log_in', views.log_in),
    path('log_out', views.log_out),
    path('LogInRegister', views.log_reg),
    path('userInfo', views.userInfo),
    # path('high', views.highcharts),
    url(r'^currency_order', views.DisplayUser.as_view()),
    path('payment', views.paymentInfo),
    path('Transfer', views.transfer),
    path('privacy', views.privacy),
    url(r'^check_reg/$', views.reg_validate, name='check_reg'),
    url(r'^check_login/$', views.login_validate, name='check_login'),
]

