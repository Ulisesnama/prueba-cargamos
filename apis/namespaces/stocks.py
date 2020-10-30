"""Servicio de stock"""

# Flask RESTPlus
from flask_restplus import Namespace, Resource, abort, fields, marshal_with

# Modelos
from apis.models.products import Product
from apis.models.stocks import Stock

# Base de datos
from database import db


api = Namespace('stock', description='Operaciones relacionadas con stock')

stock = api.model('Stock', {
    'id': fields.Integer(read_only=True, description='Número de referencia'),
    'store_id': fields.Integer(required=True, description='Número de referencia de la tienda'),
    'product_sku': fields.Integer(required=True, description='Número SKU del producto'),
    'minimum': fields.Integer(required=True, description='Existencia mínima'),
    'stock': fields.Integer(required=True, description='Existencia actual')
})

stock_parser = api.parser()
stock_parser.add_argument('store_id', type=int, required=True, help='Número de referencia de la tienda')
stock_parser.add_argument('product_sku', type=int, required=True, help='Número SKU del producto')
stock_parser.add_argument('minimum', type=int, required=True, help='Existencia mínima')
stock_parser.add_argument('stock', type=int, required=True, help='Existencia de arranque')


@api.route('/')
class StoreListResource(Resource):
    """
    Te permite crear nuevo stock de un producto
    en una tienda
    """

    @api.doc(id='post_stock', parser=stock_parser)
    @api.marshal_with(stock)
    def post(self):
        """Crea un nuevo stock"""
        args = stock_parser.parse_args()
        stock = db.session.query(Stock).filter(
            Stock.store_id==args['store_id'], 
            Stock.product_sku==args['product_sku']
        ).first()
        if stock:
            abort(404, message=f'El producto ya se encuentra registrado en está tienda')
        
        stock = Stock(store_id = args['store_id'],
            product_sku = args['product_sku'],
            minimum = args['minimum'],
            stock = args['stock']
        )
        db.session.add(stock)
        db.session.commit()
        
        return stock, 201