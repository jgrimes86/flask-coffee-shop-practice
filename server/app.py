#!/usr/bin/env python3

from models import db, Customer, Coffee, Order
from flask_migrate import Migrate
from flask import Flask, request, make_response
from flask_restful import Api, Resource
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Coffee Shop Practice Challenge</h1>'

@app.route('/coffees')
def get_coffees():
    coffees = [coffee.to_dict(rules=('-orders',)) for coffee in Coffee.query.all()]
    response = make_response(
        coffees,
        200
    )
    return response

@app.route('/coffees/<int:id>', methods=["DELETE"])
def coffee_by_id(id):
    coffee = Coffee.query.filter_by(id=id).first()

    if request.method == 'DELETE':
        if not coffee:
            return make_response({"error": "Coffee not found"}, 404)

        db.session.delete(coffee)
        db.session.commit()
        return make_response({}, 204)



@app.route('/customers/<int:id>')
def customer_by_id(id):
    try:
        customer = Customer.query.filter_by(id=id).first().to_dict()
    except:
        return make_response({"error": "Customer not found"}, 404)
    
    return make_response(customer, 200)

api = Api(app)

class Orders(Resource):
    def get(self):
        orders = [order.to_dict(rules=('-coffee_id', '-customer_id', '-customer.orders', '-price')) for order in Order.query.all()]
        return make_response(orders, 200)

    def post(self):
        params = request.json
        try:
            new_order = Order(
                coffee_id=params['coffee_id'], 
                customer_id=params['customer_id'], 
                price=params['price'], 
                customization=params['customization'])
        except ValueError as v_error:
            return make_response({"error": [str(v_error)]}, 400)

        db.session.add(new_order)
        try:
            db.session.commit()
        except IntegrityError as i_error:
            return make_response({"error": [str(i_error)]}, 400)

        response = make_response(
            new_order.to_dict(rules=('-customer.orders',)),
            200
        )
        return response


api.add_resource(Orders, '/orders')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
