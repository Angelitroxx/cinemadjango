from django import forms
from mainApp.models import Funcion


class FormVenta(forms.Form):
    LARGO_CODIGO = 9
    VALIDADOR_CODIGO = 37  # los dígitos del código deben sumar 37

    id_funcion = forms.CharField(widget=forms.HiddenInput)
    cliente = forms.CharField(max_length=50)
    email = forms.CharField(max_length=50, required=False)
    entradas = forms.IntegerField(min_value=1, max_value=10)
    codigo = forms.CharField(required=False)

    id_funcion.widget.attrs['class'] = 'form-control'
    cliente.widget.attrs['class'] = 'form-control'
    email.widget.attrs['class'] = 'form-control'
    entradas.widget.attrs['class'] = 'form-control'
    codigo.widget.attrs['class'] = 'form-control'

    def clean_entradas(self):
        id_funcion = self.cleaned_data.get('id_funcion')
        entradas = self.cleaned_data['entradas']

        try:
            funcion = Funcion.objects.get(id=id_funcion)
        except (Funcion.DoesNotExist, ValueError, TypeError):
            raise forms.ValidationError("La función seleccionada no existe")

        if entradas > funcion.asientos_disponibles:
            raise forms.ValidationError("No hay tantas entradas disponibles")

        return entradas

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo'].strip()
        if codigo == "":
            return codigo

        codigo_erroneo = False
        if len(codigo) != self.LARGO_CODIGO:
            codigo_erroneo = True
        if not codigo.isdigit():
            codigo_erroneo = True

        if not codigo_erroneo:
            suma = sum(int(c) for c in codigo)
            if suma != self.VALIDADOR_CODIGO:
                codigo_erroneo = True

        if codigo_erroneo:
            raise forms.ValidationError("Codigo incorrecto")

        return codigo
