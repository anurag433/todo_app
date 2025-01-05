from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"), 
    path("register", views.register, name="register"), 
    path("login", views.login, name="login"), 
    path("logout/", views.logout, name="logout"),
    path("add", views.add, name="add"),
    path("delete/<int:id>", views.delete, name="delete"),
    path("change_status/<int:id>/<str:status>", views.change_status, name="change_status"),
    path('edit/<int:id>', views.edit_todo, name='edit_todo'),

     
    
]
