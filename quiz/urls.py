from django.urls import path
from . import views

urlpatterns = [
    path('all', views.start_learn_all, name = 'start_learn_all'),
    path('<int:id>', views.start_learn_pack, name = 'start_learn_pack'),
    path('', views.learning_view, name = 'learn')
]