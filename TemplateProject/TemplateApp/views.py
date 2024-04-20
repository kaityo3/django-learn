from django.shortcuts import render

# Create your views here.
def index(request):
    val="mojiretu"
    return render(request, "TemplateApp/index.html", context={"value":val})

def home(request, first_name, last_name):
    my_name = f"{first_name} {last_name}"
    favorite_fruits = ["Apple","Grape","Orange"]
    my_info = {
        "name": "murakami",
        "age": 28
    }
    status = 20
    return render(request,"home.html",context={
        "my_name": my_name,
        "favorite_fruits": favorite_fruits,
        "my_info": my_info,
        "status": status,
    })

def sample1(request):
    return render(request, "sample1.html")

def sample2(request):
    return render(request, "sample2.html")

def sample(request):
    name="satoshi murakami"
    height = 168.5
    weight = 69
    bmi = weight/(height / 100)**2
    page_url = "ホームページ: https://www.google.com"
    favorite_fruits = ["Apple","Grape","Orange"]
    msg = """hello
    my name is 
    murakami satoshi
    """
    msg2 = "123456789"
    return render(request, "sample.html", context={
        "name": name,
        "bmi": bmi,
        "page_url": page_url,
        "fluits": favorite_fruits,
        "msg": msg,
        "msg2": msg2,
    })

class Country:
    def __init__(self,name,population,capital):
        self.name = name
        self.population = population
        self.capital = capital

def sample3(request):
    country = Country("Japan",120000000,"Tokyo")
    return render(request, "sample3.html",context={
        "country": country
    })
