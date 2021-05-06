from django.urls import path
from . import views

urlpatterns = [
    path('', views.learning_view, name = 'learn'),
    path('<int:id>', views.learning_view, name = 'learn'),
    path('complete', views.learning_complete, name = 'learning_complete'),
    path('pack/add', views.add_pack, name = 'add_pack'),
    path('pack/delete/<int:id>', views.delete_pack, name = 'delete_pack'),
    path('pack/question/add/<int:id>', views.add_question, name = 'add_question'),
    path('pack/question/edit/<int:id>', views.edit_question, name = 'edit_question'),
    path('pack/question/delete/<int:id>', views.delete_question, name = 'delete_question'),
]