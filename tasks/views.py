from django.shortcuts import render
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm
from tasks.models import Employee, Task

# Create your views here.
# main kaj -> response pass kora
    # Work with database
    # Transform data
    # Data pass
    # Http response / Json response 
    

def manager_dashboard(request):
    return render(request,"dashboard/manager-dashboard.html")   

def user_dashboard(request):
    return render(request,"dashboard/user-dashboard.html")

def test(request):
    context ={
        "names": ["Mahmud", "Un", "Nabi"],
        "age": 22
    }
    return render(request,"test.html", context)


#  GET vs POST Method in Django
# get method e search or data show kore and save kore
# post mothod e search or data show kore na and save kore na

def create_task(request):
    # Django Form
    
    # employees = Employee.objects.all() 
    # form = TaslForm(employees = employees) # for get 
    form = TaskModelForm() # for get
    
    # for post
    if request.method =="POST":
        # form = TaskForm(request.POST, employees = employees)
        form = TaskModelForm(request.POST)
        if form.is_valid():
            
            """For Model Form Data"""
            form.save()
            return render(request, 'task_form.html',{"form": form,
                          "message": "Task Added Successully"})
            
            """For Django Form data"""
            # data = form.cleaned_data
            # title = data.get('title')
            # description = data.get('description')
            # due_date = data.get('due_date')
            # assigned_to = data.get('assigned_to') # list [1,3]
            
            # task=Task.objects.create(
            #     title=title, description =description ,due_date=due_date
            # )
            # # Assign employee to tasks
            # for emp_id in assigned_to :
            #     employee = Employee.objects.get(id=emp_id)
            #     task.assigned_to.add(employee)
            # return HttpResponse("Task added successfully")
        
    context = {"form": form}
    return render(request, "task_form.html" , context)

# get()-> only give single data 
def view_task(request):
    # retrive all data from tasks model
    # tasks = Task.objects.all()
    
    # retrive a specific task
    # task_3 = Task.objects.get(pk=1)
    
    # Fetch the first task
    # first_task = Task.objects.first()
    
    return  render(request, "show_task.html",{"tasks": tasks,"task3": task_3, "first_task": first_task})
