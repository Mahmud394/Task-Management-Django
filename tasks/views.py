from django.shortcuts import render,redirect
from django.http import HttpResponse
from tasks.forms import TaskForm, TaskModelForm,TaskDetailModelForm
from tasks.models import Employee, Task, TaskDetails,Project
from datetime import date
from django.db.models import Q, Count, Max, Min, Avg
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

# Create your views here.
# main kaj -> response pass kora
    # Work with database
    # Transform data
    # Data pass
    # Http response / Json response 

def is_manager(user):
    return user.groups.filter(name='Manager').exists()

def is_employee(user):
    return user.groups.filter(name='Manager').exists()
 
@user_passes_test(is_manager, login_url='no-permission')
def manager_dashboard(request):
    # tasks = Task.objects.select_related('details').prefetch_related('assigned_to').all()
    
    # getting task count
    # total_task = tasks.count()
    # completed_task = Task.objects.filter(status="COMPLETED").count()
    # in_progress_task = Task.objects.filter(status="IN_PROGRESS").count()
    # pending_task = Task.objects.filter(status="PENDING").count()
    
     # count = {
    #     "total_task":
    #     "completed_task":
    #     "in_progress_task":
    #     "pending_task":
    # }
    # context ={
    #     "tasks": tasks,
    #     "total_task": total_task,
    #     "pending_task": pending_task,
    #     "in_progress_task": in_progress_task,
    #     "completed_task": completed_task
    # }
    type = request.GET.get('type', 'all')
    # print(type)

    counts = Task.objects.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='COMPLETED')),
        in_progress=Count('id', filter=Q(status='IN_PROGRESS')),
        pending=Count('id', filter=Q(status='PENDING')),
    )
    # Retriving task data

    base_query = Task.objects.select_related(
        'details').prefetch_related('assigned_to')

    if type == 'completed':
        tasks = base_query.filter(status='COMPLETED')
    elif type == 'in-progress':
        tasks = base_query.filter(status='IN_PROGRESS')
    elif type == 'pending':
        tasks = base_query.filter(status='PENDING')
    elif type == 'all':
        tasks = base_query.all()
    
    context ={
        "tasks": tasks,
        "counts": counts
    }
    return render(request,"dashboard/manager-dashboard.html", context) 

# CRUD
# C=create
# R=read
# U=update
# D=delete
  
@user_passes_test(is_employee)
def employee_dashboard(request):
    return render(request,"dashboard/user-dashboard.html")



# GET vs POST Method in Django
# get method e search or data show kore and save kore
# post mothod e search or data show kore na and save kore na
@login_required
@permission_required("tasks.add_task", login_url='no-permission')
def create_task(request):
    # Django Form
    
    # employees = Employee.objects.all() 
    # form = TaslForm(employees = employees) # for get 
    task_form = TaskModelForm() # for get
    task_detail_form = TaskDetailModelForm()
    
    
    # for post
    if request.method =="POST":
        # form = TaskForm(request.POST, employees = employees)
        task_form = TaskModelForm(request.POST) # for post
        task_detail_form = TaskDetailModelForm(request.POST)
        if task_form.is_valid() and task_detail_form.is_valid():
            
            """For Model Form Data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, "Task Created Successfully")
            return redirect('create-task')
            
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
        
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html" , context)

@login_required
@permission_required("tasks.change_task", login_url='no-permission')
def update_task(request,id):
    task = Task.objects.get(id=id)
    task_form = TaskModelForm(instance=task) # for get
    
    if task.details:
        task_detail_form = TaskDetailModelForm(instance=task.details)
    
    # for post
    if request.method =="POST":
        task_form = TaskModelForm(request.POST,instance=task) # for post
        task_detail_form = TaskDetailModelForm(request.POST,instance=task.details)
        if task_form.is_valid() and task_detail_form.is_valid():
            
            """For Model Form Data"""
            task = task_form.save()
            task_detail = task_detail_form.save(commit=False)
            task_detail.task = task
            task_detail.save()
            
            messages.success(request, "Task updated Successfully")
            return redirect('update-task',id)
        
    context = {"task_form": task_form, "task_detail_form": task_detail_form}
    return render(request, "task_form.html" , context)

@login_required
@permission_required("tasks.delete_task", login_url='no-permission')
def delete_task(request, id):
    if request.method == 'POST':
        task = Task.objects.get(id=id)
        task.delete()
        messages.success(request, 'Task Deleted Successfully')
        return redirect('manager-dashboard')
    else:
        messages.error(request, 'Something went wrong')
        return redirect('manager-dashboard')

"""ORM"""
# get()-> only give single data 
@login_required
@permission_required("tasks.view_task", login_url='no-permission')
def view_task(request):
    # retrive all data from tasks model
    # tasks = Task.objects.all()
    
    # retrive a specific task
    # task_3 = Task.objects.get(pk=1)
    
    # Fetch the first task
    # first_task = Task.objects.first()
    
    """show the task that are pending"""
    # tasks = Task.objects.filter(status="PENDING")
    
    """show the task which due date is today"""
    # tasks = Task.objects.filter(due_date=date.today())
    
    """Show the task whose priority is not low"""
    # tasks = TaskDetails.objects.exclude(priority = "L")
    
    """Show the task contain word 'c' & status pending"""
    # tasks = Task.objects.filter(title__icontains="c", status = "PENDING" )
    
    """Show the task which are pending or in-progress """
    # tasks = Task.objects.filter(Q(status="PENDING" ) | Q(status="IN_PROGRESS"))
    
    """select related (foreignKey, OneToOneField)"""
    # tasks = Task.objects.select_related('details').all()
    # tasks = TaskDetails.objects.select_related('task').all()
    
    # tasks = Task.objects.select_related('project').all()
    
    """prefetch_related(reverse ForeignKey, ManyToMany)"""
    # tasks = Project.objects.prefetch_related('task_set').all()
    
    # tasks = Task.objects.prefetch_related('assigned_to').all()
    
    """ Aggregations """
    # min,max,count,sum,avg
    # task_count = Task.objects.aggregate(num_task= Count('id'))
    projects = Project.objects.annotate(num_task= Count('task')).order_by('num_task')
    return  render(request, "show_task.html",{"projects": projects})
