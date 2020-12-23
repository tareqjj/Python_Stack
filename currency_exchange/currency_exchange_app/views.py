from django.shortcuts import render
# Create your views here.


def index(request):
    return render(request, "home.html")

def display_user(request):
    return render(request, "user_page.html")

def display_admin(request):
    return render(request, "admin.html")

