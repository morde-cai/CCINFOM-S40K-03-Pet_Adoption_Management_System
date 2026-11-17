from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new-adoption/', views.new_adoption_list, name='new_adoption_list'),
    path('new-adoption/<int:pk>/', views.new_adoption_make, name='new_adoption_make'),
    path('adoptions/', views.adoption_list, name='adoption_list'),
    path('adoptions/<int:pk>/edit/', views.adoption_edit, name='adoption_edit'),
    path('report/adoption-intake/', views.adoption_intake_report, name='adoption_intake_report'),
    path('report/staff/', views.staff_report, name='staff_report'),
]