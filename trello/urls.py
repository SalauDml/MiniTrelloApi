from django.contrib import admin
from django.urls import path,include
from .views import TaskModelView,BoardView,SpecificBoardView
urlpatterns = [
    path('tasks/',TaskModelView.as_view()),
    path('boards/',BoardView.as_view()),
    path('boards/<int:id>/',SpecificBoardView.as_view())
]