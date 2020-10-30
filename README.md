# Prueba Cargamos

Contexto: rear una API Rest con Flask que implemente un sistema de inventario de productos utilizando una BD Postgres.

### Requisitos de software
-  docker
-  docker-compose

### Instrucciones para ejecución
Navegar desde la terminal hasta la carpeta previamente descargada y extraida, ahí haremos el build de las imagenes.
```sh
$ docker-compose -f local.yml build
```
Esperamos a que termine de generar las imagenes para poder correr los contenedores.
```sh
$ docker-compose -f local.yml up
```
Expone el puerto 5000 de la máquina host que está atado al puesto 5000 del contenedor, vamos al navegador.

    localhost:5000

Ahí tenemos la raíz de la API, se visualizará su documentación.

## RUTAS IMPORTANTES DE LA API
### Productos
    localhost:5000/productos/
GET - Enlista todos los productos
POST - Crea un producto
- sku: integer (Número de referencia del producto, opcional)
- product: string (Nombre del producto, requerido)


    localhost:5000/productos/{sku}/
GET - Muestra datos de un producto
DELETE - Elimina un producto
PATCH - Actualiza un producto 
- product: string (Nombre del producto, requerido)


    localhost:5000/productos/{sku}/tiendas/
GET - Enlista todas las tiendas donde hay stock del producto

### Tiendas
    localhost:5000/tiendas/
GET - Enlista todos las tiendas
POST - Crea una tienda
- store: string (Nombre de la tienda, requerido)
- address: string (Dirección de la tienda, requerido)


    localhost:5000/tiendas/{id}/
GET - Muestra datos de una tienda
DELETE - Elimina una tienda
PATCH - Actualiza una tienda 
- store: string (Nombre de la tienda, no requerido)
- address: string (Dirección de la tienda, no requerido)


    localhost:5000/tiendas/{id}/stock/
GET - Enlista el stock de la tienda
POST - Da de alta un nuevo producto en la tienda
- product_sku: integer (Número sku del producto, requerido)
- minimum: integer (Existencia mínima, requerido)
- stock: integer (Existencia actual, requerido)


    localhost:5000/tiendas/{id}/stock/{sku}/
PATCH - Actualiza el stock de un producto
- minimum: integer (Existencia mínima, no requerido)
- stock: integer (Existencia actual, no requerido)


    localhost:5000/tiendas/{id}/stock/insuficiente/
GET - Enlista el stock insuficiente de la tienda











