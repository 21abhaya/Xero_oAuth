import requests

from base64 import b64encode

from django.http import HttpResponse
from django.conf import settings


# testing out xero oauth2 
response_type="code"
client_id=settings.XERO_CLIENT_ID
client_secret=settings.XERO_CLIENT_SECRET
redirect_uri=settings.XERO_CALLBACK_URI
scope="openid profile email"
authorization_url=settings.XERO_AUTHORIZATION_URL


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
        print("request headers:", response.request.headers)
        return response 
    
    except requests.RequestException as e:
        print("Error obtaining access token:", e)
        return HttpResponse("Error obtaining access token:" + str(e))