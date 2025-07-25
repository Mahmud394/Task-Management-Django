from django.db import models

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
        on_delete=models.CASCADE, 
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
    


