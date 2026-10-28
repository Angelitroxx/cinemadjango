import datetime

from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from mainApp.models import Peliculas, Funcion

PELICULAS = [
    ("Avatar", "James Cameron", 2009, 162, "avatar.png"),
    ("Alien", "Ridley Scott", 1979, 117, "alien.png"),
    ("Tiburón", "Steven Spielberg", 1975, 124, "tiburon.png"),
    ("Moonlight", "Barry Jenkins", 2016, 111, "moonlight.png"),
    ("Cisne Negro", "Darren Aronofsky", 2010, 108, "cisne_negro.png"),
    ("Hollywood", "Quentin Tarantino", 2019, 161, "hollywood.png"),
    ("Reyes del Futuro", "Director Desconocido", 2010, 120, "reyes_futuro.png"),
]

# (película, días desde hoy, hora, precio, asientos, sala)
FUNCIONES = [
    ("Avatar", 1, "11:54", 4000, 40, "Sala1"),
    ("Avatar", 2, "00:55", 4000, 40, "Sala2"),
    ("Alien", 1, "12:57", 3500, 30, "Sala1"),
    ("Alien", 2, "21:00", 3500, 30, "Sala2"),
    ("Tiburón", 3, "18:30", 3000, 35, "Sala3"),
    ("Moonlight", 3, "17:48", 4000, 25, "Sala 4"),
    ("Cisne Negro", 4, "18:00", 15000, 40, "A-5"),
    ("Hollywood", 5, "20:15", 4500, 45, "Sala1"),
    ("Reyes del Futuro", 5, "16:00", 3800, 50, "Sala2"),
]


class Command(BaseCommand):
    help = "Carga 7 películas y 9 funciones de ejemplo (imágenes de ejemplo incluidas)."

    def handle(self, *args, **options):
        origen = settings.BASE_DIR / 'datos_ejemplo'
        peliculas = {}
        for nombre, director, anno, duracion, archivo in PELICULAS:
            pel, creada = Peliculas.objects.get_or_create(
                nombre=nombre,
                defaults={'director': director, 'anno': anno, 'duracion': duracion, 'imagen': ''},
            )
            if creada:
                with open(origen / archivo, 'rb') as f:
                    pel.imagen.save(archivo, File(f), save=True)
            peliculas[nombre] = pel

        if Funcion.objects.exists():
            self.stdout.write("Ya existen funciones; no se crean más.")
            return

        hoy = datetime.date.today()
        for nombre, dias, hora, precio, asientos, sala in FUNCIONES:
            Funcion.objects.create(
                pelicula=peliculas[nombre],
                fecha=hoy + datetime.timedelta(days=dias),
                hora=datetime.time.fromisoformat(hora),
                precio=precio,
                asientos_disponibles=asientos,
                asientos_vendidos=0,
                sala=sala,
            )
        self.stdout.write(self.style.SUCCESS("Datos de ejemplo cargados."))
