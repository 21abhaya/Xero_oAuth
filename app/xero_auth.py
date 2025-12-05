import requests

from base64 import b64encode

from django.conf import settings


# testing out xero oauth2 
response_type="code"
client_id=settings.XERO_CLIENT_ID
client_secret=settings.XERO_CLIENT_SECRET
redirect_uri=settings.XERO_CALLBACK_URI
scope="openid profile email"
authorization_url=settings.XERO_AUTHORIZATION_URL


def make_xero_authorization_request():    
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


def xero_obtain_access_token(authorization_code):
    
    url = settings.XERO_ACCESS_TOKEN_URL
    encoded_client_id = b64encode(client_id.encode('utf-8'))
    print(type(encoded_client_id))
    encoded_client_secret = b64encode(client_secret.encode('utf-8'))
    print(type(encoded_client_secret))
    
    headers = {
        "authorization": "Basic " + encoded_client_id.decode('utf-8') + ":" + encoded_client_secret.decode('utf-8'),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type":"client_credentials",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }
    
    response = requests.post(
        url,
        headers=headers,
        data=data
    )
    return response 
