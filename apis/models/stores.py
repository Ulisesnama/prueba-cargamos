"""Tabla de las tiendas"""

# Base de datos
from database import db


class Store(db.Model):
    """Modelo de las tiendas"""
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    store = db.Column(db.String(255))
    address = db.Column(db.String(255))
    stocks = db.relationship('Stock', backref='store', lazy=True)
