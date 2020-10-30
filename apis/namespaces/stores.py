"""Servicio de tiendas"""

# Flask RESTPlus
from flask_restplus import Namespace, Resource, abort, fields, marshal_with

# Models
from apis.models.stores import Store
from apis.models.stocks import Stock

# Base de datos
from database import db


api = Namespace('tiendas', description='Operaciones relacionadas con tiendas')

store = api.model('Store', {
    'id': fields.Integer(read_only=True, description='Número de referencia'),
    'store': fields.String(required=True, description='Nombre del de la tienda'),
    'address': fields.String(required=True, description='Dirección de la tienda')
})

stock = api.model('Stock', {
    'id': fields.Integer(read_only=True, description='Número de referencia'),
    'store_id': fields.Integer(required=True, description='Número de referencia de la tienda'),
    'product_sku': fields.Integer(required=True, description='Número SKU del producto'),
    'minimum': fields.Integer(required=True, description='Existencia mínima'),
    'stock': fields.Integer(required=True, description='Existencia actual')
})

store_parser = api.parser()
store_parser.add_argument('store', type=str, required=True, help='Nombre de la tienda')
store_parser.add_argument('address', type=str, required=True, help='Dirección de la tienda')

update_store_parser = api.parser()
update_store_parser.add_argument('store', type=str, required=False, help='Nombre de la tienda')
update_store_parser.add_argument('address', type=str, required=False, help='Dirección de la tienda')

store = api.model('Store', {
    'id': fields.Integer(read_only=True, description='Número de referencia'),
    'store': fields.String(required=True, description='Nombre del de la tienda'),
    'address': fields.String(required=True, description='Dirección de la tienda')
})

stock = api.model('Stock', {
    'id': fields.Integer(read_only=True, description='Número de referencia'),
    'store_id': fields.Integer(required=True, description='Número de referencia de la tienda'),
    'product_sku': fields.Integer(required=True, description='Número SKU del producto'),
    'minimum': fields.Integer(required=True, description='Existencia mínima'),
    'stock': fields.Integer(required=True, description='Existencia actual')
})

stock_parser = api.parser()
stock_parser.add_argument('product_sku', type=int, required=True, help='Número SKU del producto')
stock_parser.add_argument('minimum', type=int, required=True, help='Existencia mínima')
stock_parser.add_argument('stock', type=int, required=True, help='Existencia actual')

update_stock_parser = api.parser()
update_stock_parser.add_argument('minimum', type=int, required=False, help='Existencia mínima')
update_stock_parser.add_argument('stock', type=int, required=False, help='Existencia actual')

@api.route('/')
class StoreListResource(Resource):
    """
    Muestra una lista de todas las 
    tiendas y te permite crear nuevas
    """

    @api.doc(id='get_stores')
    @api.marshal_with(store)
    def get(self):
        """Enlista todas las tiendas"""
        stores = db.session.query(Store).all()
        return stores
    
    @api.doc(id='post_store', parser=store_parser)
    @api.marshal_with(store)
    def post(self):
        """Crea una tienda"""
        args = store_parser.parse_args()
        store = Store(store=args['store'], address=args['address'])
        
        db.session.add(store)
        db.session.commit()
        
        return store, 201


@api.route('/<id>')
class StoreResource(Resource):
    """
    Muestra lo datos de una tienda,
    te permite modificarla y eliminarla
    """
    @api.doc(id='get_store')
    @api.marshal_with(store)
    def get(self, id):
        """Muestra los datos de una tienda"""
        store = db.session.query(Store).filter(Store.id == id).first()
        if not store:
            abort(404, message=f'No existe una tienda con el id:{id}')
        return store
    
    @api.doc(id='update_store', parser=update_store_parser)
    @api.marshal_with(store)
    def patch(self, id):
        """Actualiza una tienda"""
        args = update_store_parser.parse_args()
        store = db.session.query(Store).filter(Store.id == id).first()
        if not store:
            abort(404, message=f'No existe una tienda con el id:{id}')

        if parsed_args['store']:
            store.store = parsed_args['store']
        if parsed_args['address']:
            store.address = parsed_args['address']
        
        db.session.add(store)
        db.session.commit()
        
        return store, 201

    @api.doc(id='delete_store')
    def delete(self, id):
        """Elimina una tienda"""
        store = db.session.query(Store).filter(Store.id == id).first()
        if not store:
            abort(404, message=f'No existe una tienda con el id:{id}')
        
        db.session.delete(store)
        db.session.commit()
        
        return {}, 204


@api.route('/<id>/stock')
class StoreListResource(Resource):
    """
    Muestra una lista de todo el stock en una
    tienda y te permite dar de entrada nuevos productos
    """

    @api.doc(id='get_stock')
    @api.marshal_with(stock)
    def get(self, id):
        """Enlista el stock de la tienda"""
        stock = db.session.query(Stock).filter(Stock.store_id == id).all()
        if not stock:
            abort(404, message=f'No hay stock de productos en la tienda con el id:{id}')
        return stock
    
    @api.doc(id='post_stock', parser=stock_parser)
    @api.marshal_with(stock)
    def post(self, id):
        """Da de alta un nuevo producto en la tienda"""
        args = stock_parser.parse_args()
        stock = db.session.query(Stock).filter(
            Stock.store_id==int(id), 
            Stock.product_sku==args['product_sku']
        ).first()
        if stock:
            abort(404, message=f'El producto ya se encuentra registrado en está tienda con id:{id}')
        stock = Stock(store_id = int(id),
            product_sku = args['product_sku'],
            minimum = args['minimum'],
            stock = args['stock']
        )
        db.session.add(stock)
        db.session.commit()
        
        return stock, 201


@api.route('/<id>/stock/insuficiente')
class insufficientStockResource(Resource):
    """
    Muestra una lista de todo el stock donde es
    menor al minimo
    """

    @api.doc(id='get_insufficient_stock')
    @api.marshal_with(stock)
    def get(self, id):
        """Enlista el stock insuficiente de la tienda"""
        stock = db.session.query(Stock).filter(Stock.store_id == id, Stock.stock <= Stock.minimum).all()
        if not stock:
            abort(404, message=f'No hay stock insuficiente en la tienda con id:{id}')
        return stock
    

@api.route('/<id>/stock/<sku>')
class UpdateStockResource(Resource):
    """
    Te permite actualizar un stock 
    en una tienda
    """

    @api.doc(id='update_stock', parser=update_stock_parser)
    @api.marshal_with(stock)
    def patch(self, id, sku):
        """Ajusta el stock en una tienda"""
        parsed_args = update_store_parser.parse_args()
        stock = db.session.query(Stock).filter(
            Stock.store_id==int(id), 
            Stock.product_sku==int(sku)
        ).first()
        if not stock:
            abort(404, message=f'No hay stock del producto {sku} en la tienda {id}')
        
        if parsed_args['minimum'] != None:
            stock.minimum = parsed_args['minimum']
        if parsed_args['stock'] != None:
            stock.stock = parsed_args['stock']

        db.session.add(stock)
        db.session.commit()

        return stock, 201