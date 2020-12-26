from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.index),
    path('admin', views.display_admin),
    path('LogInRegister', views.log_reg),
    path('userInfo', views.userInfo),
    # path('high', views.highcharts),
    url(r'^currency_order', views.DisplayUser.as_view()),
    path('payment', views.paymentInfo),
    path('Transfer', views.transfer),
    path('privacy', views.privacy)
]

