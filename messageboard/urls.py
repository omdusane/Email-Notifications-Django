from django.urls import path
from .views import *

urlpatterns = [
    path('', messageboard_view, name='messageboard'),
    path('subscribe/', subscribe_view, name='subscribe'),
    path('unsubscribe/', unsubscribe_view, name='unsubscribe'),
    path('newsletter/', newsletter_view, name='newsletter'),
    
]