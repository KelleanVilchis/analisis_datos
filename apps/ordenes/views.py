from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Mesa, MesaEstado, Orden, OrdenDetalle
from .forms import MesaEstadoForm, MesaForm, OrdenForm, OrdenDetalleForm

class MesaEstadoListView(LoginRequiredMixin, ListView):
    model = MesaEstado
    template_name = 'mesas/mesas_estado_list.html'
    context_object_name = 'mesas_estados'

class MesaEstadoCreateView(LoginRequiredMixin, CreateView):
    model = MesaEstado
    form_class = MesaEstadoForm
    template_name = 'mesas/mesas_estado_form.html'
    success_url = '/ordenes/mesas_estado/'

class MesaEstadoUpdateView(LoginRequiredMixin, UpdateView):
    model = MesaEstado
    form_class = MesaEstadoForm
    template_name = 'mesas/mesas_estado_edit_form.html'
    success_url = '/ordenes/mesas_estado/'

class MesaEstadoDeleteView(LoginRequiredMixin, DeleteView):
    model = MesaEstado
    template_name = 'mesas/mesas_estado_confirm_delete.html'
    success_url = '/ordenes/mesas_estado/'

class MesaListView(LoginRequiredMixin, ListView):
    model = Mesa
    template_name = 'mesas/mesas_list.html'
    context_object_name = 'mesas'

class MesaCreateView(LoginRequiredMixin, CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'mesas/mesas_form.html'
    success_url = '/ordenes/mesas/'

class MesaUpdateView(LoginRequiredMixin, UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'mesas/mesas_edit_form.html'
    success_url = '/ordenes/mesas/'

class MesaDeleteView(LoginRequiredMixin, DeleteView):
    model = Mesa
    template_name = 'mesas/mesas_confirm_delete.html'
    success_url = '/ordenes/mesas/'

class OrdenListView(LoginRequiredMixin, ListView):
    model = Orden
    template_name = 'ordenes/ordenes_list.html'
    context_object_name = 'ordenes'

class OrdenCreateView(LoginRequiredMixin, CreateView):
    model = Orden
    form_class = OrdenForm
    template_name = 'ordenes/ordenes_form.html'
    success_url = '/ordenes/ordenes/'

    def get_initial(self):
        initial = super().get_initial()
        initial['empleado'] = self.request.user
        return initial

class OrdenDetalleView(LoginRequiredMixin, ListView):
    model = OrdenDetalle
    template_name = 'ordenes/orden_detalle_list.html'
    context_object_name = 'orden_detalles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orden'] = Orden.objects.get(id=self.kwargs.get('orden_id'))
        context['form'] = OrdenDetalleForm(initial={'orden_id': self.kwargs.get('orden_id')})
        return context

    def get_queryset(self):
        orden_id = self.kwargs.get('orden_id')
        return OrdenDetalle.objects.filter(orden__id=orden_id)
    
    def post(self, request, *args, **kwargs):
        form = OrdenDetalleForm(request.POST)
        if form.is_valid():
            orden_detalle = OrdenDetalle(
                orden=Orden.objects.get(id=form.cleaned_data['orden_id']),
                platillo=form.cleaned_data['platillo'],
                cantidad=form.cleaned_data['cantidad'],
                notas=form.cleaned_data['notas'],
                precio_unitario=form.cleaned_data['platillo'].precio
            )
            orden_detalle.save()
            return self.get(request, *args, **kwargs)
        else:
            return render(request, self.template_name, {'form': form, 'orden_detalles': self.get_queryset(), 'orden': Orden.objects.get(id=self.kwargs.get('orden_id'))})