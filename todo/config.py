import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todo.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    KEYCLOAK_SERVER_URL = 'http://localhost:8080/auth/'
    KEYCLOAK_CLIENT_ID = 'your-client-id'
    KEYCLOAK_REALM = 'your-realm'
    KEYCLOAK_CLIENT_SECRET = 'your-client-secret'
    STRIPE_SECRET_KEY = 'your_stripe_secret_key'
    STRIPE_PUBLISHABLE_KEY = 'your_stripe_publishable_key'
