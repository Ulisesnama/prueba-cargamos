"""Configuración de la API"""

# Flask RESTPlus
from flask_restplus import Api

# Namespaces
from apis.namespaces.products import api as ns_products
from apis.namespaces.stores import api as ns_stores
from apis.namespaces.stocks import api as ns_stocks


api = Api(
    title='API de Control de Inventario',
    version='1.0', 
    description='Un sistema de inventario de productos simple'
)


api.add_namespace(ns_products)
api.add_namespace(ns_stores)
api.add_namespace(ns_stocks)