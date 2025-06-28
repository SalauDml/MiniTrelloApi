from django.contrib import admin
from django.urls import path,include
from .views import RegView,LoginView
urlpatterns = [
    path('register/',RegView.as_view()),
    path('login/',LoginView.as_view())

]
