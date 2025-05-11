from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('generate_keys/', views.generate_keys, name='generate_keys'),
    path('sign_message/', views.sign_message, name='sign_message'),
    path('verify_signature/', views.verify_signature, name='verify_signature'),
    path('sign-document/', views.sign_document, name='sign_document'),
    path('verify-document/', views.verify_document, name='verify_document'),
    path('forge-document/', views.forge_document, name='forge_document'),
]