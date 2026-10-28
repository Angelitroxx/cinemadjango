from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Peliculas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('director', models.CharField(max_length=50)),
                ('anno', models.PositiveIntegerField()),
                ('duracion', models.PositiveIntegerField()),
                ('imagen', models.ImageField(upload_to='peliculas')),
            ],
            options={
                'verbose_name': 'película',
                'verbose_name_plural': 'películas',
            },
        ),
        migrations.CreateModel(
            name='Funcion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('precio', models.PositiveIntegerField()),
                ('asientos_disponibles', models.PositiveIntegerField()),
                ('asientos_vendidos', models.PositiveIntegerField()),
                ('sala', models.CharField(max_length=50)),
                ('pelicula', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.peliculas')),
            ],
            options={
                'verbose_name': 'función',
                'verbose_name_plural': 'funciones',
            },
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=50)),
                ('email', models.CharField(blank=True, max_length=50)),
                ('codigo', models.CharField(blank=True, max_length=50)),
                ('entradas', models.PositiveIntegerField()),
                ('total_original', models.PositiveIntegerField(default=0)),
                ('total_descuento', models.PositiveIntegerField(default=0)),
                ('total_final', models.PositiveIntegerField(default=0)),
                ('fecha', models.DateField()),
                ('funcion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainApp.funcion')),
            ],
            options={
                'verbose_name': 'venta',
                'verbose_name_plural': 'ventas',
            },
        ),
    ]
