from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import AppUser
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

def login_view(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('accounts:user_list')
            else:
                form.add_error(None, 'Credenciales inválidas')
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('main_index')



class UserListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = AppUser
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'