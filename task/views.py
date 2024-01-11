from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TareaForm
from .models import Tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {
            'form': UserCreationForm})
    else:
        try:
            if request.POST['password1'] == request.POST['password2']:
                # creamos el usuario
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
        except IntegrityError:
            return render(request, "signup.html", {
                'form': UserCreationForm,
                'error': "Usuario ya existente"
            })
    return render(request, "signup.html", {
        'form': UserCreationForm,
        'error': "Las claves no coinciden!!"
    })


@login_required
def task(request):
    # filtramos la consulta de tareas por el usuario registrado actualmente y por las tareas que aún no han sido completadas. El campo datecompleted solo se actualiza al terminarse una tarea
    tarea = Tarea.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks.html", {
        'tareas': tarea
    })

@login_required
def task_finished(request):
    tarea = Tarea.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request, "tasks.html", {
        'tareas': tarea
    })


@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, "create_task.html", {
            'form': TareaForm
        })
    else:
        try:
            form = TareaForm(request.POST)

            # le decimos que no guarde los datos en base de datos. solo en nueva_tarea. Esto es, porque falta indicarle el valor de la ForeignKey (que en este caso es el id del usuario actual)
            nueva_tarea = form.save(commit=False)

            # request.user es el usuario que actualmente está logeado. Es variable global hasta que se logouteee
            nueva_tarea.user = request.user

            # Ahora sí lo grabamos en la BD porque la info de la tarea está completa
            nueva_tarea.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TareaForm,
                'error': "Por favor, provea datos válidos"
            })

@login_required
def tarea_detail(request, tarea_id):
    if request.method=="GET":
        # podemos obtener un solo objeto con get(). Por ejemplo así <tarea = Tarea.objects.get(pk=tarea_id)>. Pero con get_object_or_404 controlamos el error de que queramos acceder a un objeto con id fuera de la lista.
        tarea = get_object_or_404(klass=Tarea, pk=tarea_id)
        form= TareaForm(instance=tarea)
        return render(request, 'task_detail.html', {
            'tarea': tarea,
            'form': form
        })
    else:
        try:
            #Para no permitir actualizaciones de tareas de otro usuario, obligamos a que el objeto que consultamos sea del mismo usuario que realiza la petición: <user=request.user>
            tarea = get_object_or_404(klass=Tarea, pk=tarea_id, user=request.user)
            form= TareaForm(request.POST, instance=tarea)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'tarea': tarea,
            'form': form,
            'error':'error de entrada de datos'
        })
        

@login_required
def tarea_complete(request,tarea_id):
    tarea = get_object_or_404(klass=Tarea, pk=tarea_id,user=request.user)  
    #la tarea se considera completa cuando se asigna una fecha/hora al parámetro <datecompleted>. Una vez consignada, tarea_detail.html no la mostrará. Pero la tarea no se habrá eliminado de la base de datos todavía.
    tarea.datecompleted = timezone.now()
    tarea.save()
    return redirect('tasks')

@login_required
def delete_tarea(request,tarea_id):
    tarea = get_object_or_404(klass=Tarea, pk=tarea_id,user=request.user)  
    tarea.delete()
    return redirect('tasks')

@login_required
def signout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': "Usuario NO válido o password incorrecto"
            })
        else:
            login(request, user)
            return redirect('tasks')
