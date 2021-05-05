from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', LoginView.as_view(template_name='pages/login.html'), name='login'),
    path('register/', views.register, name='register'),

]