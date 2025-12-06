from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from .xero_auth import (
    make_xero_authorization_request,
    xero_obtain_access_token
)    
        
def authorization_test_view(request):
    response = make_xero_authorization_request()
    if response.status_code != 200:
        return HttpResponse("Failed to make authorization request.", status=500)
    print("Redirecting to:", response.url)
    return HttpResponseRedirect(response.url)
    

def callback(request):
    response = request.GET.dict()
    print("Callback Response:", response)
    code = response.get("code")
    
    if code:
        response = xero_obtain_access_token(code)
       
        if response.status_code != 200:
            return HttpResponse("Failed to obtain access token.", status=500)
       
        token = response.json()
        return HttpResponse(f"Access Token obtained successfully: {token}")
    
    return HttpResponse("Callback received. You can now exchange the code for tokens.", status=200)


def homepage(request):
    return render(request, 'base.html')
