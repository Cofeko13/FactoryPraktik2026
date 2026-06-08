from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # можно кнш сдлеать чуть по другому но все равно маршрут работает, так что пойдет хех
    path('generate/', views.generate_documents_view, name='generate'),
]