from django.shortcuts import render
from matplotlib import pyplot as plt
import mpld3

# Create your views here.


def index(request):
    return render(request, "admin.html")

