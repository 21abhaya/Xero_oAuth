import requests

from base64 import b64encode

from django.http import HttpResponse, JsonResponse
from django.conf import settings


# testing out xero oauth2 
response_type="code"
scope="openid profile email"
client_id=settings.XERO_CLIENT_ID
client_secret=settings.XERO_CLIENT_SECRET
redirect_uri=settings.XERO_CALLBACK_URI
authorization_url=settings.XERO_AUTHORIZATION_URL
xero_connections_url=settings.XERO_CONNECTION_URL

def make_xero_authorization_request():    
    try:
        response = requests.get(
            authorization_url, 
            params={
                "response_type": response_type,
                "client_id": client_id,
                "redirect_uri": redirect_uri,
                "scope": scope 
            },
        )
        
        if response.status_code != 200:
            return HttpResponse("Failed to make authorization request.", status=response.status_code)
        #TODO: Look into this, what should be the correct response here?
        return response

    except requests.RequestException as e:
        return HttpResponse("Error making authorization request:" + str(e))

def xero_obtain_access_token(authorization_code):
    
    url = settings.XERO_ACCESS_TOKEN_URL
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = b64encode(credentials.encode('utf-8')).decode('utf-8')    
    
    headers = {
        "authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type":"client_credentials",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }
    
    try: 
        response = requests.post(
            url,
            headers=headers,
            data=data
        )
        
        if response.status_code != 200:
            return HttpResponse("Failed to obtain access token.", status=response.status_code)
        
        return response 
    
    except requests.RequestException as e:
        print("Error obtaining access token:", e)
        return HttpResponse("Error obtaining access token:" + str(e))
    

def test_xero_connections(access_token):
    
    url = xero_connections_url
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            url,
            headers=headers
        )
        
        if response.status_code != 200:
            return HttpResponse("Failed to fetch any Xero Connections", status=response.status_code)
        
        return JsonResponse(response.json())
    
    except requests.RequestException as e:
        return HttpResponse(f"Error fetching Xero connections: {e}" )