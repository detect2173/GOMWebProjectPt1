from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pricing/', views.pricing, name='pricing'),
    path('book/', views.book, name='book'),
    path('lead-magnet/', views.lead_magnet, name='lead_magnet'),
    path('lead-magnet/thanks/', views.lead_thanks, name='lead_thanks'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('start/', views.start, name='start'),
]