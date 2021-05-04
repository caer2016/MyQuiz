from django.urls import path
from . import views

urlpatterns = [
    path('', views.learning_view, name = 'learn'),
    path('<int:id>', views.learning_view, name = 'learn'),
    path('complete', views.learning_complete, name = 'learning_complete'),
]