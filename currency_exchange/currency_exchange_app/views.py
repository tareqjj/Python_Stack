from django.shortcuts import render, redirect
import requests
import collections
import decimal
from datetime import datetime
from . import models
from django.views.generic import TemplateView
from django.contrib import messages

import json
# Create your views here.


def index(request):
    USD = requests.get('https://api.exchangeratesapi.io/history?start_at=2020-01-01&end_at=2020-12-25&base=USD&symbols=ILS')
    GBP = requests.get('https://api.exchangeratesapi.io/history?start_at=2020-01-01&end_at=2020-12-25&base=GBP&symbols=ILS')
    JPY = requests.get('https://api.exchangeratesapi.io/history?start_at=2020-01-01&end_at=2020-12-25&base=JPY&symbols=ILS')
    # JOD = requests.get('https://api.exchangeratesapi.io/history?start_at=2020-01-01&end_at=2020-12-25&base=JOD&symbols=ILS')

    # print('*' * 80)
    # print(list(tuple(x.json()['rates'])))
    # y = list(tuple(x.json()['rates']))
    usd = dict(USD.json()['rates'])
    usd = collections.OrderedDict(sorted(usd.items()))
    gbp = dict(GBP.json()['rates'])
    gbp = collections.OrderedDict(sorted(gbp.items()))
    jpy = dict(JPY.json()['rates'])
    jpy = collections.OrderedDict(sorted(jpy.items()))
    list1 =[]
    list2 = []
    list3 = []
    for key in usd:
        rate = usd[key]['ILS']
        year = datetime.strptime(key, '%Y-%m-%d').timestamp() * 1000
        list1.append([int(year), rate])
    for key in gbp:
        rate = gbp[key]['ILS']
        year = datetime.strptime(key, '%Y-%m-%d').timestamp() * 1000
        list2.append([int(year), rate])
    for key in jpy:
        rate = jpy[key]['ILS']
        year = datetime.strptime(key, '%Y-%m-%d').timestamp() * 1000
        list3.append([int(year), rate])

    context = {
        'list1': list1,
        'list2': list2,
        'list3': list3
    }
    return render(request, "home.html", context)


class DisplayUser(TemplateView):
    def get(self, request, **kwargs):
        latest_rate = models.Rate.objects.latest('timestamp')
        USD = latest_rate.USD
        JOD = latest_rate.JOD
        GBP = latest_rate.GBP
        JPY = latest_rate.JPY
        ILS = latest_rate.ILS
        print(latest_rate)
        return render(
            request,
            'currnecy_order.html',
            {
                'USD': USD,
                'JOD': JOD,
                'GBP': GBP,
                'JPY': JPY / 100,
                'ILS': ILS,
            })


def paymentInfo(request):
    return render(request, 'payment_info.html')


def transfer(request):
    errors = models.PaymentInfo.objects.card_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/payment')
    else:
        models.Transfer(request.POST)
        return redirect('/')


def display_admin(request):
    return render(request, "admin.html")


def log_reg(request):

    return render(request, 'log_reg.html')

def currency_order(request):
    current_rates = requests.get('http://data.fixer.io/api/latest?access_key=4405fe87f8ab4f75dc9765319b17f661&symbols=USD,JOD,GBP,JPY,ILS')
    # {"success":true,"timestamp":1608912426,"base":"EUR","date":"2020-12-25","rates":{"USD":1.22085,"JOD":0.865592,"GBP":0.901658,"JPY":126.327423,"ILS":3.931082}}
    return render(request, "currnecy_order.html")

def highcharts(request):
    x = requests.get('https://api.exchangeratesapi.io/history?start_at=2020-01-01&end_at=2020-12-25&base=USD&symbols=ILS')
    print('*' * 80)
    # print(list(tuple(x.json()['rates'])))
    # y = list(tuple(x.json()['rates']))
    z = dict(x.json()['rates'])
    z = collections.OrderedDict(sorted(z.items()))
    print(z)
    list1 =[]
    for key in z:
        rate = z[key]['ILS']
        # key += " 00:00:00"
        year = datetime.strptime(key, '%Y-%m-%d').timestamp() * 1000
        print('*' * 80)
        print(int(year))
        # print('-' * 80)
        # print(year)
        list1.append([int(year), rate])

    context = {
        'list1': list1
    }
    # seconds_since_epoch = datetime.datetime.now()
    # print(int(seconds_since_epoch))
    return render(request, 'highcharts.html', context)

