from django.urls import path
from .views import *

urlpatterns = [
    path('login/', login, name='login'),
    path('callback/', oauth_callback, name='callback'),
    path('logout/', logout, name='logout')
]