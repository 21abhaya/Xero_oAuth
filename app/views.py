import requests

from django.shortcuts import render
from django.conf import settings

def homepage(request):
    return render(request, 'base.html')

def callback(request):
    return f"Callback received with params:{request.GET.dict()}"

def login_view(request):
    return render(request, 'login.html')


# testing out xero oauth2 
response_type="code"
client_id=settings.XERO_CLIENT_ID
redirect_uri=settings.XERO_CALLBACK_URI
scope="openid profile email"
authorization_url=settings.XERO_AUTHORIZATION_URL

def xero_authorization_request():
    response = requests.get(
        authorization_url, 
        params={
            "response_type": response_type,
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "scope": scope 
        },
    )
    
    print("Test Xero Authorization Response:", response)