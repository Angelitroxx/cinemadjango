from django.contrib import admin
from mainApp.models import Peliculas, Funcion, Ventas


class PeliculaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'anno', 'director']


class FuncionAdmin(admin.ModelAdmin):
    list_display = ['pelicula', 'fecha', 'hora', 'asientos_vendidos', 'sala']


class VentasAdmin(admin.ModelAdmin):
    list_display = ['funcion', 'cliente', 'entradas', 'total_original', 'total_final']


admin.site.register(Peliculas, PeliculaAdmin)
admin.site.register(Funcion, FuncionAdmin)
admin.site.register(Ventas, VentasAdmin)
