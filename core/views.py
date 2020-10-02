from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import *
from django.urls import reverse_lazy

# Create your views here.
class IndexView(TemplateView):
    template_name = 'panel/index.html'

class CreateLaborationView(CreateView):
    form_class = LaboratorioForm
    template_name = 'panel/laboratorio/create.html'
    success_url = reverse_lazy('laboratorio-create')
    
