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


def userInfo(request):
    return render(request, 'user_page.html')


class DisplayUser(TemplateView):
    def get(self, request, **kwargs):
        latest_rate = models.Rate.objects.latest('timestamp')
        USD = latest_rate.USD
        JOD = latest_rate.JOD
        GBP = latest_rate.GBP
        JPY = latest_rate.JPY
        ILS = latest_rate.ILS
        return render(
            request,
            'currnecy_order.html',
            {
                'USD': USD,
                'JOD': JOD,
                'GBP': GBP,
                'JPY': JPY / 100,
                'ILS': ILS,
                'context': models.trans_table(request.session['logged_id'])
            })


def paymentInfo(request):
    context = {
        "TransferInfo": request.POST
    }
    return render(request, 'payment_info.html', context)


def transfer(request):
    errors = models.PaymentInfo.objects.card_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/payment')
    else:
        models.Transfer(request.POST, request.session['logged_id'])
        return redirect('/')


def display_admin(request):
    return render(request, "admin.html")


def log_reg(request):
    return render(request, 'log_reg.html')


def reg_validate(request):
    errors = models.User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request, 'errors_index.html')
    else:
        user_id = models.registration(request.POST)
        request.session['logged_id'] = user_id
        return redirect('/register')    


def register(request):
    errors = models.User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/LogInRegister')
    else:
        user_id = models.registration(request.POST)
        request.session['logged_id'] = user_id
        return redirect("/currency_order")

def login_validate(request):
    errors = models.User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return render(request, 'errors_index.html')
    else:
        context = models.log_in(request.POST)
        if context['flag']:
            request.session['logged_id'] = context['this_user'].id
            return redirect('/log_in')

def log_in(request):
    errors = models.User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/LogInRegister')
    else:
        context = models.log_in(request.POST)
        if context['flag']:
            request.session['logged_id'] = context['this_user'].id
            return redirect("/currency_order")
        else:
            messages.error(request, "you need to register")
            return redirect("/LogInRegister")


def log_out(request):
    del request.session['logged_id']
    return redirect('/')


def currency_order(request):
    if 'logged_id' in request.session:
        context ={
            'trans': models.trans_table(request.session['logged_id'])
        }
        trans =  models.trans_table(request.session['logged_id'])
        return render(request, "currnecy_order.html", context)
    return('/')

def edit_user(request):
    models.update_user(request.session['logged_id'], request.POST)
    return redirect('/currency_order')   

def privacy(request):
    return render(request, 'privacy.html')
