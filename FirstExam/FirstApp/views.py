from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("<h1>Hello World</h1>")

def add_page(request, num1, num2):
    return HttpResponse(f"<h1>{num1}+{num2}={num1+num2} add_page</h1>")

def minus_page(request, num1, num2):
    return HttpResponse(f"<h1>{num1}-{num2}={float(num1)-float(num2)} minus page</h1>")

def div_page(request, num1, num2):
    num1=float(num1)
    num2=float(num2)
    return HttpResponse(f"<h1>{num1}÷{num2}={num1/num2:.0f} devide page</h1>")
