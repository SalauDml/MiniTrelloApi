from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BoardModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="boards")
    title = models.CharField(max_length=20)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class TaskModel(models.Model):
    OPTION_CHOICES = [
        ('Done', 'Option A'),
        ('In-Progress', 'Option B'),
        ('Todo', 'Option C'),
    ]
    title = models.CharField(max_length=20)
    description = models.TextField()
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE,related_name="tasks")
    status = models.CharField(choices=OPTION_CHOICES,default="Todo")



#  Get all boards associated with a user tick
# Get all tasks associated with a board?