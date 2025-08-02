from django.db.models.signals import post_save, pre_save, post_delete, pre_delete, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from tasks.models import Task



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
   
    
    
