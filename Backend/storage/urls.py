from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.get_all_users),
    path('users/<int:pk>/', views.get_user),
    path('users/create/', views.create_user),
    path('users/delete/<int:pk>/', views.delete_user),

    path('calls/', views.get_all_calls),
    path('calls/<int:pk>/', views.get_call),
    path('calls/create/', views.create_call_with_sentiment),
    path('calls/<str:caller_number>/', views.get_calls_by_caller_number),
    path('calls/delete/<int:pk>/', views.delete_call),

    path('tickets/', views.get_all_tickets),
    path('tickets/<int:pk>/', views.get_ticket),
    path('tickets/create/', views.create_ticket),
    path('tickets/delete/<int:pk>/', views.delete_ticket),

    path('leads/', views.get_all_leads),
    path('leads/<int:pk>/', views.get_lead),
    path('leads/create/', views.create_lead),
    path('leads/delete/<int:pk>/', views.delete_lead),
]
