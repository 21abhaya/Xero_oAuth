from django.urls import path
from .views import homepage, callback, authorization_test_view

urlpatterns = [
    path("", homepage, name='homepage'),
    path("test-auth/", authorization_test_view, name='test_auth'),
    path("callback/", callback, name='callback'),
]