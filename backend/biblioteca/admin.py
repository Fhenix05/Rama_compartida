from django.contrib import admin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    # Esto hará que en el panel veas una tabla con estas columnas
    list_display = ('matricula_id', 'usuario_nombre', 'usuario_aPaterno')
    # Permite buscar usuarios por matrícula o nombre
    search_fields = ('matricula_id', 'usuario_nombre')