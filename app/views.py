import requests

from base64 import b64encode

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from .xero_auth import (
    make_xero_authorization_request,
    xero_obtain_access_token
)    
        
def authorization_test_view(request):
    response = make_xero_authorization_request()
    print("Redirecting to:", response.url)
    return HttpResponseRedirect(response.url)
    

def callback(request):
    response = request.GET.dict()
    print("Callback Response:", response)
    code = response.get("code")
    if code:
        print("Authorization Code:", code)
        obtained_token = xero_obtain_access_token(code)
        print("Obtained Token Response Header:", obtained_token.content)
        return HttpResponse(f"Access Token Response: {obtained_token.json()}")
    return HttpResponse("Callback received. You can now exchange the code for tokens.")


def homepage(request):
    return render(request, 'base.html')
