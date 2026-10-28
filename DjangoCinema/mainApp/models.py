from django.db import models


class Peliculas(models.Model):
    nombre = models.CharField(max_length=50)
    director = models.CharField(max_length=50)
    anno = models.PositiveIntegerField()
    duracion = models.PositiveIntegerField()
    imagen = models.ImageField(upload_to="peliculas")

    class Meta:
        verbose_name = "película"
        verbose_name_plural = "películas"

    def __str__(self):
        return self.nombre + " (" + str(self.anno) + ")"


class Funcion(models.Model):
    pelicula = models.ForeignKey(Peliculas, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    precio = models.PositiveIntegerField()
    asientos_disponibles = models.PositiveIntegerField()
    asientos_vendidos = models.PositiveIntegerField()
    sala = models.CharField(max_length=50)

    class Meta:
        verbose_name = "función"
        verbose_name_plural = "funciones"

    def __str__(self):
        return self.pelicula.nombre


class Ventas(models.Model):
    funcion = models.ForeignKey(Funcion, on_delete=models.CASCADE)
    cliente = models.CharField(max_length=50)
    email = models.CharField(max_length=50, blank=True)
    codigo = models.CharField(max_length=50, blank=True)
    entradas = models.PositiveIntegerField()
    total_original = models.PositiveIntegerField(default=0)
    total_descuento = models.PositiveIntegerField(default=0)
    total_final = models.PositiveIntegerField(default=0)
    fecha = models.DateField()

    class Meta:
        verbose_name = "venta"
        verbose_name_plural = "ventas"

    def __str__(self):
        return f"{self.cliente} - {self.funcion} ({self.entradas})"
