from flask import request, jsonify
from keycloak import KeycloakOpenID
from config import Config

keycloak_openid = KeycloakOpenID(
    server_url=Config.KEYCLOAK_SERVER_URL,
    client_id=Config.KEYCLOAK_CLIENT_ID,
    realm_name=Config.KEYCLOAK_REALM,
    client_secret_key=Config.KEYCLOAK_CLIENT_SECRET
)

def get_user_info(token):
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except:
        return None

def login_required(f):
    def wrap(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if auth_header:
            token = auth_header.split(' ')[1]
            userinfo = get_user_info(token)
            if userinfo:
                return f(userinfo, *args, **kwargs)
        return jsonify({"error": "Unauthorized"}), 401
    wrap.__name__ = f.__name__
    return wrap
