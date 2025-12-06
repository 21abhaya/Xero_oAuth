from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render

from .xero_auth import make_xero_authorization_request, xero_obtain_access_token, test_xero_connections

        
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
    
    try:
        if code:
            response = xero_obtain_access_token(code)
        
            if response.status_code != 200:
                return HttpResponse("Failed to obtain access token.", status=500)
        
            access_token = response.json().get("access_token")
            token_type = response.json().get("token_type")
            expires_in = response.json().get("expires_in")
            scope = response.json().get("scope")
            
            if token_type.lower() != "bearer":
                return HttpResponse("Invalid token type received.", status=500)
            
            test_connections = test_xero_connections(access_token)
            
            if test_connections.status_code != 200:
                return HttpResponse("Failed to fect any Xero Connections", status=500)
            
            return HttpResponse(test_connections, status=200)
        
        return HttpResponse("Callback received. You can now exchange the code for tokens.", status=200)

    except Exception as e:
        return HttpResponse("Error in processing callback:" + str(e), status=500)

def homepage(request):
    return render(request, 'base.html')
