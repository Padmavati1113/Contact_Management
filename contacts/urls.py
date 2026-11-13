from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add-contact/', views.add_contact, name='add_contact'),
    path('edit-contact/<int:contact_id>/', views.edit_contact, name='edit_contact'),
    path('delete-contact/<int:contact_id>/', views.delete_contact, name='delete_contact'),
]