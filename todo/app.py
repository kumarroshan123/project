from flask import Flask, request, jsonify, render_template
from flask_graphql import GraphQLView
from flask_cors import CORS
from models import db, ToDoItem, User
from schema import schema
from config import Config
from auth import login_required
from payment import create_checkout_session

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/login')
def login():
    return render_template('index.html')

@app.route('/checkout', methods=['POST'])
@login_required
def checkout(userinfo):
    session = create_checkout_session(userinfo.get('sub'))
    return jsonify({'sessionId': session['id']})

@app.route('/success')
def success():
    user_id = request.args.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if user:
        user.is_pro = True
        db.session.commit()
    return "Payment Successful"

@app.route('/cancel')
def cancel():
    return "Payment Cancelled"

app.add_url_rule(
    '/graphql',
    view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True)
)

if __name__ == '__main__':
    app.run(debug=True)
