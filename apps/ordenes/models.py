from django.db import models
from apps.accounts.models import AppUser
from apps.platillos.models import Platillo

class MesaEstado(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    nombre = models.CharField(max_length=100, null=False)
    capacidad = models.IntegerField(null=False)
    estado = models.ForeignKey(MesaEstado, on_delete=models.CASCADE, related_name='mesas_estado')

    def __str__(self):
        return self.nombre

class Orden(models.Model):
    empleado = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='ordenes')
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE, related_name='ordenes')
    fecha_hora = models.DateTimeField(auto_now_add=True)
    estatus = models.CharField(max_length=50, default='pendiente')

class OrdenDetalle(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='detalles')
    platillo = models.ForeignKey(Platillo, on_delete=models.CASCADE, related_name='detalles')
    cantidad = models.IntegerField()
    notas = models.TextField(blank=True, null=True)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)    
    

class MetodoPago(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre

class Pago(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE, related_name='pagos')
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.CASCADE, related_name='pagos')
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_hora = models.DateTimeField(auto_now_add=True)