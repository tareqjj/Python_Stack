from django.urls import path
from django.conf.urls import url
from . import views


urlpatterns = [
    path('', views.index),
    path('admin', views.display_admin),
    path('LogInRegister', views.log_reg),
    # path('currency_order', views.currency_order),
    path('high', views.highcharts),
    url(r'^currency_order', views.DisplayUser.as_view()),
    path('payment', views.paymentInfo),
    path('Transfer', views.transfer)
]

