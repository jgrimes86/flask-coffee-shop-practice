from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Coffee(db.Model, SerializerMixin):
    __tablename__ = 'coffees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # add relationship
    orders = db.relationship('Order', back_populates='coffee', cascade='all, delete-orphan')

    # add serialization rules
    serialize_rules = ('-orders.coffee',)

    #validate
    @validates('name')
    def validate_name(self, key, name):
        coffees = [coffee.name for coffee in Coffee.query.all()]
        if name in coffees:
            raise ValueError("Coffee must have a unique name")
        else:
            return name

    def __repr__(self):
        return f'<Coffee {self.id} {self.name}>'


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # add relationship
    orders = db.relationship('Order', back_populates='customer', cascade='all, delete-orphan')
    
    # add serialization rules
    serialize_rules = ('-orders.customer',)

    def __repr__(self):
        return f'<Customer {self.id} {self.name}>'


class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    customization = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    coffee_id = db.Column(db.Integer, db.ForeignKey('coffees.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))

    # add relationship
    coffee = db.relationship('Coffee', back_populates='orders')
    customer = db.relationship('Customer', back_populates='orders')

    # add serialization rules
    serialize_rules = ('-coffee.orders', '-customers.orders')

    # validation
    @validates('price')
    def validate_price(self, key, price):
        if price < 2:
            raise ValueError("Price must be greater than or equal to 2")
        else:
            return price

    def __repr__(self):
        return f'<Order {self.id} {self.price} {self.created_at} {self.customization}>'