from django.urls import path
from model_results import views

urlpatterns = [
    path('model_results/', views.result_list),
    path('model_results/<int:pk>/', views.result_detail),
]