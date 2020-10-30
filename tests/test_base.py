"""Pruebas de la aplicación"""

# Utils
import unittest
import json

# Aplicación
from app import app
from database import db


class AppTest(unittest.TestCase):
    """Casos de prueba para la aplicación"""

    def setUp(self):
        """Inicializar la aplicación y la base de datos"""
        self.app = app.test_client()
        self.db = db.get_db()

    def test_successful_post_to_product(self):
        """Probar crear un producto"""
        payload = json.dumps({
            "sku": 1151,
            "product": "Procesador Intel Core i9"
        })
        response = self.app.post(
            '/productos', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_get_product(self):
        """Probar listar los productos"""
        response = self.app.get('/productos')
        self.assertEqual(200, response.status_code)
    
    def test_successful_get_specific_product(self):
        """Probar mostar los datos de un producto en especifico"""
        response = self.app.get('/productos/1151')
        self.assertEqual(200, response.status_code)
    
    def test_successful_patch_specific_product(self):
        """Probar modificar un producto"""
        payload = json.dumps({
            "product": "Procesador Intel Core i9 3.10GHz"
        })
        response = self.app.patch(
            '/productos/1151', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_post_to_store(self):
        """Probar crear una tienda"""
        payload = json.dumps({
            "store": "Digitallife",
            "address": "Av. Adolfo López Mateos Sur 5510"
        })
        response = self.app.post(
            '/tiendas', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_get_store(self):
        """Probar listar las tiendas"""
        response = self.app.get('/tiendas')
        self.assertEqual(200, response.status_code)
    
    def test_successful_get_specific_store(self):
        """Probar mostrar los datos de una tienda en especifico"""
        response = self.app.get('/tiendas/1')
        self.assertEqual(200, response.status_code)
    
    def test_successful_patch_specific_store(self):
        """Probar modificar una tienda"""
        payload = json.dumps({
            "store": "Digitallife López Mateos"
        })
        response = self.app.patch(
            '/tiendas/1', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_post_to_stock(self):
        """Probar añadirle stock de un producto a una tienda"""
        payload = json.dumps({
            "store_id": 1,
            "product_sku": 1151,
            "minimum": 5,
            "stock": 3
        })
        response = self.app.post(
            '/stock', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_successful_get_insufficient_stock(self):
        """Probar si hay suficiente stock en una tienda"""
        response = self.app.get('/tiendas/1/stock/insuficiente')
        self.assertEqual(200, response.status_code)
    
    def test_successful_patch_stock_from_store(self):
        """Modificar el stock de una tienda"""
        payload = json.dumps({
            "stock": 6
        })
        response = self.app.post(
            '/tiendas/1/stock/1151', 
            headers={"Content-Type": "application/json"}, 
            data=payload
        )
        self.assertEqual(201, response.status_code)
    
    def test_unsuccessful_get_insufficient_stock(self):
        """Probar si no hay stock en una tienda"""
        response = self.app.get('/tiendas/1/stock/insuficiente')
        self.assertEqual(404, response.status_code)

    def test_successful_delete_specific_product(self):
        """Probar borrar un producto"""
        response = self.app.delete('/productos/1151')
        self.assertEqual(204, response.status_code)

    def test_successful_delete_specific_store(self):
        """Probar borrar una tienda"""
        response = self.app.delete('/tiendas/1')
        self.assertEqual(204, response.status_code)