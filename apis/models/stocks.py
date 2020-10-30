"""Tabla intermediaria entre tiendas y productos"""

# Base de datos
from database import db


class Stock(db.Model):
    """Modelo intermediario entre tiendas y productos"""
    __tablename__ = 'stock'
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    product_sku = db.Column(db.Integer, db.ForeignKey('products.sku'))
    minimum = db.Column(db.Integer)
    stock  = db.Column(db.Integer)