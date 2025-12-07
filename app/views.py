from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from .xero_auth_utils import make_xero_authorization_request, xero_obtain_access_token

        
def authorization_test_view(request):
    try:
        response = make_xero_authorization_request()
        
        if response.status_code != 200:
            return HttpResponse("Authorization request failed.", status=response.status_code)
        
        return HttpResponseRedirect(response.url)
    
    except Exception as e:
        return HttpResponse("This exception occurred when making authorization request:" + str(e), status=500)
    

def callback(request):
    #TODO: Needs refactoring here, verify request first. what if the response is not a dictionary?
    response = request.GET.dict()
    code = response.get("code")
    
    if not code:
        return HttpResponse("No code received in callback.", status=400)
    
    if code:
        try:
            response = xero_obtain_access_token(code)
        
            if response.status_code != 200:
                return HttpResponse("Failed to obtain access token.", status=response.status_code)
        
            access_token = response.json().get("access_token")
            token_type = response.json().get("token_type")
            expires_in = response.json().get("expires_in")
            scope = response.json().get("scope")
            
            return HttpResponse("Access token obtained successfully.", status=200)
        
        except Exception as e:
            return HttpResponse("This exception occurred while obtaining access token: " + str(e), status=500)
    return HttpResponse("Callback received. You can now exchange the code for tokens.", status=200)


def homepage(request):
    return render(request, 'base.html')
