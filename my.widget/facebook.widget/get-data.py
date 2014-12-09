#!/usr/bin/python
import sys
import json
import webbrowser

widget = Widget('facebook')

FB_CLIENT_ID = YOUR_FB_CLIENT_ID
FB_CLIENT_SECRET = 'YOUR_FB_CLIENT_SECRET'

FB_LOGIN_CODE = 'YOUR_FB_LOGIN_CODE'

FB_USER_ID = YOUR_USER_ID

# 1: open popup login window to get code
# 2: exchange code obtained from successful login to access_token and then trade access_token for long_term_access_token
# 3: get FB data with long_term_access_token
# else: disabled
SETTINGS_STEP = 4

def get_fb_access_token():
    params = {
        'client_id': FB_CLIENT_ID,
        'client_secret': FB_CLIENT_SECRET,
        'grant_type': 'client_credentials'
    }
    url = 'https://graph.facebook.com/oauth/access_token'
    access_token = widget.get_response(url, 'GET', params).content.split('=')[1]
    return access_token

def invoke_login_dialog():
    params = {
        'client_id': FB_CLIENT_ID,
        'redirect_uri': 'http://localhost/',
        'response_type': 'code',
        'display': 'popup',
        'scope': 'manage_permissions'
    }
    url = 'https://www.facebook.com/dialog/oauth'
    login_dialog_url = widget.get_response(url, 'GET', params).url
    webbrowser.open(login_dialog_url)

def get_fb_access_token_from_code(code):
    params = {
        'client_id': FB_CLIENT_ID,
        'client_secret': FB_CLIENT_SECRET,
        'code': code,
        'redirect_uri': 'http://localhost/'
    }
    url = 'https://graph.facebook.com/oauth/access_token'
    access_token_response = widget.get_response(url, 'GET', params)

    if 'error' in access_token_response:
        return 'ERR get_fb_access_token_from_code {}'.format(access_token_response['error'])

    return widget.parse_from_query(access_token_response.content, 'access_token')

def get_fb_long_term_access_token(short_term_access_token):
    params = {
        'grant_type': 'fb_exchange_token',
        'fb_exchange_token': short_term_access_token,
        'client_id': FB_CLIENT_ID,
        'client_secret': FB_CLIENT_SECRET,
        'redirect_uri': 'http://localhost/'
    }
    url = 'https://graph.facebook.com/oauth/access_token'
    access_token_response = widget.get_response(url, 'GET', params)

    if 'error' in access_token_response:
        return 'ERR get_fb_access_token_from_code {}'.format(access_token_response['error'])

    return widget.parse_from_query(access_token_response.content, 'access_token')

def build_access_token(access_token):
    return '{}|{}'.format(FB_CLIENT_ID, access_token)

data = {}

if SETTINGS_STEP == 1:
    login_dialog = invoke_login_dialog()
    data = "Login invoked. Get code parameter from success login URL, paste into FB_LOGIN_CODE and switch SETTINGS_STEP to 2"
elif SETTINGS_STEP == 2:
    access_token = get_fb_access_token_from_code(FB_LOGIN_CODE)
    long_term_access_token = get_fb_long_term_access_token(access_token)
    widget.persist('access_token', long_term_access_token)
    data = "Long life access: GRANTED. Switch SETTINGS_STEP to 3"
elif SETTINGS_STEP == 3:
    access_token = widget.load_persisted('access_token')
    query = 'SELECT name, unread_count, total_count FROM mailbox_folder WHERE viewer_id=me()'

    data = widget.get_response('https://graph.facebook.com/fql', 'GET', {'access_token': access_token, 'q': query}).text

print data if isinstance(data, dict) else data.encode('utf-8')
sys.exit()
