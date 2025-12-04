import requests

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.conf import settings

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
    print("Response URI:", response.url)
    return response
    
def authorization_test_view(request):
    response = xero_authorization_request()
    return HttpResponseRedirect(response.url)
    
def homepage(request):
    return render(request, 'base.html')

def callback(request):
    response = request.GET.dict()
    print("Callback Response:", response)
    return HttpResponse("Callback received. You can now exchange the code for tokens.")

# def login_view(request):
#     if request.method == "GET":
#         response = xero_authorization_request()
#         return HttpResponseRedirect(response.url) 
#     return render(request, 'login.html')
