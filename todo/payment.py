import stripe
from config import Config

stripe.api_key = Config.STRIPE_SECRET_KEY

def create_checkout_session(user_id):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Pro License',
                },
                'unit_amount': 1000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:5000/success?session_id={CHECKOUT_SESSION_ID}&user_id=' + user_id,
        cancel_url='http://localhost:5000/cancel',
    )
    return session
