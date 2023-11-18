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
    
    # add serialization rules

    def __repr__(self):
        return f'<Coffee {self.id} {self.name}>'


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # add relationship
    
    # add serialization rules

    def __repr__(self):
        return f'<Customer {self.id} {self.name}>'


class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer)
    customization = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    # add relationship

    # add serialization rules

    def __repr__(self):
        return f'<Order {self.id} {self.price} {self.created_at} {self.customization}>'