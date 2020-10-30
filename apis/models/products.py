"""Tabla de los productos"""

# Base de datos
from database import db


class Product(db.Model):
    """Modelo de los productos"""
    __tablename__ = 'products'
    sku = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(255))
    stocks = db.relationship('Stock', backref='product', lazy=True)