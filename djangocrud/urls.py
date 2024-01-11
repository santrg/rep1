"""
URL configuration for djangocrud project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from task import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('signup/', views.signup, name="signup"),
    path('tasks/', views.task, name="tasks"),
    path('tasks/finished', views.task_finished, name="tasks_finished"),
    path('tasks/create', views.create_task, name="create_task"),
    path('tasks/<int:tarea_id>', views.tarea_detail, name="tarea_detail"),
    path('tasks/<int:tarea_id>/complete', views.tarea_complete, name="tarea_completa"),
    path('tasks/<int:tarea_id>/delete', views.delete_tarea, name="borrar_tarea"),
    path('logout/', views.signout, name="logout"),
    path('login/', views.signin, name="login"),
]
