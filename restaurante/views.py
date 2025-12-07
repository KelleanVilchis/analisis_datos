from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from apps.ordenes.models import Orden
from datetime import date, datetime, timedelta
from django.db import models
from datetime import timedelta



def main_index(request):
    return render(request, 'main/main.html')

def index_user(request):
    ordenes_hoy = Orden.objects.filter(
        estatus='pagada',
        fecha_hora__date=date.today()
    )
    total_sales = sum(o.total for o in ordenes_hoy)
    cantidad_ordenes = ordenes_hoy.count()
    semana_actual = date.today().isocalendar()[1]
    ordenes_semana = Orden.objects.filter(
        estatus='pagada',
        fecha_hora__week=semana_actual
    )
    numero_dia_hoy = date.today().isocalendar()[2]  # lunes=1 ... domingo=7
    inicio_semana = date.today() - timedelta(days=numero_dia_hoy - 1)
    dias_semana = [inicio_semana + timedelta(days=i) for i in range(7)]
    ventas_por_dia = []
    labels = []
    datos = []
    for dia in dias_semana:
        ventas_dia = (
            ordenes_semana
            .filter(fecha_hora__date=dia)
            .aggregate(total=Sum(models.F('detalles__cantidad') * models.F('detalles__precio_unitario')))
        )['total'] or 0
        labels.append(dia.strftime('%A'))  
        datos.append(float(ventas_dia))
    ultimas_ordenes = Orden.objects.all().order_by('-fecha_hora')[:5]
    platillos_mas_vendidos = (
        Orden.objects.filter(estatus='pagada')
        .values('detalles__platillo__nombre')
        .annotate(total_vendido=Sum('detalles__cantidad'))
        .order_by('-total_vendido')[:10]
    )
    context = {
        'ventas_totales': total_sales,
        'cantidad_ordenes': cantidad_ordenes,
        'ventas_por_dia_labels': labels,
        'ventas_por_dia_datos': datos,
        'ultimas_ordenes': ultimas_ordenes,
        'platillos_mas_vendidos': platillos_mas_vendidos,
    }
    return render(request, 'main/main.html', context)