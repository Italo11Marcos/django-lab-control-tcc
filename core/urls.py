from django.urls import path
from .views import IndexView, CreateLaborationView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('panel/laboratorio/cadastrar', CreateLaborationView.as_view(), name='laboratorio-create'),
]