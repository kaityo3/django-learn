from django.shortcuts import render
import datetime

# Create your views here.
def home(request):
    return render(request, "home.html")

class Student:
    def __init__(self,id,name,join_date):
        self.id = id
        self.name = name
        self.face_pic= f"member_pic//{name.lower()}.jpg"
        self.join_date = datetime.datetime.strptime(join_date,"%Y/%m/%d")
        
member_list = [
    Student(0,"Taro","2020/04/23"),
    Student(1,"Jiro","2021/04/13"),
    Student(2,"Hanako","2020/08/23"),
    Student(3,"Yoshiko","2022/04/21")
    ]

def members(request):
    return render(request, "members.html",context={
        "members": member_list,
    })

def person(request,id):
    return render(request,"person.html",context={
        "person":member_list[id]
    })
