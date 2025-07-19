
import streamlit as st
from requests_oauthlib import OAuth2Session

GOOGLE_CLIENT_ID = st.secrets["google_oauth_client_id"]
GOOGLE_CLIENT_SECRET = st.secrets["google_oauth_client_secret"]
GOOGLE_REDIRECT_URI = st.secrets["google_oauth_redirect_uri"]
GOOGLE_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_SCOPE = ['openid', 'email', 'profile']

MS_CLIENT_ID = st.secrets["ms_client_id"]
MS_CLIENT_SECRET = st.secrets["ms_client_secret"]
MS_TENANT_ID = st.secrets["ms_tenant_id"]
MS_REDIRECT_URI = GOOGLE_REDIRECT_URI
MS_AUTH_URI = f'https://login.microsoftonline.com/{MS_TENANT_ID}/oauth2/v2.0/authorize'
MS_SCOPE = ['User.Read']

def get_google_auth_url():
    google = OAuth2Session(GOOGLE_CLIENT_ID, scope=GOOGLE_SCOPE, redirect_uri=GOOGLE_REDIRECT_URI)
    auth_url, _ = google.authorization_url(GOOGLE_AUTH_URI, access_type='offline', prompt='consent')
    return auth_url

def get_microsoft_auth_url():
    ms = OAuth2Session(MS_CLIENT_ID, scope=MS_SCOPE, redirect_uri=MS_REDIRECT_URI)
    auth_url, _ = ms.authorization_url(MS_AUTH_URI, response_mode='query')
    return auth_url
