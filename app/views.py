from django.shortcuts import render, redirect
from django.http import HttpResponse

from xero_oauth.settings import XERO_CLIENT_ID, XERO_CLIENT_SECRET, XERO_ENDPOINT_URL, XERO_AUTHORIZATION_URL,XERO_ACCESS_TOKEN_URL, XERO_REFRESH_TOKEN_URL
from xero_python.api_client import ApiClient, serialize
from xero_python.api_client.configuration import Configuration
from xero_python.api_client.oauth2 import OAuth2Token

from authlib.integrations.django_client import OAuth

# configure xero-python sdk client
api_client = ApiClient(
    Configuration(
        debug=True,
        oauth2_token=OAuth2Token(
            client_id=XERO_CLIENT_ID,
            client_secret=XERO_CLIENT_SECRET,
        ),
    ),
)

# configure oauth django-client application
oauth = OAuth()
oauth = oauth.register(
    name="Xero",
    client_id=XERO_CLIENT_ID,
    client_secret=XERO_CLIENT_SECRET,
    endpoint_url=XERO_ENDPOINT_URL,
    authorize_url=XERO_AUTHORIZATION_URL,
    access_token_url=XERO_ACCESS_TOKEN_URL,
    refresh_token_url=XERO_REFRESH_TOKEN_URL,
)

token_details = {'token': None,
                 'modified': True}

@api_client.oauth2_token_getter
def get_xero_oauth2_token():
    return token_details["token"]

@api_client.oauth2_token_saver
def save_xero_oauth2_token(token):
    token_details["token"] = token
    token_details['modified'] = True

@api_client.oauth2_token_getter
def store_xero_oauth2_token(token):
    token_details["token"] = token
    token_details['modified'] = True
    

def xero_token_required(function):
    def decorator(*args, **kwargs):
        xero_token = get_xero_oauth2_token()
        if not xero_token:
            print(xero_token)
            print("Re Login")
            return redirect("/login")
        
        return function(*args, **kwargs)
    
    return decorator

def login(request):
    if not get_xero_oauth2_token():
        response = oauth.authorize_redirect(request, redirect_url="http://localhost:8000/callback")
        return response
    return redirect("home")

def logout(request):
    store_xero_oauth2_token(None)
    return redirect("login")

def oauth_callback(request):
    try:
        response = oauth.authorize_access_token(request)
    except Exception as e:
        print(e)
        raise
    if response is None or response.get("access_token") is None:
        return "Access denied: response=%s" % response
    print(response)
    store_xero_oauth2_token(response)
    return redirect("home")

def homepage(request):
    return HttpResponse("Hello, world. You're at the home page.")
