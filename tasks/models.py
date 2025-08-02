from django.db import models
from django.db.models.signals import post_save, pre_save, post_delete, pre_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail


# Create your models here.

# Many to Many
class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    # task_set
    
    def __str__(self):
        return self.name


# create table
class Task(models.Model):
    STATUS_CHOICES=[
        ('PENDING', 'Pending'),
        ('IN_PROGRESS','In_Progress'),
        ('COMPLETED','Completed')
    ]
    #  Many to one 
    project = models.ForeignKey(
        "Project", 
        on_delete=models.DO_NOTHING, 
        default=1
        )
    
    # Many to Many
    assigned_to = models.ManyToManyField(Employee, related_name='tasks')
    title = models.CharField(max_length=250)  
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # details
    
    def __str__(self):
        return self.title


# one to one 
class TaskDetails(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_OPTION =(
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low')
    )
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE, related_name='details'
        )
    # assigned_to = models.CharField(max_length=250)
    priority = models.CharField(
        max_length=1, choices=PRIORITY_OPTION, default=LOW)
    notes = models.TextField(blank=True,null=True)
    
    def __str__(self):
        return f"Details form Task {self.task.title}"


# Many to one 
class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True,null=True)
    start_date = models.DateField() 
    
    def __str__(self):
        return self.name
    

# signals

# @receiver(post_save, sender=Task) # post_save
# def notify_task_creation(sender, instance, created, **kawrgs):
#     print('sender', sender)
#     print('instance', instance)
#     print(kawrgs)
#     print(created)
#     if created:
#         instance.is_completed = True
#         instance.save()


# @receiver(pre_save, sender=Task) # pre_save
# def notify_task_creation(sender, instance, **kawrgs):
#     print('sender', sender)
#     print('instance', instance)
#     print(kawrgs)
    
#     instance.is_completed = True



# @receiver(pre_delete, sender=Task) # pre_delete
# def notify_task_creation(sender, instance, **kawrgs):
#     print('sender', sender)
#     print('instance', instance)
#     print(kawrgs)


@receiver(m2m_changed, sender=Task.assigned_to.through) # many to many
def notify_task_creation(sender, instance, action, **kawrgs):
    if action =='post_add':
        assigned_emails = [ emp.email for emp in instance.assigned_to.all()]
        
        send_mail(
            "New Task Assigned",
            f"You have been assigned to the task: {instance.title}.",
            "unmahmud@gmail.com",
            assigned_emails,
            fail_silently=False,
        )
        
@receiver(post_delete, sender=Task) # post_delete
def delete_associated_details(sender, instance, **kawrgs):
    if instance.details:
        print('instance', instance)
        instance.details.delete()
        
        print("deleted successfully")
   
    
    
