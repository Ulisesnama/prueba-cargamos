"""Servicio de productos"""

# Flask RESTPlus
from flask_restplus import Namespace, Resource, abort, fields, marshal_with

# Modelos
from apis.models.products import Product
from apis.models.stocks import Stock

# Base de datos
from database import db


api = Namespace('productos', description='Operaciones relacionadas con productos')

product = api.model('Product', {
    'sku': fields.Integer(required=False, description='Número de referencia'),
    'product': fields.String(required=True, description='Nombre del producto')
})
stock = api.model('Stock', {
    'id': fields.Integer(read_only=True, description='Número de referencia'),
    'store_id': fields.Integer(required=True, description='Número de referencia de la tienda'),
    'product_sku': fields.Integer(required=True, description='Número SKU del producto'),
    'minimum': fields.Integer(required=True, description='Existencia mínima'),
    'stock': fields.Integer(required=True, description='Existencia actual')
})

product_parser = api.parser()
product_parser.add_argument('sku', type=int, required=False, help='Número de referencia')
product_parser.add_argument('product', type=str, required=True, help='Nombre del producto')

update_product_parser = api.parser()
update_product_parser.add_argument('product', type=str, required=True, help='Nombre del producto')


@api.route('/')
class ProductsResource(Resource):
    """
    Muestra una lista de todos los 
    productos y te permite crear nuevos
    """

    @api.doc(id='get_products')
    @api.marshal_with(product)
    def get(self):
        """Enlista todos los productos"""
        products = db.session.query(Product).all() 
        return products
    
    @api.doc(id='post_product', parser=product_parser)
    @api.marshal_with(product)
    def post(self):
        """Crea un producto"""
        args = product_parser.parse_args()
        product = Product(product=args['product'])
        
        if args['sku']:
            if db.session.query(Product).filter(Product.sku==args['sku']):
                product.sku = args['sku']
            else:
                abort(404, message=f'Ya existe un producto con el sku:{args["sku"]}')
        
        db.session.add(product)
        db.session.commit()
        
        return product, 201


@api.route('/<sku>')
class ProductResource(Resource):
    """
    Muestra los datos de un producto,
    te permite modificarlo y eliminarlo
    """

    @api.doc(id='get_product')
    @api.marshal_with(product)
    def get(self, sku):
        """Muestra los datos de un producto"""
        product = db.session.query(Product).filter(Product.sku == sku).first()
        if not product:
            abort(404, message=f'No existe un producto con el sku:{sku}')
        return product
    
    @api.doc(id='update_product', parser=update_product_parser)
    @api.marshal_with(product)
    def patch(self, sku):
        """Actualiza un producto"""
        args = update_product_parser.parse_args()
        product = db.session.query(Product).filter(Product.sku == sku).first()
        if not product:
            abort(404, message=f'No existe un producto con el sku:{sku}')
        product.product = args['product']
        
        db.session.add(product)
        db.session.commit()
        
        return product, 201

    @api.doc(id='delete_product')
    def delete(self, sku):
        """Elimina un producto"""
        product = db.session.query(Product).filter(Product.sku == sku).first()
        if not product:
            abort(404, message=f'No existe un producto con el sku:{sku}')
        
        db.session.delete(product)
        db.session.commit()
        
        return {}, 204


@api.route('/<sku>/tiendas/')
class ProductInStockResource(Resource):
    """
    Muestra unas lista de todas las tiendas con stock
    """
    @api.doc(id='get_stores_with_stock')
    @api.marshal_with(stock)
    def get(self, sku):
        """Enlista las tiendas donde hay stock"""
        stock = db.session.query(Stock).filter(Stock.product_sku == sku, Stock.stock >= 1).all()
        if not stock:
            abort(404, message=f'No hay stock del producto {sku} en ninguna tienda')
        return stock