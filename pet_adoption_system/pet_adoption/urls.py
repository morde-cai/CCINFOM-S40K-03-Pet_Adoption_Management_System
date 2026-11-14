from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new-adoption/', views.new_adoption, name='new_adoption'),
    path('report/adoption-intake/', views.adoption_intake_report, name='adoption_intake_report'),
    path('report/staff/', views.staff_report, name='staff_report')
]