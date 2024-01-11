from django.contrib import admin
from .models import Tarea


class TareaAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)  # La coma es porque se le pasa una tupla

# Register your models here.


admin.site.register(Tarea, TareaAdmin)
