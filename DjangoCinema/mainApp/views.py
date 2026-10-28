from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from mainApp.models import Funcion, Ventas
from mainApp.forms import FormVenta


def index(request):
    funciones = Funcion.objects.select_related('pelicula').order_by('fecha', 'hora')
    data = {'funciones': funciones}
    return render(request, 'index.html', data)


def ticket(request, id):
    venta = get_object_or_404(Ventas.objects.select_related('funcion__pelicula'), id=id)
    data = {'venta': venta}
    return render(request, 'ticket.html', data)


def comprar(request, id):
    DESCUENTO = 37  # porcentaje si el código es válido
    funcion = get_object_or_404(Funcion.objects.select_related('pelicula'), id=id)

    if request.method == 'POST':
        datos = request.POST.copy()
        datos['id_funcion'] = str(id)  # siempre se valida contra la función de la URL
        form = FormVenta(datos)
        if form.is_valid():
            with transaction.atomic():
                # se bloquea la función para evitar vender asientos de más
                funcion = Funcion.objects.select_for_update().get(id=id)
                cantidad = form.cleaned_data['entradas']
                if cantidad > funcion.asientos_disponibles:
                    form.add_error('entradas', "No hay tantas entradas disponibles")
                else:
                    funcion.asientos_disponibles -= cantidad
                    funcion.asientos_vendidos += cantidad
                    funcion.save()

                    codigo = form.cleaned_data['codigo']
                    descuento = DESCUENTO if codigo != "" else 0

                    total_original = cantidad * funcion.precio
                    total_descuento = round(total_original * descuento / 100)
                    total_final = total_original - total_descuento

                    venta = Ventas.objects.create(
                        funcion=funcion,
                        cliente=form.cleaned_data['cliente'],
                        email=form.cleaned_data['email'],
                        codigo=codigo,
                        entradas=cantidad,
                        total_original=total_original,
                        total_descuento=total_descuento,
                        total_final=total_final,
                        fecha=timezone.localdate(),
                    )
                    return redirect('ticket', id=venta.id)
    else:
        form = FormVenta(initial={'id_funcion': id})

    data = {'funcion': funcion, 'form': form}
    return render(request, 'comprar.html', data)
