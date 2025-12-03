import django.forms as forms
from .models import Mesa, MesaEstado, Orden, MetodoPago, Pago
from apps.platillos.models import Platillo

class MesaEstadoForm(forms.ModelForm):
    class Meta:
        model = MesaEstado
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['nombre', 'capacidad', 'estado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'})
        }

class OrdenForm(forms.ModelForm):
    class Meta:
        model = Orden
        fields = ['mesa', 'empleado']
        widgets = {
            'mesa': forms.Select(attrs={'class': 'form-control'}),
            'empleado': forms.HiddenInput(attrs={'class': 'form-control'})
        }

    def save(self, commit=True):
        orden = super().save(commit=False)
        if commit:
            orden.estatus = 'pendiente'  # Set default status
            orden.empleado = self.initial['empleado']
            orden.save()
        return orden

class OrdenDetalleForm(forms.Form):
    platillo = forms.ModelChoiceField(queryset=Platillo.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    cantidad = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    notas = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}), required=False)    
    orden_id = forms.IntegerField(widget=forms.HiddenInput())


class MetodoPagoForm(forms.ModelForm):
    class Meta:
        model = MetodoPago
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'})
        }

class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['orden', 'metodo_pago', 'cantidad']
        widgets = {
            'orden': forms.HiddenInput(),
            'metodo_pago': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'})
        }