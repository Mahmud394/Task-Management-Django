from django.urls import path
from tasks.views import manager_dashboard,user_dashboard,test,create_task,view_task,update_task,delete_task

urlpatterns = [
    
    path('manager_dashboard/', manager_dashboard, name="manager-dashboard"),
    path('user_dashboard/', user_dashboard),
    path('test/',test),
    path('create-task/', create_task, name = "create-task"),
    path('view_task/', view_task),
    path('update-task/<int:id>/', update_task, name = "update-task"),
    path('delete-task/<int:id>/', delete_task, name = "delete-task")
]