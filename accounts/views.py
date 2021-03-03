from django.shortcuts import render
from .forms import *
from django.contrib import messages
from django.shortcuts import redirect

# Create your views here.
##Usuários CRUD##
def cadastro(request): 
    if request.method == "POST":
        form = CustomUsuarioCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro Realizado com Sucesso')
            return redirect('login')
        else:
            messages.error(request, 'Tivemos algum problema')
    else:
        form = CustomUsuarioCreateForm()
    context = {
        'form': form
    }
    return render(request, 'registration/register.html', context)


