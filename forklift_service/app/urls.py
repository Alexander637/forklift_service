# urls.py
from django.urls import path
from .views import MachineListView, MaintenanceListView, ComplaintListView, search_machine_view
from . import views
from django.contrib.auth import views as auth_views
from allauth.account.views import LogoutView

urlpatterns = [
    path("machines/", MachineListView.as_view(), name="machine_list"),
    path("maintenances/", MaintenanceListView.as_view(), name="maintenance_list"),
    path("complaints/", ComplaintListView.as_view(), name="complaint_list"),
    path("search_machine/", search_machine_view, name="search_machine"),
    path('accounts/logout/', LogoutView.as_view(), name='account_logout'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.welcome_view, name='welcome'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
]