from django.contrib import admin
from .models import BoardModel,TaskModel
# Register your models here.

admin.site.register(BoardModel)
admin.site.register(TaskModel)