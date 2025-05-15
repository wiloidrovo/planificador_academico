from django.contrib import admin
from .models import (
    Usuario, Rol, PeriodoAcademico, Planificacion,
    Actividad, DetalleActividad, Evidencia, Notificacion
)

# Personalización del admin para Usuario (opcional)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'cedula', 'escuela', 'is_staff')
    search_fields = ('username', 'email', 'cedula')
    filter_horizontal = ('roles', 'groups', 'user_permissions')

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Rol)
admin.site.register(PeriodoAcademico)
admin.site.register(Planificacion)
admin.site.register(Actividad)
admin.site.register(DetalleActividad)
admin.site.register(Evidencia)
admin.site.register(Notificacion)
