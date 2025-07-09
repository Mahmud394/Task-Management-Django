from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# main kaj -> response pass kora
def home(request):
    # Work with database
    # Transform data
    # Data pass
    # Http response / Json response 
    return HttpResponse("Welcome to the task management system")


def contact(request):
    return HttpResponse("<h1 style='color: red'>This is contact page<h1>")


def show_task(request):
    return HttpResponse("This is our task page")

def show_specific_task(request,id):
    print("id",id)
    print("id Type",type(id))
    return HttpResponse(f"This is show specific task page {id}")